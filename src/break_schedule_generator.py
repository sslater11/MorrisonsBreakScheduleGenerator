#!/usr/bin/env python3

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

version = "1.1.4"

# Change Log
# v1.1.4 - Added self scan as it's own separate table.
#        - Fixed a bug with the relief's departments showing wrong.
# v1.1.3 - Fixed a bug where it didn't add people to the rota if they had no task assigned to themselves.
# v1.1.2 - Made shift override include departments too so now we can set anyone's shift to anywhere.
# v1.1.1 - Added the gaps manager to output any gaps that we have.

# v1.1.0 - fixed a minor bug with windows's date formatting.
#        - removed the doorstep marshal, as it's no longer used

# v1.0.9 - Added Door marshal space, lots of other small changes, like it's now portrait.

# v1.0.8 - Fixed a bug
#        - Added the linux command line to send the break schedule file to my phone.
#        - Added the linux command to send my shifts to the clipboard.

# v1.0.7 - Added reliefs and managers on a second page.

# v1.0.6 - Added code to load Chrome manually, since the webbrowser library didn't work.

# v1.0.5 - Added copyright information
#         - Made it work with chrome's saved html files.

# v1.0.4 - Experimenting with the css, and updated the html.

# v1.0.3 - Made the ability to force someone on to a department using config files.
#
# v1.0.2 - Added my own very basic breaks manager.
#         - It only calculates the break as being in the middle of the shift right now.
#         - Hooked it up to the html, so it displays my break times,
#         - instead of showing the rubbish ones generated from the original system.

# v1.0.1 - Added command line arguments to pass a file to it, which is just much better.
#        - Made colours print in chrome
#        - Added blank lines to the table, because they're useful.
#        - Finally managed to figure out how to get rid of the table borders that are used for the layout.

# v1.0 - fixed Adam's Numbers by making it a more basic way of counting people on our department.
#        it now ignores when they change department on the same shift, because the new system doesn't handle that too well.

import sys
import os
import platform
import webbrowser
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
from datetime import date
import subprocess
import shutil
import math

from adams_numbers import AdamsNumbers
from department_handler import DepartmentHandler
from gap import Gap
from gaps_manager import GapsManager
from constants import *
from employee_handler import isEmployeeInList
from employee_handler import _getEmployeesFromFile
from my_html import MyHTML
from my_html_table import MyHTMLTable
from employee import Employee
from breaks_manager import BreaksManager

clipboard_contents = ""

class ForcedDepartment:
    def __init__( self, department, employee_name ):
        self.department = department
        self.employee_name = employee_name

    def getName( self ):
        return self.employee_name

    def getDepartment( self ):
        return self.department
class ForcedShift:
    def __init__( self, employee_name, department, day_of_the_week, shift_start, shift_end ):
        self.employee_name   = employee_name
        self.department      = department
        self.day_of_the_week = day_of_the_week
        self.shift_start     = shift_start
        self.shift_end       = shift_end

    def getName( self ):
        return self.employee_name

    def getDepartment( self ):
        return self.department

    def getDayOfWeek( self ):
        return self.day_of_the_week

    def getShiftStart( self ):
        return self.shift_start

    def getShiftEnd( self ):
        return self.shift_end




# This will return a list of employees who are working on the day and department that is passed.
def getWorkingEmployees(all_employees, department, day_of_week):
    all_working_employees = []
    for employee in all_employees:
        if not employee.isDayOff(day_of_week):

            # Test if there has been an exception to move this employee to another department.
            # Sometimes we need to move someone to another department(Checkouts, Petrol, Kiosk, Team Leader).
            if employee.hasAForcedDepartment( day_of_week ):
                if DepartmentHandler.hasSameDepartment( employee.getForcedDepartment(), department ):
                    all_working_employees.append( employee )

            elif DepartmentHandler.isDepartmentSelfScan(department)  and  DepartmentHandler.isDepartmentSelfScan ( employee.getDepartments(day_of_week) ):
                all_working_employees.append( employee )

            elif DepartmentHandler.isDepartmentCheckouts(department) and  DepartmentHandler.isDepartmentCheckouts( employee.getDepartments(day_of_week) ) and (not DepartmentHandler.isDepartmentSelfScan(employee.getDepartments(day_of_week)) ):
                all_working_employees.append( employee )

            elif DepartmentHandler.isDepartmentTeamLeader(department)  and  DepartmentHandler.isDepartmentTeamLeader ( employee.getDepartments(day_of_week) ):
                all_working_employees.append( employee )

            elif DepartmentHandler.isDepartmentKiosk(department)  and  DepartmentHandler.isDepartmentKiosk ( employee.getDepartments(day_of_week) ):
                all_working_employees.append( employee )

            elif DepartmentHandler.isDepartmentPetrol(department)  and  DepartmentHandler.isDepartmentPetrol ( employee.getDepartments(day_of_week) ):
                all_working_employees.append( employee )

            elif DepartmentHandler.isDepartmentCafe(department)    and  DepartmentHandler.isDepartmentCafe ( employee.getDepartments(day_of_week) ):
                all_working_employees.append( employee )

            elif DepartmentHandler.isDepartmentDoorsteps(department)    and  DepartmentHandler.isDepartmentDoorsteps ( employee.getDepartments(day_of_week) ):
                all_working_employees.append( employee )

    return all_working_employees

def getWorkingReliefs( all_employees, list_of_reliefs, day_of_week ):
    all_reliefs = []
    for relief in all_employees:
        if isEmployeeInList( relief, list_of_reliefs ):
            if not relief.isDayOff( day_of_week ):
                all_reliefs.append( relief )

    return all_reliefs



