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
from department_handler import DepartmentHandler
from breaks_manager import BreaksManager

class Employee:
    def __init__(self, name):
        self.employee_name = name
        self.departments        = [] # This will be a list of DepartmentHandler objects
        self.shift_start_times  = []
        self.shift_end_times    = []
        self.break_times        = []
        self.break_time_lengths = []
        self.lunch_times        = []
        self.forced_department  = None
        self.forced_shifts      = []

        for i in range(7):
            self.break_times.append( None )
            self.forced_shifts.append( False )

    # convert the string "09:25" to the int 925
    @staticmethod
    def timeTo24Hour( time ):
        hour   = int( time[:2] )
        minute = int( time[3:] )

        return (hour * 100) + minute

    def forceShift( self, department, day_of_the_week, shift_start, shift_end, is_day_off=False):
        today = -1

        department = DepartmentHandler(department, "")

        if day_of_the_week.lower() == "mon":
            today = MONDAY
        if day_of_the_week.lower() == "tue":
            today = TUESDAY
        if day_of_the_week.lower() == "wed":
            today = WEDNESDAY
        if day_of_the_week.lower() == "thu":
            today = THURSDAY
        if day_of_the_week.lower() == "fri":
            today = FRIDAY
        if day_of_the_week.lower() == "sat":
            today = SATURDAY
        if day_of_the_week.lower() == "sun":
            today = SUNDAY

        if day_of_the_week.lower() == "monday":
            today = MONDAY
        if day_of_the_week.lower() == "tuesday":
            today = TUESDAY
        if day_of_the_week.lower() == "wednesday":
            today = WEDNESDAY
        if day_of_the_week.lower() == "thursday":
            today = THURSDAY
        if day_of_the_week.lower() == "friday":
            today = FRIDAY
        if day_of_the_week.lower() == "saturday":
            today = SATURDAY
        if day_of_the_week.lower() == "sunday":
            today = SUNDAY

        if day_of_the_week.lower() == "thurs":
            today = THURSDAY
        if day_of_the_week.lower() == "thur":
            today = THURSDAY


        if today == -1:
            print("Couldn't parse the day this shift override is for")
            print("Not changing anything....")
        else:

            if shift_start.lower() == DAY_OFF or shift_start.lower() == "off" or shift_start.lower() == "hol" or shift_start.lower() == "holiday":
                self.shift_start_times  [ today ]  = DAY_OFF
                self.shift_end_times    [ today ]  = ""
                self.break_times        [ today ]  = None
                self.break_time_lengths [ today ]  = ""
                self.lunch_times        [ today ]  = ""
                self.departments        [ today ]  = department
                self.forced_shifts      [ today ]  = True
            else:
                self.shift_start_times  [ today ]  = shift_start
                self.shift_end_times    [ today ]  = shift_end
                self.break_times        [ today ]  = None
                self.break_time_lengths [ today ]  = ""
                self.lunch_times        [ today ]  = ""
                self.departments        [ today ]  = department
                self.forced_shifts      [ today ]  = True

    def addShift( self, department, shift_start, shift_end, break_time, break_time_length, lunch_time ):
        if not isinstance(department, DepartmentHandler):
            raise TypeError("department must be a DepartmentHandler() object.")
        self.departments.append        ( department        )
        self.shift_start_times.append  ( shift_start       )
        self.shift_end_times.append    ( shift_end         )
        self.break_times.append        ( break_time        )
        self.break_time_lengths.append ( break_time_length )
        self.lunch_times.append        ( lunch_time        )

    def addDayOff( self ):
        dh = DepartmentHandler()
        self.addShift(dh, DAY_OFF, "", "", "", "")

    def addHoliday( self ):
        dh = DepartmentHandler()
        self.addShift(dh, HOLIDAY, "", "", "", "")

    def hasAForcedDepartment( self ):
        if self.forced_department == None:
            return False
        elif type(self.forced_department) == str:
            return True

    def hasAForcedDepartment( self, day_of_the_week):
        if self.forced_department == None:
            return False
        elif type(self.forced_department) == str:
            return True
        else:
            if self.hasAForcedShift( day_of_the_week ):
                # Keep the department for the forced shift, so say no to this department being forced.
                return False
            else:
                return True

    def hasAForcedShift( self, day_of_the_week ):
        if self.forced_shifts[ day_of_the_week ] == True:
            return True
        else:
            return False

    def isDayOff( self, day_of_the_week ):
        if self.shift_start_times[day_of_the_week] == DAY_OFF:
            return True
        elif self.shift_start_times[day_of_the_week] == HOLIDAY:
            return True
        else:
            return False

    def getName(self):
        return self.employee_name

    # Will return an easy to read list of departments for an employee.
    def getDepartmentsAsString(self, day_of_the_week):
        # Get all the departments and remove duplicates
        all_departments = []
        if ( self.hasAForcedDepartment( day_of_the_week ) ):
            return self.getForcedDepartment()
        else:
            for i in self.departments:
                all_departments = self.departments[ day_of_the_week ].getAllDepartmentNamesAsList()

            # Make sure the department isn't already in the list
            condensed_departments = []
            for i in all_departments:
                is_in_list = False
                for k in condensed_departments:
                    if DepartmentHandler.hasSameDepartment( k, i ):
                        is_in_list = True
                        break

                if not is_in_list:
                    condensed_departments.append( i )

            # Now convert this list to a string.
            final_string = ""
            for i in range( len(condensed_departments) ):
                if DepartmentHandler.isDepartmentTeamLeader ( condensed_departments[i] ):
                    final_string += TEAM_LEADER

                elif DepartmentHandler.isDepartmentCheckouts( condensed_departments[i] ):
                    final_string += CHECKOUTS

                elif DepartmentHandler.isDepartmentSelfScan( condensed_departments[i] ):
                    final_string += SELF_SCAN

                elif DepartmentHandler.isDepartmentKiosk    ( condensed_departments[i] ):
                    final_string += KIOSK

                elif DepartmentHandler.isDepartmentTrolleys ( condensed_departments[i] ):
                    final_string += TROLLEYS

                elif DepartmentHandler.isDepartmentDoorsteps( condensed_departments[i] ):
                    final_string += DOORSTEPS

                elif DepartmentHandler.isDepartmentCafe     ( condensed_departments[i] ):
                    final_string += CAFE

                elif DepartmentHandler.isDepartmentPetrol   ( condensed_departments[i] ):
                    final_string += PETROL
                else:
                    final_string += condensed_departments[i]

                if i < len(condensed_departments)-1:

                    final_string += " / "


            # Make the string a fixed length as when it gets too long,
            # it messes up the width of the other column and will
            # make it so that a line with a longer cashier name will then become 2 lines.
            # and that pushes everything down off the page.

            # The maximum department length I've found that can work is len("Checkouts / Customer Service - Click and Col")
            string_length = len("Checkouts / Customer Service - Click")
            temp_string = ""
            for i in range( len( final_string ) ):
                if ( ((i+1) % string_length) == 0 ):
                    temp_string += "<br>" + final_string[i]
                else:
                    temp_string +=        final_string[i]

            final_string = temp_string

            return final_string

    def getDepartments(self, day_of_the_week):
        try:
            if self.hasAForcedDepartment( day_of_the_week ):
                return DepartmentHandler( self.getForcedDepartment() )
            else:
                return self.departments[day_of_the_week]
        except:
            return None

    def getDepartmentAtHour( self, day_of_the_week, hour ):
        hour_shift_ends   = self.getHourShiftEnds( day_of_the_week )
        hour_shift_starts = self.getHourShiftStarts( day_of_the_week )
        if self.hasAForcedDepartment( day_of_the_week ):
            if (hour >= hour_shift_starts) and (hour < hour_shift_ends):
                return DepartmentHandler( self.getForcedDepartment(), self.getShiftStart( day_of_the_week ) )
            else:
                return None
        # Just use the first department we found.
        return self.departments[day_of_the_week].getDepartmentAtHour( hour, hour_shift_starts, hour_shift_ends )

    def getDepartmentAtTime( self, day_of_the_week, time ):
        time_shift_starts   = self.getShiftStart        ( day_of_the_week )
        time_shift_ends     = self.getShiftEnd          ( day_of_the_week )

        if self.hasAForcedDepartment( day_of_the_week ):
            if ( self.timeTo24Hour(time) >= self.timeTo24Hour(time_shift_starts) ) and (self.timeTo24Hour(time) < self.timeTo24Hour(time_shift_ends)):
                return DepartmentHandler( self.getForcedDepartment(), self.getShiftStart( day_of_the_week ) )
            else:
                return None
        else:
            # Just use the first department we found.
            return self.departments[day_of_the_week].getDepartmentAtHour( time, time_shift_starts, time_shift_ends )


    def getForcedDepartment( self ):
        return self.forced_department

    def getHourShiftStarts( self, day_of_the_week ):
        return int( self.shift_start_times[ day_of_the_week ][:2] )
    def getMinuteShiftStarts( self, day_of_the_week ):
        return int( self.shift_start_times[ day_of_the_week ][3:] )

    def getHourShiftEnds( self, day_of_the_week ):
        hour_shift_ends = int( self.shift_end_times[ day_of_the_week ][:2] )
        if hour_shift_ends == 0:
            hour_shift_ends = 24
        return hour_shift_ends

    def getMinuteShiftEnds( self, day_of_the_week ):
        return int( self.shift_end_times[ day_of_the_week ][3:] )

    def getShiftStart( self, day_of_the_week ):
        return self.shift_start_times[day_of_the_week]

    def getShiftEnd( self, day_of_the_week ):
        shift_end = self.shift_end_times[day_of_the_week]

        return shift_end

    def getShiftLengthAsString( self, day_of_the_week ):
        shift_start = self.getShiftStart(day_of_the_week)
        shift_end   = self.getShiftEnd(day_of_the_week)

        result =  BreaksManager.getShiftLengthAsString( shift_start, shift_end )
        return result

    def getBreakTime( self, day_of_the_week ):
        if len(self.break_times) > day_of_the_week:
            if self.break_times[ day_of_the_week ]:
                return self.break_times[ day_of_the_week ]
        else:
            return None

    def getBreakTimeAsString( self, day_of_the_week ):
        # Convert the break time to a string and return it.

        break_time = ""
        if len(self.break_times) > day_of_the_week:
            if self.break_times[ day_of_the_week ] != None:
                break_time = ( self.break_times[ day_of_the_week ].strftime( "%H:%M" ) )
            else:
                break_time = ""
        else:
            break_time = ""

        return break_time

    def getBreakTimeLength( self, day_of_the_week ):
        return self.break_time_lengths[day_of_the_week]

    def getLunchTime( self, day_of_the_week ):
        return self.lunch_times[day_of_the_week]

    def setBreakTime( self, break_time, day_of_the_week ):
        if len(self.break_times) > day_of_the_week:
            self.break_times[ day_of_the_week ] = break_time

    def setForcedDepartment( self, department ):
        self.forced_department = department

    def printShift(self, day_of_the_week ):
        #print("Mon 28/09/20 - 10:00 - 15:00")
        print( "employee_name      : " + self.employee_name )
        print( "departments        : " )
        print( self.departments[day_of_the_week].getAllDepartmentNamesAsList() )
        print( "shift_start_times  : " + self.shift_start_times[day_of_the_week] )
        print( "shift_end_times    : " + self.shift_end_times[day_of_the_week] )
        print()
        print()



    def printAllShifts(self):
        for i in range( len(self.shift_start_times) ):
            self.printShift( i )

