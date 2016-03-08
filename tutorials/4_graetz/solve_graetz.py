# Copyright (C) 2015-2016 by the RBniCS authors
#
# This file is part of RBniCS.
#
# RBniCS is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RBniCS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RBniCS. If not, see <http://www.gnu.org/licenses/>.
#
## @file solve_graetz.py
#  @brief Example 4: Graetz test case
#
#  @author Francesco Ballarin <francesco.ballarin@sissa.it>
#  @author Gianluigi Rozza    <gianluigi.rozza@sissa.it>
#  @author Alberto   Sartori  <alberto.sartori@sissa.it>

from dolfin import *
from RBniCS import *

#~~~~~~~~~~~~~~~~~~~~~~~~~     EXAMPLE 4: GRAETZ CLASS     ~~~~~~~~~~~~~~~~~~~~~~~~~# 
@ShapeParametrization(
    ("x[0]", "x[1]"), # subdomain 1
    ("mu[0]*(x[0] - 1) + 1", "x[1]"), # subdomain 2
)
class Graetz(EllipticCoerciveNonCompliantBase):
    
    ###########################     CONSTRUCTORS     ########################### 
    ## @defgroup Constructors Methods related to the construction of the reduced order model object
    #  @{
    
    ## Default initialization of members
    def __init__(self, V, subd, bound):
        # Call the standard initialization
        super(Graetz, self).__init__(mesh, subd, V)
        # ... and also store FEniCS data structures for assembly
        self.u = TrialFunction(V)
        self.v = TestFunction(V)
        self.dx = Measure("dx")(subdomain_data=subd)
        self.ds = Measure("ds")(subdomain_data=bound)
        # Store the velocity expression
        self.vel = Expression("x[1]*(1-x[1])", element=self.V.ufl_element())
        # Finally, initialize an SCM object to approximate alpha LB
        self.SCM_obj = SCM_Graetz(self)
        
    #  @}
    ########################### end - CONSTRUCTORS - end ########################### 
        
    ###########################     PROBLEM SPECIFIC     ########################### 
    ## @defgroup ProblemSpecific Problem specific methods
    #  @{
    
    ## Return the alpha_lower bound.
    def get_stability_factor(self):
        return self.SCM_obj.get_alpha_LB(self.mu)
    
    ## Return theta multiplicative terms of the affine expansion of the problem.
    def compute_theta(self, term):
        mu1 = self.mu[0]
        mu2 = self.mu[1]
        if term == "a":
            theta_a0 = mu2
            theta_a1 = mu2/mu1
            theta_a2 = mu1*mu2
            theta_a3 = 1.0
            return (theta_a0, theta_a1, theta_a2, theta_a3)
        elif term == "f":
            theta_f0 = - mu2
            theta_f1 = - mu2/mu1
            theta_f2 = - mu1*mu2
            theta_f3 = - 1.0
            return (theta_f0, theta_f1, theta_f2, theta_f3)
        elif term == "s":
            return (1.0,)
        elif term == "dirichlet_bc":
            return (1.0,)
        else:
            raise RuntimeError("Invalid term for compute_theta().")
                    
    ## Return forms resulting from the discretization of the affine expansion of the problem operators.
    def assemble_operator(self, term):
        v = self.v
        dx = self.dx
        if term == "a":
            u = self.u
            vel = self.vel
            a0 = inner(grad(u),grad(v))*dx(1) + 1e-15*u*v*dx
            a1 = u.dx(0)*v.dx(0)*dx(2) + 1e-15*u*v*dx
            a2 = u.dx(1)*v.dx(1)*dx(2) + 1e-15*u*v*dx
            a3 = vel*u.dx(0)*v*dx(1) + vel*u.dx(0)*v*dx(2) + 1e-15*u*v*dx
            return (a0, a1, a2, a3)
        elif term == "f":
            lifting = self.lifting
            vel = self.vel
            f0 = inner(grad(lifting),grad(v))*dx(1) + 1e-15*lifting*v*dx
            f1 = lifting.dx(0)*v.dx(0)*dx(2) + 1e-15*lifting*v*dx
            f2 = lifting.dx(1)*v.dx(1)*dx(2) + 1e-15*lifting*v*dx
            f3 = vel*lifting.dx(0)*v*dx(1) + vel*lifting.dx(0)*v*dx(2) + 1e-15*lifting*v*dx
            return (f0, f1, f2, f3)
        elif term == "s":