# This will change "Smith, John" to "John Smith"
# It will return None if passed a None argument.
def convertToCorrectEmployeeNameFormat( employee_name ):
    if isinstance(employee_name, str):
        # Get their name
        # Change the naming format to an easier to read one.
        # It's currently "Smith, John", which is horrible to read.
        # Change it to "John Smith" by splitting it at the comma, reversing the list and joining with a space.
        employee_name = employee_name.strip()
        employee_name = employee_name.split(",")
        employee_name.reverse()
        employee_name = " ".join(employee_name)
        employee_name = employee_name.strip()
        #print( "******************************** " + employee_name + " ********************************" )

        return employee_name
    elif employee_name == None:
        return None
    else:
        raise TypeError("Must pass a string. Passed: " + str(type(employee_name)) )

def help():
    if has_help_been_displayed == False:
        print("The only arguments are --print-shifts \"Write employees name here as appears on sheet\"")
        print("e.g. this_app --print-shifts \"Simon Slater\" \"Employee Weekly Schedule.html\"")
        print("")
        print("Or we can pass just the html file")
        print("e.g. this_app \"Employee Weekly Schedule.html\"")
        print("")
        print("")
        print("")
        print("")
        print("""Please pass the html file that contains our table with employees in it.""")


# ##########################
# --- Main program start ---
# ##########################

is_print_shift             = True
is_sending_file_to_android = False
is_copying_to_clipboard    = False
is_info_shown              = True
has_help_been_displayed    = False

file_path = ""
if len(sys.argv) == 2:
    file_path = sys.argv[1]
elif len( sys.argv ) == 4:
    if sys.argv[1] == "--print-shifts":
        is_print_shift = True
        print_employee_name = sys.argv[2]
        file_path = sys.argv[3]
    else:
        print("You didn't pass the only argument --print-shifts")
        help()
        exit(1)

else:
    help()
    exit(1)

if not os.path.exists( file_path ):
    print("Couldn't open file \"" + file_path + "\"")
    print()
    help()
    exit(1)


if is_info_shown:
    print ("Loading...")

# Load the list of employees with departments we have overridden.

forced_departments = []

if not os.path.exists( DEPARTMENT_OVERRIDE_FILE_PATH ):
    print("Couldn't open file \"" + DEPARTMENT_OVERRIDE_FILE_PATH + "\"")
    print("We can't override anyone's department, because the file with overrides doesn't exist.")
else:
    file = open(DEPARTMENT_OVERRIDE_FILE_PATH, "r")
    for line in file:
        line = line.strip()
        if (line != "") and (len(line) > 0):
            if line[0] != "#":
                employee_name, department = line.split("=")

                employee_name = employee_name.strip()
                department    = department.strip()

                forced_departments.append( ForcedDepartment( department, employee_name ) )

# Load the list of employees with shifts we have overridden.
forced_shifts = []

if not os.path.exists( SHIFTS_OVERRIDE_FILE_PATH ):
    print("Couldn't open file \"" + SHIFTS_OVERRIDE_FILE_PATH + "\"")
    print("We can't override anyone's shifts, because the file with overrides doesn't exist.")
else:
    file = open(SHIFTS_OVERRIDE_FILE_PATH, "r")
    for line in file:
        line = line.strip()
        if (line != "") and (len(line) > 0):
            if line[0] != "#":
                if len(line.split("\t")) == 4:
                    # Only got 4 arguments, so it's probably a line like this
                    # Simon Slater    mon   off
                    employee_name, department, day, shift_start = line.split("\t")
                    shift_end = ""
                elif len(line.split("\t")) == 5:
                    employee_name, department, day, shift_start, shift_end = line.split("\t")
                else:
                    print("Error parsing line in shifts override!!!")
                    continue

                employee_name = employee_name.strip()
                day           = day.strip()
                department    = department.strip()
                shift_start   = shift_start.strip()
                shift_end     = shift_end.strip()

                forced_shifts.append( ForcedShift( employee_name, department, day, shift_start, shift_end ) )



if is_info_shown:
    print("Reading html file.")
html_contents = Path(file_path).read_text()

if is_info_shown:
    print("Cleaning up the html.")


# Convert the file into a readable format
# For some reason, saving as a single webpage using chrome adds some junk to the html that breaks it.
# So we need to remove it to restore it to proper html.

# We need to remove
# =09
# =20
# =\n that's an equals sign followed by a new line.
#
# and change
# =3D to =
html_contents = html_contents.replace('=09', '')
html_contents = html_contents.replace('=20', '')
html_contents = html_contents.replace('=\n', '')
html_contents = html_contents.replace('=3D', '=')


if is_info_shown:
    print("Parsing HTML")
soup = BeautifulSoup(html_contents, 'html.parser')


# Get this string from the page "Week Of 31 Aug , 2020"
str_date = soup.find('span', attrs={'class' : 'calendarDateLabel pointer ng-binding'})
str_date = str_date.text.strip()
str_date = str_date[8:]
# sometimes the date is like this "Week of 31 Aug , 2020"
# and other times it is like this "Week of 31 Aug, 2020"
# so just replace the comma with a space, then just remove all duplicate spaces.
str_date = str_date.replace(", ", " ")
# Do this a few times to remove the duplicates, just in case.
str_date = str_date.replace("  ", " ")
str_date = str_date.replace("  ", " ")
str_date = str_date.replace("  ", " ")
str_date = str_date.replace("  ", " ")

# We're left with "31 Aug 2020"
week_commencing_date = datetime.strptime(str_date, '%d %b %Y')

all_employees = []


def getOriginalDepartment( employee_shifts ):
    # Go up 2 levels to get to the div tag which has the group they belong to.
    #print( employee_shifts.parent.parent)

    original_department = employee_shifts.parent.parent
    original_department = d.find('div').attrs["id"]


