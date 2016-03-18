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
## @file reduced_method_factory.py
#  @brief Factories to associate parametrized problem classes to reduction method classes.
#
#  @author Francesco Ballarin <francesco.ballarin@sissa.it>
#  @author Gianluigi Rozza    <gianluigi.rozza@sissa.it>
#  @author Alberto   Sartori  <alberto.sartori@sissa.it>

#~~~~~~~~~~~~~~~~~~~~~~~~~     REDUCED METHOD FACTORY CLASSES     ~~~~~~~~~~~~~~~~~~~~~~~~~# 
## @class ReducedBasis
#
# Factories to associate parametrized problem classes to reduction method classes: reduced basis method
def ReducedBasis(truth_problem):
    # Determine what kind of RB method is need
    def _ReducedBasis_TypeFactory(truth_problem):
        if isinstance(truth_problem, EllipticCoerciveProblem):
            return EllipticCoerciveRBReduction
        else:
            raise RuntimeError("Invalid arguments in ReducedBasis factory.")
    
    # Add EIM or SCM, as required
    @_DecoratedReductionMethod_TypeFactory(truth_problem)
    class _ReducedBasis_ReductionMethod( _ReducedBasis_TypeFactory(truth_problem) ):
        pass
        
    # Finally, return an instance of the generated class
    return _ReducedBasis_ReductionMethod(truth_problem)
    
## @class PODGalerkin
#
# Factories to associate parametrized problem classes to reduction method classes: POD-Galerkin method
def PODGalerkin(truth_problem):
    # Determine what kind of RB method is need
    def _PODGalerkin_TypeFactory(truth_problem):
        if isinstance(truth_problem, EllipticCoerciveProblem):
            return EllipticCoercivePODGalerkinReduction
        else:
            raise RuntimeError("Invalid arguments in PODGalerkin factory.")
            
    # Add EIM or SCM, as required
    @_DecoratedReductionMethod_TypeFactory(truth_problem)
    class _PODGalerkin_ReductionMethod( _PODGalerkin_TypeFactory(truth_problem) ):
        pass
        
    # Finally, return an instance of the generated class
    return _PODGalerkin_ReductionMethod(truth_problem)

# Decorator to add EIM or SCM, as required
def _DecoratedReductionMethod_TypeFactory(truth_problem):
    def _DecoratedReductionMethod_TypeFactory__Decorator(ReductionMethod_DerivedClass):
        DecoratedReductionMethod_Type = ReductionMethod_DerivedClass
        if isinstance(truth_problem, EIMDecoratedProblem_Class):
            DecoratedReductionMethod_Type = EIMDecoratedReductionMethod(DecoratedReductionMethod_Type)
        if isinstance(truth_problem, ExactParametrizedFunctionEvaluationDecoratedProblem_Class):
            DecoratedReductionMethod_Type = ExactParametrizedFunctionEvaluationDecoratedReductionMethod(DecoratedReductionMethod_Type)
        if isinstance(truth_problem, SCMDecoratedProblem_Class):
            DecoratedReductionMethod_Type = SCMDecoratedReductionMethod(DecoratedReductionMethod_Type)
        if isinstance(truth_problem, ExactCoercivityConstantDecoratedProblem_Class):
            DecoratedReductionMethod_Type = ExactCoercivityConstantDecoratedReductionMethod(DecoratedReductionMethod_Type)
        return DecoratedReductionMethod_Type
    return _DecoratedReductionMethod_TypeFactory__Decorator