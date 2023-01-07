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

from datetime import datetime
from datetime import timedelta
import platform

# This will calculate the best time to send someone for their break.
# There are several rules that need to be applied to calculae breaks appropriately.

# We should send someone for their 15m/30m break in the middle of their shift, to split their day up evenly.

# We must try to never overlap any breaks, so only one cashier is on a break at any time.

# shorter shifts have higher priority, because there's less time to get their breaks in.
# e.g. a seven hour shift and 4 hour shift, the 4 hour needs their break first, because there's only 2 hours leeway on each side of the break.

# We fit hour breaks in last, because it's much easier to work out the smaller breaks, and move them about if we need to, or delay an hour break by 15m.

# We must count how many people are working too, because we shouldn't send someone for a break at 3pm if we lose 2 cashiers then, instead, send them at 2:45, so by the time they come back from their 15m break, they will be back in time for losing 2 members of staff.
# Also, why send someone for a break at 9:45 when at 10am we gain 3 members of staff and have no more breaks.
# It needs to scan ahead and behind by a small amount to see when is the best time to send someone :).

# We need to pass a list of cashiers with their starting and ending times, so just pass the cashiers list.
# We will then need a new list of breaks for everyone, and also for their lunch.
# 
# We need to get the number of cashiers at their break time, and see if moving them forward or backwards by 15-30 minutes works out better, because we have more people in, meaning it's easier to cover them.
class Break:
    def __init__( self, employee_name, break_time, lunch_time ):
        self.employee_name = employee_name
        self.break_time = break_time
        self.lunch_time = lunch_time

    def getBreakTime( self ):
        return self.break_time

    def getLunchTime( self ):
        return self.break_time

    def getName( self ):
        return self.employee_name

    def setBreakTime( self, break_time ):
        self.break_time = break_time

