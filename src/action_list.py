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


ACTION_SHIFT_END         = 1
ACTION_SHIFT_START       = 2
ACTION_BREAK_TIME        = 3
ACTION_LUNCH_TIME        = 4
ACTION_DEPARTMENT_CHANGE = 5

class ActionItem:
    def __init__( self, action_time, action_type, employee_name=None, break_time_length=None ):
        self.action_time = action_time
        self.action_type = action_type
        self.employee_names     = []
        self.break_time_lengths = []

        if (employee_name != None) and (break_time_length != None):
            self.add( employee_name, break_time_length )
        elif employee_name != None:
            self.add( employee_name )


    def add( self, employee_name, break_time_length=None):
        self.employee_names.append( employee_name )
        if break_time_length != None:
            self.break_time_lengths.append( break_time_length )

    def getActionTime( self ):
        return self.action_time

    def getActionType( self ):
        return self.action_type

    # Outputs an action like this [ "13:00", "Break", "Bob (15m)" ]
    def getStrings( self ):
        str_action_type = ""
        str_names = ""

        if self.action_type == ACTION_SHIFT_END:
            str_action_type, str_names = self._generateActionString( "Finished" )
        elif self.action_type == ACTION_SHIFT_START:
            str_action_type, str_names = self._generateActionString( "Starting" )
        # Commented out for now as the break times aren't accurate.
        #elif self.action_type == ACTION_BREAK_TIME:
        #    str_action_type, str_names = self._generateActionString( "Break", "Breaks" )
        #elif self.action_type == ACTION_LUNCH_TIME:
        #    str_action_type, str_names = self._generateActionString( "Lunch", "Lunches" )

        #old code
        #if self.action_type == ACTION_SHIFT_END:
        #    if len(self.employee_names) > 1:
        #        str_action_type = str(len(self.employee_names)) + " "
        #    str_action_type = str_action_type + "Finished"

        #    for i in range( len(self.employee_names) ):
        #        if i < (len(self.employee_names)-1):
        #            if (i % 3 == 0) and (i != 0):
        #                str_names = str_names + "<br>" + self.employee_names[i] + ", "
        #            else:
        #                str_names = str_names + self.employee_names[i] + ", "
        #        else:
        #            str_names = str_names + self.employee_names[i]

        #elif self.action_type == ACTION_SHIFT_START:
        #    if len(self.employee_names) > 1:
        #        str_action_type = str_action_type + str(len(self.employee_names)) + " "
        #    str_action_type = str_action_type + "Starting"

        #    for i in range( len(self.employee_names) ):
        #        if i < (len(self.employee_names)-1):
        #            if (i % 3 == 0) and (i != 0):
        #                str_names = str_names + "<br>" + self.employee_names[i] + ", "
        #            else:
        #                str_names = str_names + self.employee_names[i] + ", "
        #        else:
        #            if (i % 3 == 0) and (i != 0):
        #                str_names = str_names + "<br>" + self.employee_names[i]
        #            else:
        #                str_names = str_names + self.employee_names[i]




        #elif self.action_type == ACTION_BREAK_TIME:
        #    if len(self.employee_names) > 1:
        #        str_action_type = str_action_type + str(len(self.employee_names)) + " Breaks"
        #    else:
        #        str_action_type = str_action_type + "Break"

        #    for i in range( len(self.employee_names) ):
        #        if i < (len(self.employee_names)-1):
        #            str_names = str_names + self.employee_names[i] + " (" + self.break_time_lengths[i] + "), <br>"
        #        else:
        #            str_names = str_names + self.employee_names[i] + " (" + self.break_time_lengths[i] + ")"

        #elif self.action_type == ACTION_LUNCH_TIME:
        #    if len(self.employee_names) > 1:
        #        str_action_type = str_action_type + str(len(self.employee_names)) + " Lunches"
        #    else:
        #        str_action_type = str_action_type + "Lunch"

        #    for i in range( len(self.employee_names) ):
        #        if i < (len(self.employee_names)-1):
        #            str_names = str_names + self.employee_names[i] + ", <br>"
        #        else:
        #            str_names = str_names + self.employee_names[i]

        return [ self.action_time, str_action_type, str_names ]

    def _generateActionString( self, str_action_type, str_action_type_plural=None ):

        # Count how many people have this action, and append it if there's more
        if len(self.employee_names) > 1:
            if str_action_type_plural == None:
                str_action_type = str(len(self.employee_names)) + " " + str_action_type
            else:
                str_action_type = str(len(self.employee_names)) + " " + str_action_type_plural

        str_names = ""
        for i in range( len(self.employee_names) ):
            if i < (len(self.employee_names)-1):
                if (i % 3 == 0) and (i != 0):
                    str_names = str_names + "<br>" + self.employee_names[i] + ", "
                else:
                    str_names = str_names + self.employee_names[i] + ", "
            else:
                if (i % 3 == 0) and (i != 0):
                    str_names = str_names + "<br>" + self.employee_names[i]
                else:
                    str_names = str_names + self.employee_names[i]

        return str_action_type, str_names


