# Copyright (C) 2015-2018 by the RBniCS authors
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

from ufl.core.operator import Operator
from dolfin import assign, Function, has_pybind11, LagrangeInterpolator, project
if has_pybind11():
    from dolfin.function.expression import BaseExpression
else:
    from dolfin import Expression as BaseExpression

def evaluate_expression(expression, function):
    assert isinstance(expression, (BaseExpression, Function, Operator))
    if isinstance(expression, BaseExpression):
        LagrangeInterpolator.interpolate(function, expression)
    elif isinstance(expression, Function):
        assign(function, expression)
    elif isinstance(expression, Operator):
        project(expression, function.function_space(), function=function)
    else:
        raise ValueError("Invalid expression")