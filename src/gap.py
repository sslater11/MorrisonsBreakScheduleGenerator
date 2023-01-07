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
from datetime import timedelta
from constants import *

class Gap:
    def __init__( self, week_commencing_date, day_of_the_week, department, hour_start, minute_start ):
        self.setHourStart( hour_start )
        self.setMinuteStart( minute_start )
        self.department      = department
        self.day_of_the_week = day_of_the_week
        self.week_commencing_date = week_commencing_date
        self.hour_end = -1
        self.minute_end = -1

    @staticmethod
    def _integersToTimeStr( hour, minute ):
        if hour < 10:
            hour = "0" + str(hour)
        else:
            hour =       str(hour)

        if minute < 10:
            minute = "0" + str(minute)
        else:
            minute =       str(minute)

        return hour + ":" + minute

    def setHourStart( self, hour ):
        self.hour_start   = int(hour)

    def setMinuteStart( self, minute ):
        self.minute_start = int(minute)

    def setHourEnd( self, hour ):
        self.hour_end   = int(hour)

    def setMinuteEnd( self, minute ):
        self.minute_end = int(minute)

    def toString( self ):
        str_day = DAYS_OF_THE_WEEK[self.day_of_the_week]

        str_time_start = Gap._integersToTimeStr( self.hour_start, self.minute_start )
        str_time_end   = Gap._integersToTimeStr( self.hour_end,   self.minute_end   )
        str_department = self.department.getDepartment(0)

        current_date = self.week_commencing_date + timedelta(days = self.day_of_the_week)
        # Print out "Monday 31 Aug"
        #str_the_date = current_date.strftime( "%A %d %b" )
        # Print out "Mon 31 Aug"
        str_the_date = current_date.strftime( "%a %d %b" )
        return str_the_date + ":\n" + str_time_start + " - " + str_time_end + " - " + str_department

    def toStringWithoutDay( self ):
        str_day = DAYS_OF_THE_WEEK[self.day_of_the_week]

        str_time_start = Gap._integersToTimeStr( self.hour_start, self.minute_start )
        str_time_end   = Gap._integersToTimeStr( self.hour_end,   self.minute_end   )
        str_department = self.department.getDepartment(0)

        return str_time_start + " - " + str_time_end + " - " + str_department


    def toHTML( self ):
        str_day = DAYS_OF_THE_WEEK[self.day_of_the_week]

        str_time_start = Gap._integersToTimeStr( self.hour_start, self.minute_start )
        str_time_end   = Gap._integersToTimeStr( self.hour_end,   self.minute_end   )
        str_department = self.department.getDepartment(0)

        html  = """            <tr>\n"""
        html += """                <td align="left"  >""" + str_department + """</td>\n"""
        html += """                <td align="left"  >""" + str_time_start + """</td>\n"""
        html += """                <td align="left"  >""" + str_time_end   + """</td>\n"""
        html += """                <td align="left"  >&nbsp;</td>\n"""
        html += """            </tr>\n"""
        return html