if is_info_shown:
    print("Extracting everyone's shifts.")

# Loop through all employees and add their shifts.
for employee_shifts in soup.findAll('tbody'):
    # See what department this employee is underneath
    #for i in employee_shifts.findAll('td', attrs={'class': 'storeNameContainer'}):
    #    print( "--- Department: " + i.text.strip() + " ---")

    employee_name = employee_shifts.find('td', attrs={'class': 'employeeNameContainer'})
    if employee_name != None:
        ###Get the department they belong to.
        ### It's in a div tag outside of this scope, so use parent to look out far enough to get this employee's department.

        ###d = employee_name.previous_element.previous_element.previous_element.previous_element.previous_element.previous_element.previous_element.previous_element.previous_element.previous_element.previous_element.previous_element
        #d = employee_name.parent.parent.parent.parent.parent
        ##print(d.find('div'))
        ##print(d.find('div').attrs)
        ##print(d.find('div').attrs["id"])
        ###d = d.find('div')
        ####d = d.findAll('td', attrs={'class': 'storeNameContainer'})
        ###for i in d:
        ###    print(i)
        #print( employee_shifts.parent.parent)
        #getOriginalDepartment( employee_shifts )

        #exit(1)


        # Change the naming format to an easier to read one.
        # Change it from "Smith, John" to "John Smith"
        str_employee_name = convertToCorrectEmployeeNameFormat( employee_name.text )
        current_employee = Employee( str_employee_name )


        day_of_week = 0
        for shift in employee_shifts.findAll('td'):
            table_cells_class_tag = shift.get('class')

            #print(table_cells_class_tag)
            if table_cells_class_tag == None:
                # Do nothing
                pass

            # They are working this day
            elif "contentRow-store-td" in table_cells_class_tag:
                #print("#### " + DAYS_OF_THE_WEEK[day_of_week] + " ####" )

                shift_details = shift.findAll('tr')

                # See if it's their day off.
                # Check if it's a single table row
                # Then check if it's empty, meaning a day off.
                if len( shift_details) == 1 :
                    # If it's an empty cell, then it's a day off.
                    if( len(shift_details[0].text.strip()) ) == 0:
                        #print( "Day Off" )
                        current_employee.addDayOff()
                else:
                    # They're working, so extract the deets.
                    departments       = DepartmentHandler() # A list of DepartmentHandler objects
                    shift_start       = ""
                    shift_end         = ""
                    break_time        = ""
                    break_time_length = ""
                    lunch_time        = ""

                    is_day_off = False
                    for i in range(len(shift_details)):
                        # Remove all the junk whitespace from it.
                        shift_details_text = shift_details[i].text.strip()
                        shift_details_text = shift_details_text.replace("\n", "")
                        shift_details_text = shift_details_text.replace("\t", "")
                        # Get their starting and ending shift times.
                        if i == 0:
                            # Check if they've transferred to another store...
                            if "Transferred" in shift_details_text:
                                is_day_off = True
                                # Skip to the next shift
                                break
                            current_shift = shift_details_text[:SHIFT_TIMESTAMP_LENGTH]
                            shift_start = current_shift.split("-")[0].strip()
                            shift_end   = current_shift.split("-")[1].strip()

                            # Get the length of their break, since it's included in the shift starting and ending times.
                            if "Meal" in shift_details_text:
                                break_time_length = shift_details_text[SHIFT_TIMESTAMP_LENGTH:]
                                break_time_length = break_time_length.replace("(Meal : ", "")
                                break_time_length = break_time_length.replace(")", "")
                            else:
                                break_time_length = ""
                        else:
                            # Check if this is their break time
                            if "Unpaid Break" in shift_details_text:
                                # It's formatted like this "08:00 Unpaid Break"
                                # So just get the time from it.
                                #print ("Unpaid Break at: " + shift_details_text[:5])
                                #break_time = shift_details_text[:5]

                                # Do nothing, we will calculate breaks ourselves at a later date.
                                pass
                            elif "Lunch Break" in shift_details_text:
                                # It's formatted like this "08:00 Lunch Break"
                                # So just get the time from it.
                                #print ("Lunch Break at: " + shift_details_text[:5])
                                #lunch_time = shift_details_text[:5]

                                # Do nothing, we will calculate breaks ourselves at a later date.
                                pass
                            #elif "No Task" in shift_details_text:
                                # Do nothing
                                pass
                            elif "Paid Break" in shift_details_text:
                                # Do nothing, because a paid break is only for managers.
                                pass
                            else:
                                # All other sections are for what department the person is working on.
                                # It's formatted like this "08:15 Bakery", so separate it first.
                                department_name = shift_details_text[6:]
                                department_time = shift_details_text[:5]

                                # Loop through the list of overridden departments and see if this person has one.
                                has_added_department = False
                                for i in forced_departments:
                                    name_1 = i.getName().lower()
                                    name_2 = current_employee.getName().lower()
                                    if name_1 == name_2:
                                        has_added_department = True
                                        if current_employee.forced_department == None:
                                            current_employee.setForcedDepartment( i.getDepartment() )
                                            print( "overriding for: " + current_employee.getName() + " with department " + i.getDepartment() )
                                            break

                                # Not overriding the department, so add the one from the table.
                                if has_added_department == False:
                                    if "No Task" in shift_details_text:
                                        # Their department was just blank, so don't add them.
                                        #departments.addDepartment( department_name, department_time )
                                        pass
                                    else:
                                        departments.addDepartment( department_name, department_time )
                    # End of for loop

                    # Add the shift
                    if is_day_off:
                        current_employee.addDayOff()
                    else:
                        current_employee.addShift( departments, shift_start, shift_end, break_time, break_time_length, lunch_time )

                day_of_week = day_of_week + 1
            elif "collapseContainer" in shift.get('class'):
                # Do nothing
                # This is the empty cell in the table before the main data, so ignore it.
                pass
            elif "totalsContainer" in shift.get('class'):
                # Do nothing
                # This is the cell in the table that contains the total hours worked.
                pass
            elif "dayOff-store-td" in table_cells_class_tag:
                current_employee.addDayOff()
                day_of_week = day_of_week + 1
            elif "terminated_shift_row" in table_cells_class_tag:
                current_employee.addDayOff()
                day_of_week = day_of_week + 1
            elif "inactive_shift_row" in table_cells_class_tag:
                current_employee.addDayOff()
                day_of_week = day_of_week + 1
            elif "Non_homeStoreRow-store-td" in table_cells_class_tag:
                current_employee.addDayOff()
                day_of_week = day_of_week + 1

        # Finally add them to the list :)
        all_employees.append( current_employee )



