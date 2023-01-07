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

from employee_handler import getShiftStartAsInt

class MyHTMLTable:
    def __init__( self, title, is_smaller_font=False ):
        self.is_smaller_font = is_smaller_font
        self.CASHIER_NAME      = 0
        self.SHIFT_START       = 1
        self.SHIFT_END         = 2
        self.SHIFT_LENGTH      = 3
        self.DEPARTMENTS       = 4
        self.BREAK_TIME        = 5
        self.BREAK_TIME_LENGTH = 6
        self.LUNCH_TIME        = 7

        self.title = title
        self.table_lines = []

    # Sort the table by the shift start times
    def sort( self ):
        self.table_lines.sort(key=getShiftStartAsInt)

    def addLine(self, cashier_name, shift_start, shift_end, shift_length, departments, break_time, break_time_length, lunch_time, include_till_column=True):
        if isinstance(cashier_name,     str) and \
          isinstance(shift_start,       str) and \
          isinstance(shift_end,         str) and \
          isinstance(shift_length,      str) and \
          isinstance(departments,       str) and \
          isinstance(break_time,        str) and \
          isinstance(break_time_length, str) and \
          isinstance(lunch_time,        str):
            # All variables are strings,
            # so add them to the table.
            self.table_lines.append( [cashier_name, shift_start, shift_end, shift_length, departments, break_time, break_time_length, lunch_time] )
        else:
            raise TypeError("Must pass all arguments as a string.")

    def getLineCount(self):
        return len( self.table_lines )

    # A very messy looking function to preserve the html code style.
    # It returns the html code with a table inside it.
    def getHTML(self):
        str_table_class = ""
        if self.is_smaller_font:
            str_table_class = "myTableSmall"
        else:
            str_table_class = "myTable"
        html_table_start = """
            <table class=\"""" + str_table_class + """\">
            <thead>
            <tr>
                <th>"""  +  self.title  +  """</th>
                <th>Till</th>
                <th>Start</th>
                <th>Finish</th>
                <th>Length</th>
                <th>Department</th>
                <th>Break</th>
                <th>Break</th>
                <th>Break<br>Length</th>
                <th>Lunch</th>
            </tr>
            </thead>
            <tbody>
"""

        html_table_end = """            </tbody>
            </table>
"""

        # Generate the lines for each employee in the table
        table_rows = ""
        for i in self.table_lines:
            table_rows += """            <tr>\n"""
            table_rows += """                <td align="left"  >""" + i[self.CASHIER_NAME]      + """</td>\n"""
            table_rows += """                <td align="center">""" + ""                        + """</td>\n"""
            table_rows += """                <td align="center">""" + i[self.SHIFT_START]       + """</td>\n"""
            table_rows += """                <td align="center">""" + i[self.SHIFT_END]         + """</td>\n"""
            table_rows += """                <td align="center">""" + i[self.SHIFT_LENGTH]      + """</td>\n"""
            table_rows += """                <td align="left" style="vertical-align:middle" >""" + i[self.DEPARTMENTS]       + """</td>\n"""
            table_rows += """                <td align="center">""" + i[self.BREAK_TIME]        + """</td>\n"""
            table_rows += """                <td align="center">""" + ""                        + """</td>\n"""
            table_rows += """                <td align="center">""" + i[self.BREAK_TIME_LENGTH] + """</td>\n"""
            table_rows += """                <td align="center">""" + i[self.LUNCH_TIME]        + """</td>\n"""
            table_rows += """            </tr>\n"""

        final_html = html_table_start + table_rows + html_table_end

        return final_html
