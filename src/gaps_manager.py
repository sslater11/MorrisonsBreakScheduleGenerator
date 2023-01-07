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

from constants import *
from employee_handler import _getEmployeesFromFile
from employee_handler import isEmployeeInList
from department_handler import DepartmentHandler
from adams_numbers import AdamsNumbers
from gap import Gap

class GapsManager:
    def __init__( self ):
        self.list_of_gaps = []
        self.exclusions_list = _getEmployeesFromFile( ADAMS_NUMBERS_EXCLUSIONS_FILE_PATH )
        self.html_exclusions_list = ""
        self.is_smaller_font = False

    def isEmpty( self ):
        if( len( self.list_of_gaps ) > 0 ):
            return False
        else:
            return True

    @staticmethod
    # Returns the starting time the department needs staff.
    def getDepartmentActiveStart( department, day_of_the_week ):
        for i in all_department_active_times:
            if DepartmentHandler.hasSameDepartment (i[ DEPARTMENT_ACTIVE_INDEX_DEPARTMENT ], department.getDepartment(0) ):
                if day_of_the_week == i[ DEPARTMENT_ACTIVE_INDEX_DAY ]:
                    return i[ DEPARTMENT_ACTIVE_INDEX_START_TIME ]

        return None

    @staticmethod
    # Returns the time the department closes and no longer needs staff.
    def getDepartmentActiveEnd( department, day_of_the_week ):
        for i in all_department_active_times:
            if DepartmentHandler.hasSameDepartment( i[ DEPARTMENT_ACTIVE_INDEX_DEPARTMENT ], department.getDepartment(0) ):
                if day_of_the_week == i[ DEPARTMENT_ACTIVE_INDEX_DAY ]:
                    return i[ DEPARTMENT_ACTIVE_INDEX_END_TIME ]

        return None


    # Needs a list of employees to scan through
    # The department we want to count them on.
    # The day of the week to see if they're working.
    def add(self, week_commencing_date, list_of_employees, department, day_of_the_week):
        if isinstance(list_of_employees, list) and \
          isinstance(department, DepartmentHandler) and \
          isinstance(day_of_the_week,       int):
            # All variables type checked.

            # Generate a list of gaps on this department
            # We need to scan through the whole day in 15 minute increments.
            # Check if there's any employee at that time scheduled in
            # if not, add the gaps list

            time_start = GapsManager.getDepartmentActiveStart( department, day_of_the_week )
            time_end   = GapsManager.getDepartmentActiveEnd  ( department, day_of_the_week )

            start_hour   = int( time_start[:2] )
            start_minute = int( time_start[3:] )

            end_hour     = int( time_end[:2] )
            end_minute   = int( time_end[3:] )

            has_a_gap_been_found = False
            gap = None
            for hour in range( start_hour, end_hour ):
                for minute in [ "00", "15", "30", "45", "59" ]:
                    if ( hour == start_hour )  and  ( int( minute ) < start_minute ):
                        # Time is before the starting time, so do nothing
                        pass
                    else:

                        if has_a_gap_been_found:
                            count = AdamsNumbers._countHowManyEmployeesInAtTime(list_of_employees, department, day_of_the_week, hour, minute, self.exclusions_list)
                            #print( str(count) + "count at " + str(hour) + ":" + str(minute) )

                            if( count > 0 ):
                                # End of the gap.
                                gap.setHourEnd  ( hour   )
                                gap.setMinuteEnd( minute )
                                has_a_gap_been_found = False
                                self.list_of_gaps += [ gap ]
                        else:
                            count = AdamsNumbers._countHowManyEmployeesInAtTime(list_of_employees, department, day_of_the_week, hour, minute, self.exclusions_list)
                            if count == 0:
                                gap = Gap( week_commencing_date, day_of_the_week, department, hour, minute )
                                has_a_gap_been_found = True

            if has_a_gap_been_found:
                # There's a gap until the end of the active timeslot.
                # Set it to the last time.
                gap.setHourEnd  ( end_hour   )
                print("set hour end to: " + str(end_hour) )
                gap.setMinuteEnd( end_minute )
                self.list_of_gaps += [ gap ]

            # Generate the exclusion text for the html file.
            for employee in list_of_employees:
                if ( not employee.isDayOff( day_of_the_week ) ) and isEmployeeInList( employee, self.exclusions_list ):
                    self.html_exclusions_list = self.html_exclusions_list + "\n            <br>Excluded " + employee.getName() + " from the gaps."
        else:
            raise TypeError("Passed the wrong object types to this function.")


    def toString( self ):
        previous_day = -1
        result = ""
        for i in self.list_of_gaps:
            if i.day_of_the_week == previous_day:
                result += i.toStringWithoutDay() + "\n"
            else:
                if previous_day != -1:
                    result += "\n"
                result += i.toString() + "\n"

            previous_day = i.day_of_the_week

        return result

    def getHTML( self ):
        str_table_class = ""
        if self.is_smaller_font:
            str_table_class = "myTableSmall"
        else:
            str_table_class = "myTable"

        html_table_start = self.html_exclusions_list + """
            </p>
            <table class=\"""" + str_table_class + """\">
            <thead>
            <tr>
                <th colspan=\"4\"> Gaps </th>
            </tr>
            <tr>
                <th>Department</th>
                <th>Start</th>
                <th>Finish</th>
                <th>Person Covering Gap</th>
            </tr>
            </thead>
            <tbody>
"""

        html_table_end = """            </tbody>
            </table>
"""

        table_rows = ""
        for i in self.list_of_gaps:
            table_rows += i.toHTML()

        final_html = html_table_start + table_rows + html_table_end

        return final_html