# We have all the employees shifts extracted.


# Override employee's shifts
for i in forced_shifts:
    for k in range(len(all_employees)):
        if i.getName().lower() == all_employees[k].getName().lower():
            print("Warning!")
            print("Overriding shift!")
            print( i.getName() + ", " + i.getDepartment() + ", " + i.getDayOfWeek() + ", " + i.getShiftStart() + ", " + i.getShiftEnd() )
            all_employees[k].forceShift( i.getDepartment(), i.getDayOfWeek(), i.getShiftStart(), i.getShiftEnd() )
            break
        else:
            if k == len(all_employees)-1:
                print( "couldn't find a match for this shift override" )
                print( i.getName() + ", " + i.getDepartment() + ", " + i.getDayOfWeek() + ", " + i.getShiftStart() + ", " + i.getShiftEnd() )


# Make a list of all departments found assigned to their shifts.
print("A list of all departments:")
list_of_all_departments = []
for employee in all_employees:
    for day in range(7):
        employees_departments = employee.getDepartments( day )
        if ( employees_departments != None ):
            for i in employees_departments.getAllDepartmentNamesAsList():
                    if not (i in list_of_all_departments):
                        list_of_all_departments.append( i )

for i in list_of_all_departments:
    print( i )
    print(   )


list_of_reliefs  = _getEmployeesFromFile( RELIEFS_FILE_PATH  )
list_of_managers = _getEmployeesFromFile( MANAGERS_FILE_PATH )



### Generate the html output ###
# Creates the html tables and the A4 pages.

