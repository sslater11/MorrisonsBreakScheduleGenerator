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
class DepartmentHandler:
    def __init__( self, department=None, department_time=None ):
        self.departments      = []
        self.department_times = []

        if (not (department == None)) and (not (department_time == None)):
            if isinstance(department, str) and isinstance(department_time, str):
                self.addDepartment( department, department_time )
            else:
                raise TypeError("Must pass a string as the department and another as the department_time.")

    def addDepartment( self, department, department_time):
        if isinstance(department, str) and isinstance(department_time, str):
            self.departments.append     ( department      )
            self.department_times.append( department_time )
        else:
            raise TypeError("Must pass 2 strings like this addDepartment('Bakery', '13:15').")


    # Can be passed a string or a DepartmentHandler Object.
    @staticmethod
    def hasSameDepartment( first_department, second_department ):
        first_list_of_department_names = []
        second_list_of_department_names = []

        # Setup the first list of department names.
        if isinstance(first_department, str):
            first_list_of_department_names.append( first_department )

        elif isinstance(first_department, DepartmentHandler):
            first_list_of_department_names = first_department.getAllDepartmentNamesAsList()

        else:
            raise TypeError("Must pass either a string or DepartmentHandler() object.")


        # Setup the second list of department names.
        if isinstance(second_department, str):
            second_list_of_department_names.append( second_department )

        elif isinstance(second_department, DepartmentHandler):
            second_list_of_department_names = second_department.getAllDepartmentNamesAsList()

        else:
            raise TypeError("Must pass either a string or DepartmentHandler() object.")


        for i in first_list_of_department_names:
            for k in second_list_of_department_names:
                if DepartmentHandler.areDepartmentNamesSimilar(i, k):
                    return True
                elif DepartmentHandler.isDepartmentTeamLeader(i) and DepartmentHandler.isDepartmentTeamLeader( k ):
                    return True
                elif DepartmentHandler.isDepartmentCheckouts (i) and DepartmentHandler.isDepartmentCheckouts ( k ):
                    return True
                elif DepartmentHandler.isDepartmentSelfScan  (i) and DepartmentHandler.isDepartmentSelfScan  ( k ):
                    return True
                elif DepartmentHandler.isDepartmentKiosk     (i) and DepartmentHandler.isDepartmentKiosk     ( k ):
                    return True
                elif DepartmentHandler.isDepartmentTrolleys  (i) and DepartmentHandler.isDepartmentTrolleys  ( k ):
                    return True
                elif DepartmentHandler.isDepartmentPetrol    (i) and DepartmentHandler.isDepartmentPetrol    ( k ):
                    return True
                elif DepartmentHandler.isDepartmentCafe      (i) and DepartmentHandler.isDepartmentCafe      ( k ):
                    return True

        return False

    @staticmethod
    def areDepartmentNamesSimilar( department1, department2 ):
        if isinstance(department1, str) and isinstance(department2, str):
            if department1.lower() in department2.lower():
                return True
            elif department2.lower() in department1.lower():
                return True
            elif department1.lower() == department2.lower():
                return True
            else:
                # It wasnt found, so return false
                return False
        else:
            raise TypeError("department must be a string")

    @staticmethod
    def isDepartmentTeamLeader( department ):
        department_list = []
        if isinstance( department, DepartmentHandler ):
            department_list = department.getAllDepartmentNamesAsList()

        elif isinstance( department, str ):
            department_list = [department]

        else:
            raise TypeError("Not passed a string or DepartmentHandler()")

        for i in department_list:
            if DepartmentHandler.areDepartmentNamesSimilar(TEAM_LEADER, i):
                return True
            elif DepartmentHandler.areDepartmentNamesSimilar("checkout close", i):
                return True
        return False

    @staticmethod
    def isDepartmentCheckouts( department ):
        department_list = []
        if isinstance( department, DepartmentHandler ):
            department_list = department.getAllDepartmentNamesAsList()

        elif isinstance( department, str ):
            department_list = [department]

        else:
            raise TypeError("Not passed a string or DepartmentHandler()")

        for i in department_list:
            if DepartmentHandler.areDepartmentNamesSimilar(SELF_SCAN, i):
                if( IS_SCO_SEPERATE == False ):
                    return True
                else:
                    return False
            elif DepartmentHandler.areDepartmentNamesSimilar(CHECKOUTS, i):
                return True
            elif DepartmentHandler.areDepartmentNamesSimilar(TROLLEYS, i):
                return True
            elif DepartmentHandler.areDepartmentNamesSimilar("Customer Service - Marshall", i):
                return True
        return False

    @staticmethod
    def isDepartmentSelfScan( department ):
        if( IS_SCO_SEPERATE == True ):
            department_list = []
            if isinstance( department, DepartmentHandler ):
                department_list = department.getAllDepartmentNamesAsList()
            elif isinstance( department, str ):

                department_list = [department]

            else:
                raise TypeError("Not passed a string or DepartmentHandler()")

            for i in department_list:
                if DepartmentHandler.areDepartmentNamesSimilar(SELF_SCAN, i):
                    return True

        return False

    @staticmethod
    def isDepartmentKiosk( department ):
        department_list = []
        if isinstance( department, DepartmentHandler ):
            department_list = department.getAllDepartmentNamesAsList()
        elif isinstance( department, str ):

            department_list = [department]

        else:
            raise TypeError("Not passed a string or DepartmentHandler()")

        for i in department_list:
            if DepartmentHandler.areDepartmentNamesSimilar(KIOSK, i):
                return True

        return False

    @staticmethod
    def isDepartmentTrolleys( department ):
        department_list = []
        if isinstance( department, DepartmentHandler ):
            department_list = department.getAllDepartmentNamesAsList()
        elif isinstance( department, str ):

            department_list = [department]

        else:
            raise TypeError("Not passed a string or DepartmentHandler()")

        for i in department_list:
            if DepartmentHandler.areDepartmentNamesSimilar(TROLLEYS, i):
                return True

        return False

    @staticmethod
    def isDepartmentPetrol( department ):
        department_list = []
        if isinstance( department, DepartmentHandler ):
            department_list = department.getAllDepartmentNamesAsList()
        elif isinstance( department, str ):

            department_list = [department]

        else:
            raise TypeError("Not passed a string or DepartmentHandler()")

        for i in department_list:
            if DepartmentHandler.areDepartmentNamesSimilar(PETROL, i):
                return True

        return False


    @staticmethod
    def isDepartmentDoorsteps( department ):
        department_list = []
        if isinstance( department, DepartmentHandler ):
            department_list = department.getAllDepartmentNamesAsList()
        elif isinstance( department, str ):

            department_list = [department]

        else:
            raise TypeError("Not passed a string or DepartmentHandler()")

        for i in department_list:
            if DepartmentHandler.areDepartmentNamesSimilar(DOORSTEPS, i):
                return True

        return False

    @staticmethod
    def isDepartmentCafe( department ):
        department_list = []
        if isinstance( department, DepartmentHandler ):
            department_list = department.getAllDepartmentNamesAsList()
        elif isinstance( department, str ):

            department_list = [department]

        else:
            raise TypeError("Not passed a string or DepartmentHandler()")

        for i in department_list:
            if DepartmentHandler.areDepartmentNamesSimilar(CAFE, i):
                return True

        return False


    # Will return None if the hour is below their shift start time.
    # Returns a department object with just the department name.
    # This will just return the first department they've been assigned.
    # I can't seem to find a reliable way to see what department they are on,
    # because the new system is rubbish at allocating it,
    # so just go by the first department added.
    def getDepartmentAtHour( self, hour, hour_shift_starts, hour_shift_ends ):
        if len( self.departments ) == 0:
            return None
        elif (hour >= hour_shift_starts) and (hour < hour_shift_ends):
            # Just use the first department we found.
            first_department_name = self.departments[0]
            current_department      = DepartmentHandler( first_department_name, "" )
            return current_department
        else:
            return None

    # Will return None if the time is below their shift start time.
    # Returns a department object with just the department name.
    # This will just return the first department they've been assigned.
    def getDepartmentAtTime( self, current_time, time_shift_starts, time_shift_ends ):
        first_department_name = self.departments[0]

        current_department = DepartmentHandler( first_department_name, "" )

        if (current_time >= time_shift_starts) and (current_time < time_shift_ends):
            # Just use the first department we found.
            return current_department
        else:
            return None

    def getDepartment( self, index ):
        try:
            return self.departments[ index ]
        except:
            return None

    def getDepartmentTime( self, index ):
        # Department is stored like this "15:00 Checkouts"
        # Extract just the time from it.
        return self.departments[ index ][:5]

    def getAllDepartments( self ):
        all_departments = []

        for i in self.departments:
            all_departments.append( DepartmentHandler( i, "" ) )

        return all_departments

    def getAllDepartmentNamesAsList( self ):
        return self.departments

    @staticmethod
    def _get_department_hour( department ):
        return int( department[:2] )

    @staticmethod
    def _get_department_name( department ):
        return department[6:]