class BreaksManager:
    def __init__( self, employees, day_of_the_week ):
        self.employees = employees
        self.day_of_the_week = day_of_the_week
        self.calculated_breaks = []

        self.calculateBreaks()
        #self.spreadOutBreaks()

        # Next need to check if a break lies at a time when we have fewer cashiers. Check both before and after the break to see if we can move it in either direction.
        # We also need to do this with groups of breaks too.
        # Scan through breaks that are after eachother, and see if moving them forward or back will be better. Also see which way lies closest to the middle of everyone's shift.

        # Need to make the spread out breaks count for 30 minutes.
        self.moveBreaksToBetterTime()

    def getBreakTime(self, employee, day_of_the_week):
        for i in self.calculated_breaks:
            if i.getName() == employee.getName():
                return i.getBreakTime()
        return None


    @staticmethod
    def getShiftLength( shift_start, shift_end ):
        shift_start = datetime.strptime(shift_start, '%H:%M')
        shift_end   = datetime.strptime(shift_end,   '%H:%M')

        # convert it all to time deltas for easy maths.
        delta_shift_start = timedelta(hours=shift_start.hour, minutes=shift_start.minute)
        delta_shift_end   = timedelta(hours=shift_end.hour,   minutes=shift_end.minute)

        if (delta_shift_start > delta_shift_end):
            # They must be on a night shift, as they finish later than they start.
            twenty_four_hours = timedelta(days=1)
            shift_length = (twenty_four_hours - delta_shift_start) + delta_shift_end
        else:
            shift_length = delta_shift_end - delta_shift_start

        return shift_length

    @staticmethod
    def getShiftLengthAsString( shift_start, shift_end ):
        shift_length = BreaksManager.getShiftLength( shift_start, shift_end )

        # Convert the timedelta to a datetime.
        result = datetime.strptime(str(shift_length), "%H:%M:%S")

        if platform.system() == "Linux":
            # Linux requires the dashes to make it a 9h and not 09h.
            # return as a string like "9h 30m"
            return result.strftime("%-Hh %-Mm")
        if "windows" in platform.system().lower():
            # return as a string like "9h 30m"
            return result.strftime("%Hh %Mm")
        else:
            # not sure what platform, so do this.
            # sometimes windows doesn't return "Windows"
            # return as a string like "9h 30m"
            return result.strftime("%Hh %Mm")

    # This will round to the nearest 15 minutes, with a tendancy to round down more than up.
    @staticmethod
    def roundMinutes( mins ):
        # Round the minutes to the nearest 15.
        # Notice the <=7.5 will mean it'll round down slightly more often.
        if   ( mins >= 0    ) and ( mins <= 7.5  ):
            mins = 0

        elif ( mins >= 7.5  ) and ( mins <= 15   ):
            mins = 15

        elif ( mins >= 15   ) and ( mins <= 22.5 ):
            mins = 15

        elif ( mins >= 22.5 ) and ( mins <= 30   ):
            mins = 30

        elif ( mins >= 30   ) and ( mins <= 37.5 ):
            mins = 30

        elif ( mins >= 37.5 ) and ( mins <= 45   ):
            mins = 45

        elif ( mins >= 45   ) and ( mins <= 52.5 ):
            mins = 45

        elif ( mins >= 52.5 ) and ( mins <= 60   ):
            mins = 60

        return mins


    def halveShiftLength( self, shift_length ):
        # get the hours and minutes.
        totsec = shift_length.total_seconds()
        h = totsec//3600
        m = (totsec%3600) // 60
        s =(totsec%3600)%60

        # Halve the shift.
        h = h / 2
        m = m / 2

        # Make it 0, 15, 45, 60 minutes.
        m = BreaksManager.roundMinutes( m )

        half_of_shift_length = timedelta(hours=h, minutes=m)

        return half_of_shift_length

    # This function calculates the break time by just setting it to the middle of their shift.
    # This does mean that we can end up with multiple breaks at the same time.
    def calculateBreaks( self ):
        # loop through all employees and calculate their breaks at the middle of their shift.
        for employee in self.employees:
            if not employee.isDayOff( self.day_of_the_week ):
                new_lunch = ""
                employee_name      = employee.getName()
                shift_start        = employee.getShiftStart        ( self.day_of_the_week )
                shift_end          = employee.getShiftEnd          ( self.day_of_the_week )
                break_time         = employee.getBreakTimeAsString ( self.day_of_the_week )
                break_time_length  = employee.getBreakTimeLength   ( self.day_of_the_week )
                lunch_time         = employee.getLunchTime         ( self.day_of_the_week )

                #print( employee.getName() )
                #print ( employee.getShiftStart        ( self.day_of_the_week ) )
                #print ( employee.getShiftEnd          ( self.day_of_the_week ) )
                #print ( employee.getBreakTimeAsString ( self.day_of_the_week ) )
                #print ( employee.getBreakTimeLength   ( self.day_of_the_week ) )
                #print ( employee.getLunchTime         ( self.day_of_the_week ) )

                if lunch_time == "":
                    # They have no lunch, so it's just a 15 or 30m break.
                    shift_length = BreaksManager.getShiftLength( shift_start, shift_end )

                    # Get the middle of the shift.
                    half_of_shift_length = self.halveShiftLength( shift_length )

                    new_break = datetime.strptime(shift_start, '%H:%M') + half_of_shift_length
                else:
                    new_break = "N/A: " + break_time
                    new_lunch = "N/A: " + lunch_time

                self.calculated_breaks.append( Break( employee_name, new_break, new_lunch ) )


        # These 2 notes belong to a function which will run after this.
        # Then see if their break falls at a time when we lose a cashier, if so move it to before we lose someone.
        # Also see if we can send them for a break later when we gain someone.
        pass

    # Find overlapping breaks, and spread them out by moving one to a later time.
    def spreadOutBreaks( self ):
        are_breaks_overlapping = True
        while are_breaks_overlapping:
            are_breaks_overlapping = False
            for employee_1 in range(len(self.calculated_breaks) -1):
                for employee_2 in range(employee_1 + 1, len(self.calculated_breaks)):
                    if self.calculated_breaks[employee_1].getBreakTime() == self.calculated_breaks[employee_2].getBreakTime():
                        print ()
                        print(self.calculated_breaks[employee_1].getName())
                        print(self.calculated_breaks[employee_1].getBreakTime())
                        print(self.calculated_breaks[employee_2].getName())
                        print(self.calculated_breaks[employee_2].getBreakTime())

                        # Find out which shift is longer.
                        shift_start_1 =  self.calculated_breaks[employee_1].getShiftStart()
                        shift_start_2 = self.calculated_breaks[employee_2].getShiftStart()
                        shift_end_1 = self.calculated_breaks[employee_1].getShiftEnd()
                        shift_end_2 = self.calculated_breaks[employee_2].getShiftEnd()

                        shift_length_1 = BreaksManager.getShiftLength( shift_start_1, shift_end_1 )
                        shift_length_2 = BreaksManager.getShiftLength( shift_start_2, shift_end_2 )

                        if shift_length_1 > shift_length_2:
                            # Need to move one person's break forward by 15 minutes to fix the overlap.
                            new_break_time = self.calculated_breaks[employee_1].getBreakTime() + timedelta(minutes=15)
                            self.calculated_breaks[employee_1].setBreakTime( new_break_time )
                        else:
                            new_break_time = self.calculated_breaks[break_2].getBreakTime() + timedelta(minutes=15)
                            self.calculated_breaks[break_2].setBreakTime( new_break_time )


    def moveBreaksToBetterTime( self ):
        pass
        # Loop through the breaks.
        # If we found a break that is happening when the cashier count goes down from just before or after it,
        # Move it to the more reasonable time.
        # if there's another break at that time, check if it can be moved to a time where we'll have more cashiers.
