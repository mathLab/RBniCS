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
## @file numpy_io.py
#  @brief I/O helper functions
#
#  @author Francesco Ballarin <francesco.ballarin@sissa.it>
#  @author Gianluigi Rozza    <gianluigi.rozza@sissa.it>
#  @author Alberto   Sartori  <alberto.sartori@sissa.it>

###########################     I/O     ########################### 
## @defgroup IO Input/output methods
#  @{

import os # for path
import numpy
from RBniCS.utils.mpi import mpi_comm

class TextIO(object):
    
    ## Load a variable from file
    @staticmethod
    def load_file(directory, filename):
        raise NotImplementedError("File loading is not implemented yet for text files")
    
    ## Save a variable to file
    @staticmethod
    def save_file(content, directory, filename):
        if mpi_comm.rank == 0:
            with open(str(directory) + "/" + filename + ".txt", "w") as outfile:
                for i in range(len(content)):
                    outfile.write(str(i) + " " + str(content[i]) + "\n")
        mpi_comm.barrier()
            
    ## Check if the file exists
    @staticmethod
    def exists_file(directory, filename):
        raise NotImplementedError("There is no need to check if files exists, since file loading is not implemented yet for text files")

#  @}
########################### end - I/O - end ########################### 
