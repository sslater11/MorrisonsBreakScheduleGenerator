# Copyright (C) 2020  Simon Slater
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os
def _getEmployeesFromFile( file_path ):
    employee_list = []

    if not os.path.exists( file_path ):
        print("Couldn't open file \"" + file_path + "\"")
    else:
        file = open(file_path, "r")
        for line in file:
            line = line.strip()
            if (line != "") and (len(line) > 0):
                if line[0] != "#":
                    employee_list.append( line )

    return employee_list

def isEmployeeInList( employee, employee_list ):
    for i in employee_list:
        if i.lower() == employee.getName().lower():
            return True

    return False

# Will return 13:45 as an int 1345
def getShiftStartAsInt( employee_shift ):
    shift_start_times = employee_shift[1]
    hour = int( shift_start_times[:2]  )
    mins = int( shift_start_times[3:5] )
    result = (hour * 1000) + mins
    return result