my_html = MyHTML()
# Now find out who is in each day.
all_gaps = []
for day_of_the_week in range(7):
    # Get the week commencing date, and increment it by x days.

    all_cashiers       = getWorkingEmployees( all_employees, CHECKOUTS,        day_of_the_week )
    if( IS_SCO_SEPERATE ):
        all_sco            = getWorkingEmployees( all_employees, SELF_SCAN,        day_of_the_week )
    all_self_isolating = getWorkingEmployees( all_employees, SELF_ISOLATING,   day_of_the_week )
    all_cafe           = getWorkingEmployees( all_employees, CAFE,             day_of_the_week )
    all_cash_office    = getWorkingEmployees( all_employees, CASH_OFFICE,      day_of_the_week )
    all_team_leaders   = getWorkingEmployees( all_employees, TEAM_LEADER,      day_of_the_week )
    if day_of_the_week == 0:
        for i in all_team_leaders:
            i.printShift(0)
    all_kiosk          = getWorkingEmployees( all_employees, KIOSK,            day_of_the_week )
    all_doorsteps      = getWorkingEmployees( all_employees, DOORSTEPS,        day_of_the_week )
    all_car_park       = getWorkingEmployees( all_employees, CAR_PARK,         day_of_the_week )
    all_trolleys       = getWorkingEmployees( all_employees, TROLLEYS,         day_of_the_week )
    all_petrol         = getWorkingEmployees( all_employees, PETROL,           day_of_the_week )
    all_reliefs        = getWorkingReliefs  ( all_employees, list_of_reliefs,  day_of_the_week )
    all_managers       = getWorkingReliefs  ( all_employees, list_of_managers, day_of_the_week )

    # Add all cashiers to the break scheduler
    bm = BreaksManager(all_cashiers, day_of_the_week)
    # Update all cashier's breaks to the newly generated ones.
    for i in range( len( all_cashiers ) ):
        break_time = bm.getBreakTime( all_cashiers[i], day_of_the_week )
        all_cashiers[i].setBreakTime( break_time, day_of_the_week )

    if( IS_SCO_SEPERATE ):
        # Add all sco to the break scheduler
        bm = BreaksManager(all_sco, day_of_the_week)
        # Update all sco breaks to the newly generated ones.
        for i in range( len( all_sco ) ):
            break_time = bm.getBreakTime( all_sco[i], day_of_the_week )
            all_sco[i].setBreakTime( break_time, day_of_the_week )

    # Add all kiosk to the break scheduler
    bm = BreaksManager(all_kiosk, day_of_the_week)
    # Update all kiosk breaks to the newly generated ones.
    for i in range( len( all_kiosk ) ):
        break_time = bm.getBreakTime( all_kiosk[i], day_of_the_week )
        all_kiosk[i].setBreakTime( break_time, day_of_the_week )

    # Add all petrol to the break scheduler
    bm = BreaksManager(all_petrol, day_of_the_week)
    # Update all petrol breaks to the newly generated ones.
    for i in range( len( all_petrol ) ):
        break_time = bm.getBreakTime( all_petrol[i], day_of_the_week )
        all_petrol[i].setBreakTime( break_time, day_of_the_week )


    adams_numbers = AdamsNumbers()
    adams_numbers.add( "C",  all_cashiers,     DepartmentHandler(CHECKOUTS,   ""), day_of_the_week )
    if( IS_SCO_SEPERATE ):
        adams_numbers.add( "S",  all_sco,          DepartmentHandler(SELF_SCAN,   ""), day_of_the_week )
    adams_numbers.add( "TL", all_team_leaders, DepartmentHandler(TEAM_LEADER, ""), day_of_the_week )
    adams_numbers.add( "K",  all_kiosk,        DepartmentHandler(KIOSK,       ""), day_of_the_week )
    adams_numbers.add( "P",  all_petrol,       DepartmentHandler(PETROL,      ""), day_of_the_week )
    adams_numbers.addOthersFromList( "R", all_reliefs, day_of_the_week )


    gaps = GapsManager()
    gaps.add( week_commencing_date, all_cashiers,     DepartmentHandler(CHECKOUTS,   ""), day_of_the_week )
    if( IS_SCO_SEPERATE ):
        gaps.add( week_commencing_date, all_sco,          DepartmentHandler(SELF_SCAN,   ""), day_of_the_week )
    gaps.add( week_commencing_date, all_team_leaders, DepartmentHandler(TEAM_LEADER, ""), day_of_the_week )
    gaps.add( week_commencing_date, all_kiosk,        DepartmentHandler(KIOSK,       ""), day_of_the_week )
    #gaps.add( week_commencing_date, all_doorsteps,    DepartmentHandler(DOORSTEPS,   ""), day_of_the_week )
    gaps.add( week_commencing_date, all_petrol,       DepartmentHandler(PETROL,      ""), day_of_the_week )
    all_gaps += [ gaps ]

    #action_list = ActionList()
    #action_list.addEmployees( "Cashiers",       all_cashiers,     day_of_the_week )
    ##action_list.addEmployees( "Team Leaders", all_team_leaders, day_of_the_week )
    #action_list.addEmployees( "Kiosk",        all_kiosk,        day_of_the_week )
    ##action_list.addEmployees( "Petrol",       all_petrol,       day_of_the_week )
    #action_list.sort()

    cashier_html_table = MyHTMLTable("Cashiers")
    for i in all_cashiers:
        # Table layout
        # Name | Till Number | Shift Start | Shift End | Departments | Break Time | Break Time Length| Lunch Time
        name              = i.getName()
        shift_start       = i.getShiftStart          ( day_of_the_week )
        shift_end         = i.getShiftEnd            ( day_of_the_week )
        shift_length      = i.getShiftLengthAsString ( day_of_the_week )
        departments       = i.getDepartmentsAsString ( day_of_the_week )
        break_time        = i.getBreakTimeAsString   ( day_of_the_week )
        break_time_length = i.getBreakTimeLength     ( day_of_the_week )
        lunch_time        = i.getLunchTime           ( day_of_the_week )

        cashier_html_table.addLine(name, shift_start, shift_end, shift_length, departments, break_time, break_time_length, lunch_time)
    cashier_html_table.sort()
    # Blank lines so we can add people manually.
    cashier_html_table.addLine("&nbsp;", "", "", "", "", "", "", "")
    cashier_html_table.addLine("&nbsp;", "", "", "", "", "", "", "")
    cashier_html_table.addLine("&nbsp;", "", "", "", "", "", "", "")
    cashier_html_table.addLine("&nbsp;", "", "", "", "", "", "", "")
    cashier_html_table.addLine("&nbsp;", "", "", "", "", "", "", "")
    cashier_html_table.addLine("&nbsp;", "", "", "", "", "", "", "")

    if( IS_SCO_SEPERATE ):
        sco_html_table = MyHTMLTable("Self Scan")
        for i in all_sco:
            # Table layout
            # Name | Till Number | Shift Start | Shift End | Departments | Break Time | Break Time Length| Lunch Time
            name              = i.getName()
            shift_start       = i.getShiftStart          ( day_of_the_week )
            shift_end         = i.getShiftEnd            ( day_of_the_week )
            shift_length      = i.getShiftLengthAsString ( day_of_the_week )
            departments       = i.getDepartmentsAsString ( day_of_the_week )
            break_time        = i.getBreakTimeAsString   ( day_of_the_week )
            break_time_length = i.getBreakTimeLength     ( day_of_the_week )
            lunch_time        = i.getLunchTime           ( day_of_the_week )

            sco_html_table.addLine(name, shift_start, shift_end, shift_length, departments, break_time, break_time_length, lunch_time)
        sco_html_table.sort()

    self_isolating_html_table = MyHTMLTable("Self Isolating", is_smaller_font=False)
    for i in all_self_isolating:
        # Table layout
        # Name | Shift Start | Shift End | Departments | Break Time | Break Time Length| Lunch Time
        name              = i.getName()
        shift_start       = i.getShiftStart          ( day_of_the_week )
        shift_end         = i.getShiftEnd            ( day_of_the_week )
        shift_length      = i.getShiftLengthAsString ( day_of_the_week )
        departments       = i.getDepartmentsAsString ( day_of_the_week )
        break_time        = i.getBreakTimeAsString   ( day_of_the_week )
        break_time_length = i.getBreakTimeLength     ( day_of_the_week )
        lunch_time        = i.getLunchTime           ( day_of_the_week )

        self_isolating_html_table.addLine(name, shift_start, shift_end, shift_length, departments, break_time, break_time_length, lunch_time, include_till_column=False)

    self_isolating_html_table.sort()

    team_leaders_html_table = MyHTMLTable("Team Leaders")
    for i in all_team_leaders:
        # Table layout
        # Name | Shift Start | Shift End | Departments | Break Time | Break Time Length| Lunch Time
        name              = i.getName()
        shift_start       = i.getShiftStart          ( day_of_the_week )
        shift_end         = i.getShiftEnd            ( day_of_the_week )
        shift_length      = i.getShiftLengthAsString ( day_of_the_week )
        departments       = i.getDepartmentsAsString ( day_of_the_week )
        break_time        = i.getBreakTimeAsString   ( day_of_the_week )
        break_time_length = i.getBreakTimeLength     ( day_of_the_week )
        lunch_time        = i.getLunchTime           ( day_of_the_week )

        team_leaders_html_table.addLine(name, shift_start, shift_end, shift_length, departments, break_time, break_time_length, lunch_time, include_till_column=False)

    team_leaders_html_table.sort()

    cash_office_html_table = MyHTMLTable("Office2", is_smaller_font=True)
    for i in all_cash_office:
        # Table layout
        # Name | Shift Start | Shift End | Departments | Break Time | Break Time Length| Lunch Time
        name              = i.getName()
        shift_start       = i.getShiftStart          ( day_of_the_week )
        shift_end         = i.getShiftEnd            ( day_of_the_week )
        shift_length      = i.getShiftLengthAsString ( day_of_the_week )
        departments       = i.getDepartmentsAsString ( day_of_the_week )
        break_time        = i.getBreakTimeAsString   ( day_of_the_week )
        break_time_length = i.getBreakTimeLength     ( day_of_the_week )
        lunch_time        = i.getLunchTime           ( day_of_the_week )

        cash_office_html_table.addLine(name, shift_start, shift_end, shift_length, departments, break_time, break_time_length, lunch_time, include_till_column=True)

    cash_office_html_table.sort()


    cafe_html_table = MyHTMLTable("Cafe")
    for i in all_cafe:
        # Table layout
        # Name | Shift Start | Shift End | Departments | Break Time | Break Time Length| Lunch Time
        name              = i.getName()
        shift_start       = i.getShiftStart          ( day_of_the_week )
        shift_end         = i.getShiftEnd            ( day_of_the_week )
        shift_length      = i.getShiftLengthAsString ( day_of_the_week )
        departments       = i.getDepartmentsAsString ( day_of_the_week )
        break_time        = i.getBreakTimeAsString   ( day_of_the_week )
        break_time_length = i.getBreakTimeLength     ( day_of_the_week )
        lunch_time        = i.getLunchTime           ( day_of_the_week )

        cafe_html_table.addLine(name, shift_start, shift_end, shift_length, departments, break_time, break_time_length, lunch_time, include_till_column=True)

    cafe_html_table.sort()

    kiosk_html_table = MyHTMLTable("Kiosk")
    for i in all_kiosk:
        # Table layout
        # Name | Shift Start | Shift End | Departments | Break Time | Break Time Length| Lunch Time
        name              = i.getName()
        shift_start       = i.getShiftStart          ( day_of_the_week )
        shift_end         = i.getShiftEnd            ( day_of_the_week )
        shift_length      = i.getShiftLengthAsString ( day_of_the_week )
        departments       = i.getDepartmentsAsString ( day_of_the_week )
        break_time        = i.getBreakTimeAsString   ( day_of_the_week )
        break_time_length = i.getBreakTimeLength     ( day_of_the_week )
        lunch_time        = i.getLunchTime           ( day_of_the_week )

        kiosk_html_table.addLine(name, shift_start, shift_end, shift_length, departments, break_time, break_time_length, lunch_time, include_till_column=False)

    kiosk_html_table.sort()

    car_park_html_table = MyHTMLTable("Car Park")
    for i in all_car_park:
        # Table layout
        # Name | Shift Start | Shift End | Departments | Break Time | Break Time Length| Lunch Time
        name              = i.getName()
        shift_start       = i.getShiftStart          ( day_of_the_week )
        shift_end         = i.getShiftEnd            ( day_of_the_week )
        shift_length      = i.getShiftLengthAsString ( day_of_the_week )
        departments       = i.getDepartmentsAsString ( day_of_the_week )
        break_time        = i.getBreakTimeAsString   ( day_of_the_week )
        break_time_length = i.getBreakTimeLength     ( day_of_the_week )
        lunch_time        = i.getLunchTime           ( day_of_the_week )

        car_park_html_table.addLine(name, shift_start, shift_end, shift_length, departments, break_time, break_time_length, lunch_time, include_till_column=False)

    doorsteps_html_table = MyHTMLTable("Doorsteps")
    for i in all_doorsteps:
        # Table layout
        # Name | Shift Start | Shift End | Departments | Break Time | Break Time Length| Lunch Time
        name              = i.getName()
        shift_start       = i.getShiftStart          ( day_of_the_week )
        shift_end         = i.getShiftEnd            ( day_of_the_week )
        shift_length      = i.getShiftLengthAsString ( day_of_the_week )
        departments       = i.getDepartmentsAsString ( day_of_the_week )
        break_time        = i.getBreakTimeAsString   ( day_of_the_week )
        break_time_length = i.getBreakTimeLength     ( day_of_the_week )
        lunch_time        = i.getLunchTime           ( day_of_the_week )

        doorsteps_html_table.addLine(name, shift_start, shift_end, shift_length, departments, break_time, break_time_length, lunch_time, include_till_column=False)

    doorsteps_html_table.sort()

    petrol_html_table = MyHTMLTable("Petrol", is_smaller_font=True)
    for i in all_petrol:
        # Table layout
        # Name | Shift Start | Shift End | Departments | Break Time | Break Time Length| Lunch Time
        name              = i.getName()
        shift_start       = i.getShiftStart          ( day_of_the_week )
        shift_end         = i.getShiftEnd            ( day_of_the_week )
        shift_length      = i.getShiftLengthAsString ( day_of_the_week )
        departments       = i.getDepartmentsAsString ( day_of_the_week )
        break_time        = i.getBreakTimeAsString   ( day_of_the_week )
        break_time_length = i.getBreakTimeLength     ( day_of_the_week )
        lunch_time        = i.getLunchTime           ( day_of_the_week )

        petrol_html_table.addLine(name, shift_start, shift_end, shift_length, departments, break_time, break_time_length, lunch_time, include_till_column=False)
    petrol_html_table.sort()

    reliefs_html_table = MyHTMLTable("Reliefs")
    for i in all_reliefs:
        # Table layout
        # Name | Shift Start | Shift End | Departments | Break Time | Break Time Length| Lunch Time
        name              = i.getName()
        shift_start       = i.getShiftStart          ( day_of_the_week )
        shift_end         = i.getShiftEnd            ( day_of_the_week )
        shift_length      = i.getShiftLengthAsString ( day_of_the_week )
        departments       = i.getDepartmentsAsString ( day_of_the_week )
        break_time        = i.getBreakTimeAsString   ( day_of_the_week )
        break_time_length = i.getBreakTimeLength     ( day_of_the_week )
        lunch_time        = i.getLunchTime           ( day_of_the_week )

        reliefs_html_table.addLine(name, shift_start, shift_end, shift_length, departments, break_time, break_time_length, lunch_time, include_till_column=False)
    reliefs_html_table.sort()

    managers_html_table = MyHTMLTable("Managers")
    for i in all_managers:
        # Table layout
        # Name | Shift Start | Shift End | Departments | Break Time | Break Time Length| Lunch Time
        name              = i.getName()
        shift_start       = i.getShiftStart          ( day_of_the_week )
        shift_end         = i.getShiftEnd            ( day_of_the_week )
        shift_length      = i.getShiftLengthAsString ( day_of_the_week )
        departments       = i.getDepartmentsAsString ( day_of_the_week )
        break_time        = i.getBreakTimeAsString   ( day_of_the_week )
        break_time_length = i.getBreakTimeLength     ( day_of_the_week )
        lunch_time        = i.getLunchTime           ( day_of_the_week )

        managers_html_table.addLine(name, shift_start, shift_end, shift_length, departments, break_time, break_time_length, lunch_time, include_till_column=False)
    managers_html_table.sort()

    current_date = week_commencing_date + timedelta(days = day_of_the_week)

    # Create the main break schedule page.
    my_html.addHTML("""    <!-- Each sheet element should have the class "sheet" -->
    <!-- "padding-**mm" is optional: you can set 10, 15, 20 or 25 -->
    <section class="sheet padding-10mm">
    <!-- Write HTML just like a web page -->
""")

    my_html.addHTML("""<page size="A4">""")
    my_html.addHTML( """
<table class="mainLayout" width=100%>
<thead></thead>
<tbody>
    <tr>
    <td style="width:100%">""")

    my_html.addDate      ( current_date                )
    if( not gaps.isEmpty() ):
        my_html.addHTMLTable ( gaps )
        my_html.addHTML      ( "            <br>" )

    my_html.addHTMLTable ( cashier_html_table )
    my_html.addHTML      ( "            <p>&nbsp;</p>" )
    if( IS_SCO_SEPERATE ):
        if( sco_html_table.getLineCount() >= 1 ):
            my_html.addHTMLTable ( sco_html_table   )
            my_html.addHTML      ( "            <br>"          )
    my_html.addHTML("""

    </td>
    <td style="width:auto%">"""                        )

    my_html.addHTMLTable ( adams_numbers               )
    #my_html.addHTML("<p font-size=\"" + FONT_SIZE_ADAMS_NUMBERS + "px\">Generated on<br>" + date.today().strftime( "%a %d %b %y" ) + "<br>at " + datetime.now().strftime( "%H:%M:%S" ) + "</p>" )
    my_html.addHTML("<p align=\"center\" style=\"font-size: " + FONT_SIZE_ADAMS_NUMBERS + "px\">Break schedule<br>generated on<br>" + date.today().strftime( "%a %d %b %y" ) + "<br>at " + datetime.now().strftime( "%H:%M:%S" ) + "</p>" )
    my_html.addHTML("""
    </td>
    </tr>""")

