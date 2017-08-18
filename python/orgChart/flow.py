if __name__ == '__main__':
    employeeData = {}       # dic of employee to metadata
    supToEmp = {}           # dic of supervisors to employees
    headManagers = set([])  # List of managers who report to no one

    orgChart = OrgChart(employeeData, supToEmp, headManagers)
    employeeInput = Util.processFile("employees.txt")

    # Create employeeData
    try:
        orgChart.employeeData = Util.createEmployeeObjects(employeeInput)
    except ValueError as ve:  # Catch case of duplicate employees in input
        print ve 

    # Find head managers and all "emp supervises emp" relations
    orgChart.headManagers, orgChart.supToEmp = Util.findSupervisorRelations(orgChart.employeeData)

    # TEST: printOrgChart
    output = orgChart.printOrgChart()
    print output
    test = "Laks [Dev, SF]\n\tAvi [Dev, SF]\n\t\tDave [Dev, Canada]\n\t\tRam [Dev, SF]\n\tGlynn [Dev, SF]\n\t\tDD [Dev, SF]\n\t\t\tHari [Dev, India]\n\t\tJin [Dev, SF]\n\tLaura [Dev, Canada]\n"
    if(test!=output):
        print "printOrgChart failed"

    # TEST: add Employee        
    try:
        orgChart.addNewEmployee("Heather","Heather","Dev","SF")
        orgChart.addNewEmployee("David","Heather","Dev","SF")
        output = orgChart.printOrgChart()
        test = "Heather [Dev, SF]\n\tDavid [Dev, SF]\nLaks [Dev, SF]\n\tAvi [Dev, SF]\n\t\tDave [Dev, Canada]\n\t\tRam [Dev, SF]\n\tGlynn [Dev, SF]\n\t\tDD [Dev, SF]\n\t\t\tHari [Dev, India]\n\t\tJin [Dev, SF]\n\tLaura [Dev, Canada]\n"
        if(test!=output):
            print "addNewEmployee failed"
    except ValueError as ve:  
        print ve 
    
    # TEST: remove Employee
    orgChart.removeEmployee("Heather")
    test = "David [Dev, SF]\nLaks [Dev, SF]\n\tAvi [Dev, SF]\n\t\tDave [Dev, Canada]\n\t\tRam [Dev, SF]\n\tGlynn [Dev, SF]\n\t\tDD [Dev, SF]\n\t\t\tHari [Dev, India]\n\t\tJin [Dev, SF]\n\tLaura [Dev, Canada]\n"
    output = orgChart.printOrgChart()
    if(test!=output):
        print "removeEmployeeFailed"

    test = "Avi [Dev, SF]\n\tDave [Dev, Canada]\n\tRam [Dev, SF]\nDavid [Dev, SF]\nGlynn [Dev, SF]\n\tDD [Dev, SF]\n\t\tHari [Dev, India]\n\tJin [Dev, SF]\nLaura [Dev, Canada]\n"
    orgChart.removeEmployee("Laks")
    output = orgChart.printOrgChart()
    if(test!=output):
        print "removeEmployeeFailed"

    # TEST: reAssignEmployee
    # Case 1: emp -> headManager
    orgChart.reAssignEmployee("Dave", "David")
    output = orgChart.printOrgChart()
    test = "Avi [Dev, SF]\n\tRam [Dev, SF]\nDavid [Dev, SF]\n\tDave [Dev, Canada]\nGlynn [Dev, SF]\n\tDD [Dev, SF]\n\t\tHari [Dev, India]\n\tJin [Dev, SF]\nLaura [Dev, Canada]\n"
    if(test!=output):
        print "reAssignEmployeeFailed - Case 1:emp->headManager"
    # Case 2: headManager -> emp
    test = "Avi [Dev, SF]\n\tRam [Dev, SF]\nGlynn [Dev, SF]\n\tDD [Dev, SF]\n\t\tHari [Dev, India]\n\tDavid [Dev, SF]\n\t\tDave [Dev, Canada]\n\tJin [Dev, SF]\nLaura [Dev, Canada]\n"
    orgChart.reAssignEmployee("David", "Glynn")
    output = orgChart.printOrgChart()
    if(test!=output):
        print "reAssignEmployeeFailed - Case 2: headManager->emp"
    # Case 3: emp -> emp
    orgChart.reAssignEmployee("Dave", "DD")
    output = orgChart.printOrgChart()
    test = "Avi [Dev, SF]\n\tRam [Dev, SF]\nGlynn [Dev, SF]\n\tDD [Dev, SF]\n\t\tDave [Dev, Canada]\n\t\tHari [Dev, India]\n\tDavid [Dev, SF]\n\tJin [Dev, SF]\nLaura [Dev, Canada]\n"
    if(test!=output):
        print "reAssignEmployeeFailed - Case 3: emp->emp"