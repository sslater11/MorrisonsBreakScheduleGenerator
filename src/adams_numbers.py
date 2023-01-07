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

class AdamsNumbers:
    def __init__( self ):
        self.earliest_shift_start_time = ADAMS_NUMBERS_EARLIEST_START
        self.latest_shift_start_time   = ADAMS_NUMBERS_LATEST_START
        self.adams_list = []
        self.adams_list_titles = []
        self.exclusions_list = _getEmployeesFromFile( ADAMS_NUMBERS_EXCLUSIONS_FILE_PATH )
        self.html_exclusions_list = ""

        self.addTimes()

        # This class needs to hold all the numbers for every hour for several departments.
        # it then needs to store that data as a list which is easily merged
        # the final output will look like this
        # adams numbers
        # time  | checkouts | kiosk | team leaders | petrol
        # 13:00 | 4         | 2     | 1            | 1
        # 14:00 | 5         | 2     | 2            | 1
        # 15:00 | 6         | 1     | 2            | 1
        # 16:00 | 4         | 2     | 1            | 1
        # 
        # 
        # To make this I need to pass to it add( list_of_employees, department, day_of_the_week )
        # 
        # Finally, add a html output for it and we're sorted!



    @staticmethod
    def _countHowManyEmployeesInAtHour( list_of_employees, department, day_of_the_week , hour, exclusions_list ):
        employees_working = 0

        for employee in list_of_employees:
            if not isEmployeeInList( employee, exclusions_list ):
                department_at_hour = employee.getDepartmentAtHour( day_of_the_week, hour )

                if department_at_hour == None:
                    # Just skip over it.
                    continue

                elif DepartmentHandler.hasSameDepartment( department_at_hour, department ):
                    # Make sure we don't count people who go home during this hour.
                    if employee.getHourShiftEnds( day_of_the_week ) != hour:
                        employees_working = employees_working + 1

        return employees_working


    @staticmethod
    # Count the number of reliefs in the store.
    def _countHowManyOtherEmployeesInAtHour( list_of_employees, day_of_the_week , hour, exclusions_list ):
        employees_working = 0

        for employee in list_of_employees:
            if not isEmployeeInList( employee, exclusions_list ):
                department_at_hour = employee.getDepartmentAtHour( day_of_the_week, hour )

                if department_at_hour == None:
                    # Just skip over it.
                    continue

                elif DepartmentHandler.isDepartmentTeamLeader( department_at_hour.getDepartment(0) ):
                    # Just skip over it.
                    continue
                elif DepartmentHandler.isDepartmentSelfScan  ( department_at_hour.getDepartment(0) ):
                    # Just skip over it.
                    continue
                elif DepartmentHandler.isDepartmentCheckouts ( department_at_hour.getDepartment(0) ):
                    # Just skip over it.
                    continue
                elif DepartmentHandler.isDepartmentKiosk     ( department_at_hour.getDepartment(0) ):
                    # Just skip over it.
                    continue
                elif DepartmentHandler.isDepartmentTrolleys  ( department_at_hour.getDepartment(0) ):
                    # Just skip over it.
                    continue
                elif DepartmentHandler.isDepartmentPetrol    ( department_at_hour.getDepartment(0) ):
                    # Just skip over it.
                    continue
                elif DepartmentHandler.isDepartmentCafe      ( department_at_hour.getDepartment(0) ):
                    # Just skip over it.
                    continue
                else:
                    # Make sure we don't count people who go home during this hour.
                    if employee.getHourShiftEnds( day_of_the_week ) != hour:
                        employees_working = employees_working + 1

        return employees_working

    @staticmethod
    def _countHowManyEmployeesInAtTime( list_of_employees, department, day_of_the_week, hour, minute, exclusions_list ):
        employees_working = 0

        for employee in list_of_employees:
            if not isEmployeeInList( employee, exclusions_list ):
                if hour < 10:
                    cur_time = "0" + str(hour) + ":" + str(minute)
                else:
                    cur_time = str(hour) + ":" + str(minute)

                department_at_time = employee.getDepartmentAtTime( day_of_the_week, cur_time )

                if department_at_time == None:
                    # Just skip over it.
                    continue

                elif DepartmentHandler.hasSameDepartment( department_at_time, department ):
                    # Make sure we don't count people who go home during this time.
                    if employee.getHourShiftEnds( day_of_the_week ) == hour and \
                        employee.getMinuteShiftEnds( day_of_the_week ) == minute:
                            # Do nothing
                            pass
                    else:
                        employees_working = employees_working + 1


        return employees_working

    #@staticmethod
    #def _countHowManyEmployeesInAtTime( list_of_employees, department, day_of_the_week, current_time, exclusions_list ):
    #    employees_working = 0

    #    for employee in list_of_employees:
    #        if not isEmployeeInList( employee, exclusions_list ):
    #            department_at_time = employee.getDepartmentAtTime( day_of_the_week, current_time )

    #            if department_at_time == None:
    #                # Just skip over it.
    #                continue

    #            elif (department == None) or DepartmentHandler.hasSameDepartment( department_at_time, department ):
    #                # Make sure we don't count people who go home during this hour.
    #                time_shift_ends = employee.getShiftEnd( day_of_week )
    #                time_shift_ends = datetime.strptime( time_shift_ends, "%H:%M" )
    #                if time_shift_ends != current_time:
    #                    employees_working = employees_working + 1


    #    return employees_working

    @staticmethod
    # Counts how many people are in who aren't Team Leaders, Checkouts, Kiosk, Trolleys or Petrol
    def _countHowManyOtherEmployeesInAtTime( list_of_employees, day_of_the_week, current_time, exclusions_list ):
        employees_working = 0

        for employee in list_of_employees:
            if not isEmployeeInList( employee, exclusions_list ):
                department_at_time = employee.getDepartmentAtTime( day_of_the_week, current_time )

                if department_at_time == None:
                    # Just skip over it.
                    continue

                    # Make sure we don't count people who go home during this hour.
                    time_shift_ends = employee.getShiftEnd( day_of_week )
                    time_shift_ends = datetime.strptime( time_shift_ends, "%H:%M" )
                    if time_shift_ends != current_time:
                        employees_working = employees_working + 1

        return employees_working

    # Takes a string for the title to give the table column a title.
    # needs a list of employees to scan through
    # The department we want to count them on.
    # The day of the week to see if they're working.
    def add(self, title, list_of_employees, department, day_of_the_week):
        if isinstance(title,     str) and \
          isinstance(list_of_employees, list) and \
          isinstance(department, DepartmentHandler) and \
          isinstance(day_of_the_week,       int):
            # All variables type checked.
            list_of_employees_at_hour = []
            for hour in range(self.earliest_shift_start_time, self.latest_shift_start_time):
                count = AdamsNumbers._countHowManyEmployeesInAtHour(list_of_employees, department, day_of_the_week, hour, self.exclusions_list)
                list_of_employees_at_hour = list_of_employees_at_hour + [str(count)]
                #print( str(hour) + ":00 - " + str(count) )
            self.adams_list.append( list_of_employees_at_hour )
            self.adams_list_titles.append( title )

            # Generate the exclusion text for the html file.
            for employee in list_of_employees:
                if ( not employee.isDayOff( day_of_the_week ) ) and isEmployeeInList( employee, self.exclusions_list ):
                    self.html_exclusions_list = self.html_exclusions_list + "\n            <br>Excluded " + employee.getName() + " from the count."

        else:
            raise TypeError("Passed the wrong object types to this function.")

    # Used for adding managers and reliefs,
    # So we need to exclude them from being counted if they're already
    # assigned to Checkouts, Kiosk, Team Leaders, or Petrol
    # Title is the title at the heading at the top of adam's numbers.
    def addOthersFromList( self, title, list_of_employees, day_of_the_week ):
        if isinstance(title,     str) and \
          isinstance(list_of_employees, list) and \
          isinstance(day_of_the_week,       int):
            # All variables type checked.
            list_of_employees_at_hour = []
            for hour in range(self.earliest_shift_start_time, self.latest_shift_start_time):
                count = AdamsNumbers._countHowManyOtherEmployeesInAtHour(list_of_employees, day_of_the_week, hour, self.exclusions_list)
                list_of_employees_at_hour = list_of_employees_at_hour + [str(count)]
                #print( str(hour) + ":00 - " + str(count) )
            self.adams_list.append( list_of_employees_at_hour )
            self.adams_list_titles.append( title )

            # Generate the exclusion text for the html file.
            for employee in list_of_employees:
                if ( not employee.isDayOff( day_of_the_week ) ) and isEmployeeInList( employee, self.exclusions_list ):
                    self.html_exclusions_list = self.html_exclusions_list + "\n            <br>Excluded " + employee.getName() + " from the count."
        else:
            raise TypeError("Passed the wrong object types to this function.")

    def addTimes( self ):
        list_of_hours = []
        for hour in range(self.earliest_shift_start_time, self.latest_shift_start_time):
            #if hour < 10:
            #    hour = "0" + str(hour) + ":00"
            #else:
            #    hour =  str(hour) + ":00"
            hour = str(hour)

            list_of_hours = list_of_hours + [hour]
            #print( str(hour) + ":00 - " + str(count) )
        self.adams_list.append( list_of_hours )
        self.adams_list_titles.append( "Time" )



    def getHTML( self ):
        html_table_start = """
            <p style="font-size: """ + FONT_SIZE_ADAMS_NUMBERS + """px">
            C = Cashiers<br>
            S = Self Scan<br>
            TL = Team Leaders<br>
            K = Kiosk<br>
            P = Petrol<br>
            R = Reliefs
            """ + self.html_exclusions_list + """
            </p>
            <table class="adamsNumbersTable">
            <thead>
            <tr>
                <th colspan=\"""" + str(len(self.adams_list)) +"""\"> Adam's Numbers </th>
            </tr>
            <tr>
"""

        for i in range( len(self.adams_list) ):
            html_table_start = html_table_start + """                <th>""" + self.adams_list_titles[i] + """</th>\n"""

        html_table_start = html_table_start + """            </tr>
            </thead>
            <tbody>
"""

        html_table_end = """            </tbody>
            </table>
"""

        # Generate the lines for each employee in the table
        table_rows = ""
        for i in range( self.earliest_shift_start_time, self.latest_shift_start_time ):
            table_rows += """            <tr>\n"""
            for k in range( len(self.adams_list) ):
                index = i - self.earliest_shift_start_time
                if self.adams_list[k][index] == "0":
                    str_count = ""
                else:
                    str_count = self.adams_list[k][index]
                if k == 0:
                    table_rows += """                <td align="center" class="adamsNumbersHourHighlight">""" + str_count + """</td>\n"""
                else:
                    table_rows += """                <td align="center">""" + str_count + """</td>\n"""
            table_rows += """            </tr>\n"""
        final_html = html_table_start + table_rows + html_table_end

        return final_html