# Used this to make the next row a new table, used it with doormarshall showing on the right.
#    my_html.addHTML( """
#</tbody></table>
#<table class="mainLayout" width=100%>
#<thead></thead>
#<tbody>""")

    my_html.addHTML ("""
    <tr>
    <td style="width:100%">""")
    if( self_isolating_html_table.getLineCount() >= 1 ):
        my_html.addHTMLTable ( self_isolating_html_table   )
        my_html.addHTML      ( "            <br>"          )
    my_html.addHTMLTable ( team_leaders_html_table     )
    my_html.addHTML      ( "            <br>"          )
    my_html.addHTMLTable ( kiosk_html_table            )
    my_html.addHTML      ( "            <br>"          )
    my_html.addHTMLTable ( car_park_html_table         )
    my_html.addHTML      ( "            <br>"          )
    #my_html.addHTMLTable ( doorsteps_html_table        )
    #my_html.addHTML      ( "            <br>"          )
    #my_html.addHTMLTable ( cash_office_html_table             )
    #my_html.addHTML      ( "            <br>"          )
    my_html.addHTMLTable ( petrol_html_table           )
    my_html.addHTML("""
    <td style="width:auto%">"""                        )

    # No longer using the action list, as it's not any use. The break schedule changes way too much for it to work.
   #my_html.addHTMLTable ( action_list             )

    # close the table on the page.
    my_html.addHTML("""
    </td>
    </tr>
</tbody></table>""")

    # Start a new page
    my_html.addHTML("""    </section>""")


    # Make the reliefs and manager's page
    my_html.addHTML("""    <!-- Each sheet element should have the class "sheet" -->
    <!-- "padding-**mm" is optional: you can set 10, 15, 20 or 25 -->
    <section class="sheet padding-10mm">
    <!-- Write HTML just like a web page -->
""")
    my_html.addHTML("""<page size="A4">""")
    my_html.addHTML( """
<table class="mainLayout" width=100%>
<thead></thead>
<tbody>
    <tr>
    <td>""")
    my_html.addDate      ( current_date            )
    my_html.addHTMLTable ( managers_html_table )
    my_html.addHTML      ( "            <p>&nbsp;</p>"   )
    my_html.addHTMLTable ( reliefs_html_table      )
    my_html.addHTML      ( "            <br>"          )
    my_html.addHTMLTable ( cafe_html_table             )
    my_html.addHTML("""
    </td>
    </tr>
</tbody></table>""")
    my_html.addHTML("""    </section>""")


