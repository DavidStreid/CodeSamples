from employee import Employee

class Util:
    def processFile(fileName):
        """Converts file into list of employee data
        Args:
            fileName (str): Name of file to read from

        Returns:
            list: List of strings containing employee data,  [employeeName, managerName, employeeTitle, employeeLocation]
                E.g. ['DD,Glynn,Dev,SF', ...]
        """
        file = open(fileName, "r")
        employeeInput = file.read().strip().split("\n")
        return employeeInput

    def findSupervisorRelations(employeeData):
        """ Generates child links of supervisor to supervised employees and generates list of managers who report to no one, headManagers
        Args:
            employeeData (string -> Employee): dic of employee name to employee information

        Returns:
            headManagers (list): list of managers who report to no one
        """
        headManagers = set([])

        # Iterates through empName and Employee instance
        for name,emp in employeeData.iteritems():        
            manager = emp.get_manager()

            # Check if employee is head manager
            if(name==manager):
                headManagers.add(name)
            else:
                employeeData[manager].get_supervised().add(name) # Add employee to supervised list

        return headManagers

    def createEmployeeObjects(employeeInput):
        """Create dictionary of employees to their employee information
        Args:
            employeeInput (list of strings): Employee data read from file

        Returns:
            employeeData: dictionary of employee to their information
        """
        employeeData = {}
        for e in employeeInput:
            e = e.split(',') # Parse string for employee fields split on ','

            # Check for membership in orgChart, should not be the case
            name = e[0]
            if name in employeeData:
                raise ValueError("createEmployeeObjects::employeeInput has duplicate employee - %s" % name)

            # Add employee w/ metadata
            manager = e[1]
            title = e[2]
            location = e[3]
            supervised = set([])    # supervised relationship initialized to empty set

            employeeData[name] = Employee(name,manager,title,location,supervised)

        return employeeData

    # Make methods static
    processFile = staticmethod(processFile)
    findSupervisorRelations = staticmethod(findSupervisorRelations)
    createEmployeeObjects = staticmethod(createEmployeeObjects)
