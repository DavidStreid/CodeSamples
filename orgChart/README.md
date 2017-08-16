README.md

### TO RUN ###
$ cd /directory_of_unzipped_file
$ python orgChartTest.py

* To turn off logging of orgChartTest.py, modify trace (line 8) and logging (line 15) to false
** Input comes from "employee.txt" file which must be in same directory as orgChartTest.py

orgChart.py: implements an organizational chart with following methods
    printOrgChart:      prints organizational chart
    addNewEmployee:     adds new employee
    removeEmployee:     removes employee
    reAssignEmployee:   reAssigns employee to a different manager

employee.py: implements an instance of an Employee with fields for name, manager, role, location, and supervised employees

util.py: implements utility methods for reading in file of employee information and populating OrgChart instance with employeeData and a set of headManagers

Sample Input (E.g. employees.txt)
    DD,Glynn,Dev,SF
    Avi,Laks,Dev,SF
    Dave,Avi,Dev,Canada
    Hari,DD,Dev,India
    Jin,Glynn,Dev,SF
    Ram,Avi,Dev,SF
    Laks,Laks,Dev,SF
    Glynn,Laks,Dev,SF
    Laura,Laks,Dev,Canada

Sample Output:
    Laks [Dev, SF]
        Avi [Dev, SF]
            Dave [Dev, Canada]
            Ram [Dev, SF]
        Glynn [Dev, SF]
            DD [Dev, SF]
                Hari [Dev, India]
            Jin [Dev, SF]
        Laura [Dev, Canada]