html_output = my_html.getHTML()



# Write the html to a file.
str_output_filename = week_commencing_date.strftime( "%Y-%m-%d-Break-Schedule.html" )
output_html_file = os.path.dirname( os.path.abspath(script_path) )
output_html_file = os.path.join(output_html_file, str_output_filename)
with open(output_html_file, 'w') as f:
    f.write( html_output )



print()
print( "---------- All the gaps found ----------" )
print()
# surround with backticks for whatsapp pasting as monospace :)
clipboard_contents += "```Gaps:"
#print( all_gaps.toString() )
for i in range( len(all_gaps) ):
    if all_gaps[i].toString() != "":
        print( all_gaps[i].toString() )
        clipboard_contents += "\n" + all_gaps[i].toString()
#clipboard_contents += all_gaps.toString()
clipboard_contents += "```\n"
print( "----------------------------------------" )
print()

if is_print_shift:
    try:
        str_shifts = ""
        for i in all_employees:
            print_employee_name = print_employee_name.strip().lower()
            employee_name = i.getName().strip().lower()

            total_hours_worked = None
            if print_employee_name == employee_name:
                print( i.getName() )
                for day_of_the_week in range(7):
                    current_date = week_commencing_date + timedelta(days = day_of_the_week)
                    shift_start = i.getShiftStart( day_of_the_week )
                    shift_end   = i.getShiftEnd  ( day_of_the_week )



                    # 02/Sep - Mon - 7-7

                    str_current_shift = current_date.strftime( '%d/%b - %a - ' )
                    print( i.getDepartmentsAsString( day_of_the_week ) )
                    if shift_start == "Day Off":
                        str_current_shift = str_current_shift + shift_start
                    else:
                        str_current_shift = str_current_shift + shift_start + " - " + shift_end

                        if total_hours_worked == None:
                            total_hours_worked = BreaksManager.getShiftLength( shift_start, shift_end )
                        else:
                            total_hours_worked += BreaksManager.getShiftLength( shift_start, shift_end )

                    str_shifts += str_current_shift + "\n"
                hours = math.trunc(total_hours_worked.total_seconds()/60/60)
                real_hours = total_hours_worked.total_seconds()/60/60
                minutes = math.trunc((real_hours - hours) * 60)

                str_shifts += "Total: " + str(hours) + "h " + str(minutes) + "m\n"
        print( str_shifts )

        if is_copying_to_clipboard:
            str_shifts = str_shifts.replace("\n","\\n")
            clipboard_contents += str_shifts
    except Exception:
        pass

