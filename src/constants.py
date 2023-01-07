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
import sys

DAYS_OF_THE_WEEK = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" ]
MONDAY    = 0
TUESDAY   = 1
WEDNESDAY = 2
THURSDAY  = 3
FRIDAY    = 4
SATURDAY  = 5
SUNDAY    = 6

## Font size in the html file.
#FONT_SIZE                = "11"  #"11"
FONT_SIZE                = "10"  #"11"
FONT_SIZE_SMALL          = "8"  #"11"
FONT_SIZE_ADAMS_NUMBERS  = "8"  #"11"
FONT_SIZE_ACTION_LIST    = "7"  #"11"
FONT_SIZE_DEPARTMENT     = "7"  #"11"
FONT_SIZE_TODAYS_DATE    = "22"  #"11"

#FONT_SIZE                = "9" #"11"
#FONT_SIZE_SMALL          = "7"  #"11"
#FONT_SIZE_ADAMS_NUMBERS  = "6"  #"11"
#FONT_SIZE_ACTION_LIST    = "6"  #"11"
## christmas font sizes
#FONT_SIZE                = "6" #"11"
#FONT_SIZE_SMALL          = "5"  #"11"
#FONT_SIZE_ADAMS_NUMBERS  = "6"  #"11"
#FONT_SIZE_ACTION_LIST    = "6"  #"11"

# new years font sizes
#FONT_SIZE                = "10" #"11"
#FONT_SIZE_SMALL          = "7"  #"11"
#FONT_SIZE_ADAMS_NUMBERS  = "8"  #"11"
#FONT_SIZE_ACTION_LIST    = "7"  #"11"

# Adam's Numbers min/max hour.
ADAMS_NUMBERS_EARLIEST_START =  6
ADAMS_NUMBERS_LATEST_START   = 22

### File Paths ###
script_path = os.path.dirname( sys.argv[0] )
ADAMS_NUMBERS_EXCLUSIONS_FILE_PATH = os.path.join( script_path, "config/BreakSchedule-AdamsNumbersExclusions.txt" )
DEPARTMENT_OVERRIDE_FILE_PATH      = os.path.join( script_path, "config/BreakSchedule-Department-Override.txt" )
SHIFTS_OVERRIDE_FILE_PATH          = os.path.join( script_path, "config/BreakSchedule-Shift-Override.txt" )
RELIEFS_FILE_PATH                  = os.path.join( script_path, "config/BreakSchedule-Reliefs.txt" )
MANAGERS_FILE_PATH                 = os.path.join( script_path, "config/BreakSchedule-Managers.txt" )



SHIFT_TIMESTAMP_LENGTH = 13 # Shift timestamp looks like this "07:00 - 13:30". Use this length to slice it out of a string.
DAY_OFF = "Day Off"
HOLIDAY = "Holiday"

CHECKOUTS      = "Checkouts"
SELF_SCAN      = "Self Scan"
SELF_ISOLATING = "Self Isolating"
CAFE           = "Cafe - Customer Cafe"
CASH_OFFICE    = "Price and Cash"
TEAM_LEADER    = "Team Leader"
KIOSK          = "Kiosk"
#DOORSTEPS      = "Online - Home Delivery"
DOORSTEPS      = "Customer Service - Doorstep"
CAR_PARK       = "Car Park"
TROLLEYS       = "Trolleys"
PETROL         = "Petrol"

DEPARTMENT_ACTIVE_INDEX_DEPARTMENT = 0
DEPARTMENT_ACTIVE_INDEX_DAY        = 1
DEPARTMENT_ACTIVE_INDEX_START_TIME = 2
DEPARTMENT_ACTIVE_INDEX_END_TIME   = 3




IS_SCO_SEPERATE            = False



# A list of the start - end times for when we need an employee on this department.
all_department_active_times = [
    [ CHECKOUTS,   MONDAY,    "07:00", "22:00" ],
    [ CHECKOUTS,   TUESDAY,   "07:00", "22:00" ],
    [ CHECKOUTS,   WEDNESDAY, "07:00", "22:00" ],
    [ CHECKOUTS,   THURSDAY,  "07:00", "22:00" ],
    [ CHECKOUTS,   FRIDAY,    "07:00", "22:00" ],
    [ CHECKOUTS,   SATURDAY,  "07:00", "22:00" ],
    [ CHECKOUTS,   SUNDAY,    "09:00", "16:00" ],

    [ SELF_SCAN,   MONDAY,    "09:00", "18:00" ],
    [ SELF_SCAN,   TUESDAY,   "09:00", "18:00" ],
    [ SELF_SCAN,   WEDNESDAY, "09:00", "18:00" ],
    [ SELF_SCAN,   THURSDAY,  "09:00", "18:00" ],
    [ SELF_SCAN,   FRIDAY,    "09:00", "18:00" ],
    [ SELF_SCAN,   SATURDAY,  "09:00", "18:00" ],
    [ SELF_SCAN,   SUNDAY,    "10:00", "16:00" ],

    [ TEAM_LEADER, MONDAY,    "06:45", "22:00" ],
    [ TEAM_LEADER, TUESDAY,   "06:45", "22:00" ],
    [ TEAM_LEADER, WEDNESDAY, "06:45", "22:00" ],
    [ TEAM_LEADER, THURSDAY,  "06:45", "22:00" ],
    [ TEAM_LEADER, FRIDAY,    "06:45", "22:00" ],
    [ TEAM_LEADER, SATURDAY,  "06:45", "22:00" ],
    [ TEAM_LEADER, SUNDAY,    "09:00", "17:00" ],

    [ KIOSK,       MONDAY,    "07:00", "22:00" ],
    [ KIOSK,       TUESDAY,   "07:00", "22:00" ],
    [ KIOSK,       WEDNESDAY, "07:00", "22:00" ],
    [ KIOSK,       THURSDAY,  "07:00", "22:00" ],
    [ KIOSK,       FRIDAY,    "07:00", "22:00" ],
    [ KIOSK,       SATURDAY,  "07:00", "22:00" ],
    [ KIOSK,       SUNDAY,    "09:00", "16:00" ],

    #[ DOORSTEPS,   MONDAY,    "13:00", "14:00" ],
    #[ DOORSTEPS,   TUESDAY,   "13:00", "14:00" ],
    #[ DOORSTEPS,   WEDNESDAY, "13:00", "14:00" ],
    #[ DOORSTEPS,   THURSDAY,  "13:00", "14:00" ],
    #[ DOORSTEPS,   FRIDAY,    "13:00", "14:00" ],
    #[ DOORSTEPS,   SATURDAY,  "13:00", "14:00" ],
    #[ DOORSTEPS,   SUNDAY,    "13:00", "14:00" ],

    [ PETROL,      MONDAY,    "06:00", "22:15" ],
    [ PETROL,      TUESDAY,   "06:00", "22:15" ],
    [ PETROL,      WEDNESDAY, "06:00", "22:15" ],
    [ PETROL,      THURSDAY,  "06:00", "22:15" ],
    [ PETROL,      FRIDAY,    "06:00", "22:15" ],
    [ PETROL,      SATURDAY,  "06:00", "22:15" ],
    [ PETROL,      SUNDAY,    "08:00", "20:00" ]
]