#            ds = self.ds
#            s0 = v*ds(3)
            s0 = v*dx(2)
            return (s0,)
        elif term == "dirichlet_bc":
            bc0 = [(self.V, Constant(0.0), self.bound, 1),
                   (self.V, Constant(0.0), self.bound, 5),
                   (self.V, Constant(0.0), self.bound, 6),
                   (self.V, Constant(1.0), self.bound, 2),
                   (self.V, Constant(1.0), self.bound, 4)]
            return (bc0,)
        elif term == "inner_product":
            x0 = u*v*dx + inner(grad(u),grad(v))*dx
            return (x0,)
        else:
            raise RuntimeError("Invalid term for assemble_operator().")
        
    #  @}
    ########################### end - PROBLEM SPECIFIC - end ########################### 
    
    ###########################     I/O     ########################### 
    ## @defgroup IO Input/output methods
    #  @{
    
    ## Preprocess the solution before plotting to add a lifting
    def preprocess_solution_for_plot(self, solution):
        solution_with_lifting = Function(self.V)
        solution_with_lifting.vector()[:] = solution.vector()[:] + self.lifting.vector()[:]
        return solution_with_lifting
        
    #  @}
    ########################### end - I/O - end ########################### 
    
#~~~~~~~~~~~~~~~~~~~~~~~~~     EXAMPLE 4: SCM CLASS     ~~~~~~~~~~~~~~~~~~~~~~~~~# 
class SCM_Graetz(SCM):
    
    ###########################     CONSTRUCTORS     ########################### 
    ## @defgroup Constructors Methods related to the construction of the reduced order model object
    #  @{
    
    ## Default initialization of members
    def __init__(self, parametrized_problem):
        # Call the standard initialization
        SCM.__init__(self, parametrized_problem)
        
        # Good guesses to help convergence of bounding box
        self.guess_bounding_box_minimum = (1.e-5, 1.e-5, 1.e-5, 1.e-5)
        self.guess_bounding_box_maximum = (1., 1., 1., 1.)
    
    #  @}
    ########################### end - CONSTRUCTORS - end ########################### 
    
    ###########################     PROBLEM SPECIFIC     ########################### 
    ## @defgroup ProblemSpecific Problem specific methods
    #  @{
    
    ## Set additional options for the eigensolver (bounding box minimum)
    def set_additional_eigensolver_options_for_bounding_box_minimum(self, eigensolver, qa):
        eigensolver.parameters["spectral_transform"] = "shift-and-invert"
        eigensolver.parameters["spectral_shift"] = self.guess_bounding_box_minimum[qa]
        
    ## Set additional options for the eigensolver (bounding box maximimum)
    def set_additional_eigensolver_options_for_bounding_box_maximum(self, eigensolver, qa):
        eigensolver.parameters["spectral_transform"] = "shift-and-invert"
        eigensolver.parameters["spectral_shift"] = self.guess_bounding_box_maximum[qa]
        
    #  @}
    ########################### end - PROBLEM SPECIFIC - end ########################### 


#~~~~~~~~~~~~~~~~~~~~~~~~~     EXAMPLE 4: MAIN PROGRAM     ~~~~~~~~~~~~~~~~~~~~~~~~~# 

# 1. Read the mesh for this problem
mesh = Mesh("data/graetz.xml")
subd = MeshFunction("size_t", mesh, "data/graetz_physical_region.xml")
bound = MeshFunction("size_t", mesh, "data/graetz_facet_region.xml")

# 2. Create Finite Element space (Lagrange P1)
V = FunctionSpace(mesh, "Lagrange", 1)

# 3. Allocate an object of the Graetz class
graetz_problem = Graetz(V, mesh, subd, bound)
mu_range = [(0.01, 10.0), (0.01, 10.0)]
graetz_problem.setmu_range(mu_range)

# 4. Choose PETSc solvers as linear algebra backend
parameters.linear_algebra_backend = 'PETSc'

# 5. Prepare reduction with a reduced basis method
reduced_basis_method = ReducedBasis(graetz_problem)
reduced_basis.setNmax(10)

# 6. Perform the offline phase
first_mu = (1.0, 1.0)
graetz_problem.setmu(first_mu)
reduced_basis.setxi_train(100)
reduced_graetz_problem = reduced_basis.offline()

# 7. Perform an online solve
online_mu = (10.0, 0.01)
reduced_graetz_problem.setmu(online_mu)
reduced_graetz_problem.online_solve()