if is_copying_to_clipboard:
    subprocess.Popen( [sys.path[0] + "/copy_to_clipboard.sh", clipboard_contents ] )

# This is just for me on linux.
# It'll send the break schedule to my phone, so I can share it with everyone.
if is_sending_file_to_android:
    try:
        command_1 = "kdeconnect-cli -d 81030ac220f205d9 --share ".split()
        command_2 = "kdeconnect-cli -d 6e497038e95a4324 --share ".split()
        subprocess.run( command_1 + [ str(output_html_file) ] )
        subprocess.run( command_2 + [ str(output_html_file) ] )
    except Exception:
        pass


# Open the page in a web browser.
did_browser_run = False

# This prints what webbrowsers we can load.
print("Available browsers")
print (webbrowser._tryorder)

# Test if we have chrome.
if not did_browser_run:
    try:
        if "windows" in platform.system().lower():
            chromepath = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
            subprocess.run( [chromepath, output_html_file] )
            chromepath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
            subprocess.run( [chromepath, output_html_file] )
        else:
            # Try on linux
            webbrowser.get("chrome").open( output_html_file )
        did_browser_run = True
    except:
        pass
        print( "No chrome browser found" )

# Test if we have firefox.
if not did_browser_run:
    try:
        if platform.system() == "Windows":
            ffpath = 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'
            ffpath = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
            #print( webbrowser._tryorder )
            webbrowser.register('firefox', None, webbrowser.GenericBrowser(ffpath))
            #print( webbrowser._tryorder )
            ff = webbrowser.get('firefox')
            ff.open( output_html_file )
        else:
            # Try on linux
            webbrowser.get("firefox").open( output_html_file )

        did_browser_run = True
    except:
        pass
        print( "No firefox browser found" )

# Test if we have windows, and get the default browser.
if not did_browser_run:
    try:
        webbrowser.get("windows-default").open( output_html_file )
        did_browser_run = True
    except:
        pass
        print( "No default windows browser found" )

if not did_browser_run:
    print( "No web browsers were found, so we can't automatically load it for you" )
    print("Manually open file " + str(output_html_file))
    exit(1)


# Cleanup the folder that is created by firefox when we download the html.
firefox_junk_directory = file_path.replace(".html", "_files")
if os.path.exists( firefox_junk_directory ):
    print( "Cleaning up left over files..." )
    try:
        shutil.rmtree( firefox_junk_directory )
    except:
        pass

