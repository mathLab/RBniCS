# Copyright (C) 2015-2017 by the RBniCS authors
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
## @file __init__.py
#  @brief Init file for auxiliary I/O module
#
#  @author Francesco Ballarin <francesco.ballarin@sissa.it>
#  @author Gianluigi Rozza    <gianluigi.rozza@sissa.it>
#  @author Alberto   Sartori  <alberto.sartori@sissa.it>

from __future__ import print_function
from rbnics.utils.mpi.log import log, CRITICAL, ERROR, WARNING, INFO, PROGRESS, TRACE, DEBUG
from rbnics.utils.mpi.mpi import is_io_process, parallel_max
from rbnics.utils.mpi.print import print

__all__ = [
    'log', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'PROGRESS', 'TRACE', 'DEBUG',
    'is_io_process', 'parallel_max',
    'print'
]