# Used to create a list of what action the team leader needs to take next.
# E.g.
# 12:00 - Shift End   - Jerry Smith
# 12:15 - Break       - John Smith
# 12:45 - Break       - John Doe
# 13:00 - Shift Start - Bob Smith
class ActionList:
    def __init__( self ):
        self.action_list = []
        self.departments = []

    def _actionListGetTime( action_list_item ):
        return action_list_item.getActionTime()

    def _addItem( self, employee_name, action_time, action_type, break_time_length=None ):
        is_already_in_list = False
        # Check to see if this time and action type is in the list, and if it is, add to that item.
        for i in range( len(self.action_list) ):
            if (self.action_list[i].getActionTime() == action_time) and (self.action_list[i].getActionType() == action_type):
                if break_time_length == None:
                    self.action_list[i].add( employee_name )
                else:
                    self.action_list[i].add( employee_name, break_time_length )
                is_already_in_list = True
                break

        # If it wasn't in the list, add it now.
        if not is_already_in_list:
            if break_time_length == None:
                self.action_list.append( ActionItem(action_time, action_type, employee_name) )
            else:
                self.action_list.append( ActionItem(action_time, action_type, employee_name, break_time_length) )

    def addEmployees( self, department, employees, day_of_the_week ):
        self.departments.append( department )
        for employee in employees:
            if not employee.isDayOff( day_of_the_week ):
                employee_name     = employee.getName()
                shift_start       = employee.getShiftStart          ( day_of_the_week )
                shift_end         = employee.getShiftEnd            ( day_of_the_week )
                break_time        = employee.getBreakTimeAsString   ( day_of_the_week )
                break_time_length = employee.getBreakTimeLength     ( day_of_the_week )
                lunch_time        = employee.getLunchTime           ( day_of_the_week )

                self._addItem( employee_name, shift_start, ACTION_SHIFT_START )
                self._addItem( employee_name, shift_end,   ACTION_SHIFT_END )

                # Commented out until I get break times working properly
                #if break_time != "":
                #    self._addItem( employee_name, break_time,  ACTION_BREAK_TIME, break_time_length )

                #if lunch_time != "" :
                #    self._addItem( employee_name, lunch_time,  ACTION_LUNCH_TIME )


    def sort( self ):
        self.action_list.sort( key=ActionList._actionListGetTime )

        # bubble sort to sort by the Action Type, so that shift end is listed first, shift start next, then breaks, then lunch
        is_sorted = False
        while not is_sorted:
            is_sorted = True
            for i in range( len(self.action_list) - 1 ):
                # sort only if these both have the same times.
                if self.action_list[i].getActionTime() == self.action_list[i+1].getActionTime():
                    if self.action_list[i].getActionType() > self.action_list[i+1].getActionType():
                        is_sorted = False
                        temp_item = self.action_list[i]
                        self.action_list[i] = self.action_list[i+1]
                        self.action_list[i+1] = temp_item


    def getDepartmentsAsString( self ):
        str_result = ""
        for i in range( len(self.departments) ):
            if i == 0:
                str_result = self.departments[i]
            else:
                str_result = str_result + ", " + self.departments[i]

        return str_result

    def getHTML( self ):
        html_table_start = """
            <table class="actionListTable">
            <thead>
            <tr>
                <th colspan=\"3\"> Action List - """ + self.getDepartmentsAsString() + """</th>
            </tr>
            </thead>
            <tbody>
"""

        html_table_end = """            </tbody>
            </table>
"""

        # Generate the lines for each employee in the table
        table_rows = ""
        previous_action_hour = ""
        is_table_line_highlighted = True
        for i in range( len(self.action_list) ):
            str_action_time, str_action, str_employee_names = self.action_list[i].getStrings()

            str_row_class = ""
            if i == 0:
                previous_action_hour = str_action_time[:2]
            elif ( previous_action_hour != str_action_time[:2] ):
                is_table_line_highlighted = not is_table_line_highlighted
                previous_action_hour = str_action_time[:2]
                # add a gap
                #table_rows += """            <tr>\n"""
                #table_rows += """                <td class="tableGap" colspan="3">&nbsp;</td>\n"""
                #table_rows += """            </tr>\n"""

            # Add some padding to separate the hours from each other.
            if is_table_line_highlighted:
                # don't give the row a class
                str_row_class = ""
            else:
                # Highlight this row
                str_row_class = "class=\"actionListHighlightRow\""


            table_rows += """            <tr """ + str_row_class + """>\n"""
            table_rows += """                <td align="center"><b>""" + str_action_time    + """</b></td>\n"""
            table_rows += """                <td align="left"  >""" + str_action         + """</td>\n"""
            table_rows += """                <td align="left"  >""" + str_employee_names + """</td>\n"""
            table_rows += """            </tr>\n"""

        final_html = html_table_start + table_rows + html_table_end

        return final_html
