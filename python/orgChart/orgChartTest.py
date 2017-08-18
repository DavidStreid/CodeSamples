import unittest
from util import Util
from orgChart import OrgChart
from employee import Employee

class OrgChartTest(unittest.TestCase):

    trace = True

    def getOrgChart(self):
        employeeInput = Util.processFile("employees.txt")
        employeeData = Util.createEmployeeObjects(employeeInput)
        headManagers = Util.findSupervisorRelations(employeeData)
        orgChart = OrgChart(employeeData, headManagers)  
        orgChart.setLogging(True)
        return orgChart

    def testPrintOrgChart(self):
        if(self.trace):
            print "\n***************************\nTESTING - testPrintOrgChart\n***************************"

        orgChart = self.getOrgChart()
        output = orgChart.printOrgChart()
        test = "Laks [Dev, SF]\n\tAvi [Dev, SF]\n\t\tDave [Dev, Canada]\n\t\tRam [Dev, SF]\n\tGlynn [Dev, SF]\n\t\tDD [Dev, SF]\n\t\t\tHari [Dev, India]\n\t\tJin [Dev, SF]\n\tLaura [Dev, Canada]\n"
        self.assertEqual(output,test)

        if(self.trace):
            print output

    def testAddNewEmployee(self):
        if(self.trace):
            print "\n***************************\nTESTING - testAddNewEmployee\n***************************"

        orgChart = self.getOrgChart()
        if(self.trace):
            print orgChart.printOrgChart()

        # Adding new headManager and supervised employee
        orgChart.addNewEmployee("Heather","Heather","Dev","SF",set([]))
        orgChart.addNewEmployee("David","Heather","Dev","SF",set([]))
        output = orgChart.printOrgChart()
        test = "Heather [Dev, SF]\n\tDavid [Dev, SF]\nLaks [Dev, SF]\n\tAvi [Dev, SF]\n\t\tDave [Dev, Canada]\n\t\tRam [Dev, SF]\n\tGlynn [Dev, SF]\n\t\tDD [Dev, SF]\n\t\t\tHari [Dev, India]\n\t\tJin [Dev, SF]\n\tLaura [Dev, Canada]\n"
        self.assertEqual(output,test)
        if(self.trace):
            print output

        # Adding supervised employee under headManager
        orgChart.addNewEmployee("Seinfeld", "Laks", "Dev", "SF",set([]))
        output = orgChart.printOrgChart()
        test = "Heather [Dev, SF]\n\tDavid [Dev, SF]\nLaks [Dev, SF]\n\tAvi [Dev, SF]\n\t\tDave [Dev, Canada]\n\t\tRam [Dev, SF]\n\tGlynn [Dev, SF]\n\t\tDD [Dev, SF]\n\t\t\tHari [Dev, India]\n\t\tJin [Dev, SF]\n\tLaura [Dev, Canada]\n\tSeinfeld [Dev, SF]\n"
        self.assertEqual(output,test)
        if(self.trace):
            print output

        try:
            orgChart.addNewEmployee("Laks","Laks","Dev","SF",set([]))
        except ValueError as ve:
            if(self.trace):
                print ve

        try: 
            orgChart.addNewEmployee("McGee","Bob","Dev","SF",set([]))
        except ValueError as ve:
            if(self.trace):
                print ve

    def testRemoveEmployee(self):
        if(self.trace):
            print "\n***************************\nTESTING - testRemoveEmployee\n***************************"

        orgChart = self.getOrgChart()
        if(self.trace):
            print orgChart.printOrgChart()

        orgChart.removeEmployee("Avi")
        output = orgChart.printOrgChart()
        test = "Laks [Dev, SF]\n\tDave [Dev, Canada]\n\tGlynn [Dev, SF]\n\t\tDD [Dev, SF]\n\t\t\tHari [Dev, India]\n\t\tJin [Dev, SF]\n\tLaura [Dev, Canada]\n\tRam [Dev, SF]\n"
        self.assertEqual(output,test)
        if(self.trace):
            print output

        orgChart.removeEmployee("DD")
        output = orgChart.printOrgChart()
        test = "Laks [Dev, SF]\n\tDave [Dev, Canada]\n\tGlynn [Dev, SF]\n\t\tHari [Dev, India]\n\t\tJin [Dev, SF]\n\tLaura [Dev, Canada]\n\tRam [Dev, SF]\n"
        self.assertEqual(output,test)
        if(self.trace):
            print output

        orgChart.removeEmployee("Laks")
        output = orgChart.printOrgChart()
        test = "Dave [Dev, Canada]\nGlynn [Dev, SF]\n\tHari [Dev, India]\n\tJin [Dev, SF]\nLaura [Dev, Canada]\nRam [Dev, SF]\n"
        self.assertEqual(output,test)
        if(self.trace):
            print output

        try:
            orgChart.removeEmployee("Bob")
        except ValueError as ve:
            if(self.trace):
                print ve

    def testReAssignEmployee(self):
        if(self.trace):
            print "\n***************************\nTESTING - testReAssignEmployee\n***************************"

        orgChart = self.getOrgChart()
        if(self.trace):
            print orgChart.printOrgChart()

        # TEST CASE 1: HM to employee in supervised chain
        orgChart.reAssignEmployee("Laks", "DD")
        output = orgChart.printOrgChart()
        test ="DD [Dev, SF]\n\tHari [Dev, India]\n\tLaks [Dev, SF]\n\t\tAvi [Dev, SF]\n\t\t\tDave [Dev, Canada]\n\t\t\tRam [Dev, SF]\n\t\tGlynn [Dev, SF]\n\t\t\tJin [Dev, SF]\n\t\tLaura [Dev, Canada]\n"
        self.assertEqual(output,test)
        if(self.trace):
            print output

        # TEST CASE 2: emp to employee in supervised chain
        orgChart.reAssignEmployee("Laks","Dave")
        output = orgChart.printOrgChart()
        test = "DD [Dev, SF]\n\tDave [Dev, Canada]\n\t\tLaks [Dev, SF]\n\t\t\tAvi [Dev, SF]\n\t\t\t\tRam [Dev, SF]\n\t\t\tGlynn [Dev, SF]\n\t\t\t\tJin [Dev, SF]\n\t\t\tLaura [Dev, Canada]\n\tHari [Dev, India]\n"
        self.assertEqual(output,test)
        if(self.trace):
            print output

        # TEST CASE 3 - emp to employee immediately below in supervised chain
        orgChart.reAssignEmployee("Laks","Avi")
        test = "DD [Dev, SF]\n\tDave [Dev, Canada]\n\t\tAvi [Dev, SF]\n\t\t\tLaks [Dev, SF]\n\t\t\t\tGlynn [Dev, SF]\n\t\t\t\t\tJin [Dev, SF]\n\t\t\t\tLaura [Dev, Canada]\n\t\t\tRam [Dev, SF]\n\tHari [Dev, India]\n"
        output = orgChart.printOrgChart()
        self.assertEqual(output,test)
        if(self.trace):
            print output

        # TEST CASES 4 - emp to emp
        orgChart.reAssignEmployee("Jin","Laura")
        output = orgChart.printOrgChart()
        test = "DD [Dev, SF]\n\tDave [Dev, Canada]\n\t\tAvi [Dev, SF]\n\t\t\tLaks [Dev, SF]\n\t\t\t\tGlynn [Dev, SF]\n\t\t\t\tLaura [Dev, Canada]\n\t\t\t\t\tJin [Dev, SF]\n\t\t\tRam [Dev, SF]\n\tHari [Dev, India]\n"
        self.assertEqual(output,test)
        if(self.trace):
            print output

        orgChart.reAssignEmployee("Laura","Ram")
        output = orgChart.printOrgChart()
        test = "DD [Dev, SF]\n\tDave [Dev, Canada]\n\t\tAvi [Dev, SF]\n\t\t\tLaks [Dev, SF]\n\t\t\t\tGlynn [Dev, SF]\n\t\t\tRam [Dev, SF]\n\t\t\t\tLaura [Dev, Canada]\n\t\t\t\t\tJin [Dev, SF]\n\tHari [Dev, India]\n"
        self.assertEqual(output,test)
        if(self.trace):
            print output

        orgChart.reAssignEmployee("Laks","Hari")
        output = orgChart.printOrgChart()
        test = "DD [Dev, SF]\n\tDave [Dev, Canada]\n\t\tAvi [Dev, SF]\n\t\t\tRam [Dev, SF]\n\t\t\t\tLaura [Dev, Canada]\n\t\t\t\t\tJin [Dev, SF]\n\tHari [Dev, India]\n\t\tLaks [Dev, SF]\n\t\t\tGlynn [Dev, SF]\n"
        self.assertEqual(output,test)
        if(self.trace):
            print output

        # TEST CASE 5: HM to employee not in supervised chain
        orgChart.reAssignEmployee("DD","Hari")
        test = "Hari [Dev, India]\n\tDD [Dev, SF]\n\t\tDave [Dev, Canada]\n\t\t\tAvi [Dev, SF]\n\t\t\t\tRam [Dev, SF]\n\t\t\t\t\tLaura [Dev, Canada]\n\t\t\t\t\t\tJin [Dev, SF]\n\tLaks [Dev, SF]\n\t\tGlynn [Dev, SF]\n"
        output = orgChart.printOrgChart()
        self.assertEqual(output,test)
        if(self.trace):
            print output

        # TEST CASE 6: employee to HM
        orgChart.reAssignEmployee("DD","DD")
        output = orgChart.printOrgChart()
        test = "DD [Dev, SF]\n\tDave [Dev, Canada]\n\t\tAvi [Dev, SF]\n\t\t\tRam [Dev, SF]\n\t\t\t\tLaura [Dev, Canada]\n\t\t\t\t\tJin [Dev, SF]\nHari [Dev, India]\n\tLaks [Dev, SF]\n\t\tGlynn [Dev, SF]\n"
        self.assertEqual(output,test)
        if(self.trace):
            print output

        # TEST CASE 7: employee in supervised chain to HM
        orgChart.reAssignEmployee("Avi","Avi")
        test = "Avi [Dev, SF]\n\tRam [Dev, SF]\n\t\tLaura [Dev, Canada]\n\t\t\tJin [Dev, SF]\nDD [Dev, SF]\n\tDave [Dev, Canada]\nHari [Dev, India]\n\tLaks [Dev, SF]\n\t\tGlynn [Dev, SF]\n"
        output = orgChart.printOrgChart()
        self.assertEqual(output,test) 
        if(self.trace):
            print output

        # TEST CASE 8: employee to employee
        orgChart.reAssignEmployee("Dave","Laks")
        output = orgChart.printOrgChart()
        test = "Avi [Dev, SF]\n\tRam [Dev, SF]\n\t\tLaura [Dev, Canada]\n\t\t\tJin [Dev, SF]\nDD [Dev, SF]\nHari [Dev, India]\n\tLaks [Dev, SF]\n\t\tDave [Dev, Canada]\n\t\tGlynn [Dev, SF]\n"
        self.assertEqual(output,test) 
        if(self.trace):
            print output

        try:
            orgChart.reAssignEmployee("Bob","Dave")
        except ValueError as ve:
            if(self.trace):
                print ve
        try:
            orgChart.reAssignEmployee("Dave","Bob")
        except ValueError as ve:
            if(self.trace):
                print ve
        try:
            orgChart.reAssignEmployee("Hari","Hari")
        except ValueError as ve:
            if(self.trace):
                print ve

    def testRemoveReassign(self):
        if(self.trace):
            print "\n***************************\nTESTING - testRemoveReassign\n***************************"

        orgChart = self.getOrgChart()
        if(self.trace):
            print orgChart.printOrgChart()

        orgChart.removeEmployee("Avi")
        if(self.trace):
            print orgChart.printOrgChart()
            
        orgChart.reAssignEmployee("Glynn","Laura")
        output = orgChart.printOrgChart()
        test = "Laks [Dev, SF]\n\tDave [Dev, Canada]\n\tLaura [Dev, Canada]\n\t\tGlynn [Dev, SF]\n\t\t\tDD [Dev, SF]\n\t\t\t\tHari [Dev, India]\n\t\t\tJin [Dev, SF]\n\tRam [Dev, SF]\n"
        self.assertEqual(output,test)      
        if(self.trace):
            print output  

    def testAddRemove(self):
        if(self.trace):
            print "\n***************************\nTESTING - testAddRemove\n***************************"

        orgChart = self.getOrgChart()
        if(self.trace):
            print orgChart.printOrgChart()

        orgChart.addNewEmployee("Jon","Glynn","Dev","SF",set([]))
        if(self.trace):
            print orgChart.printOrgChart()

        orgChart.removeEmployee("Glynn")
        output = orgChart.printOrgChart()
        test = "Laks [Dev, SF]\n\tAvi [Dev, SF]\n\t\tDave [Dev, Canada]\n\t\tRam [Dev, SF]\n\tDD [Dev, SF]\n\t\tHari [Dev, India]\n\tJin [Dev, SF]\n\tJon [Dev, SF]\n\tLaura [Dev, Canada]\n"
        self.assertEqual(output,test)    
        if(self.trace):
            print output  

    def testAddReassignRemove(self):
        if(self.trace):
            print "\n***************************\nTESTING - testAddReassignRemove\n***************************"

        orgChart = self.getOrgChart()
        if(self.trace):
            print orgChart.printOrgChart()

        orgChart.addNewEmployee("Jon","Glynn","Dev","SF",set([]))
        if(self.trace):
            print orgChart.printOrgChart()

        orgChart.reAssignEmployee("Jon","Laks")
        if(self.trace):
            print orgChart.printOrgChart()

        orgChart.removeEmployee("Laks")
        output = orgChart.printOrgChart()
        test = "Avi [Dev, SF]\n\tDave [Dev, Canada]\n\tRam [Dev, SF]\nGlynn [Dev, SF]\n\tDD [Dev, SF]\n\t\tHari [Dev, India]\n\tJin [Dev, SF]\nJon [Dev, SF]\nLaura [Dev, Canada]\n"
        self.assertEqual(output,test)
        if(self.trace):
            print output  

class UtilTest(unittest.TestCase):
    def testProcessFile(self):
        employeeInput = Util.processFile("employees.txt")
        expectedEmployeeInput = ['DD,Glynn,Dev,SF', 'Avi,Laks,Dev,SF', 'Dave,Avi,Dev,Canada', 'Hari,DD,Dev,India', 'Jin,Glynn,Dev,SF', 'Ram,Avi,Dev,SF', 'Laks,Laks,Dev,SF', 'Glynn,Laks,Dev,SF', 'Laura,Laks,Dev,Canada']
        self.assertEqual(employeeInput,expectedEmployeeInput)

    def testFindSupervisorRelations(self):
        expectedHeadManagers = set(['Laks'])
        expectedSupToEmp = {'Glynn': set(['Jin', 'DD']), 'Hari': set([]), 'Jin': set([]), 'DD': set(['Hari']), 'Ram': set([]), 'Laura': set([]), 'Dave': set([]), 'Avi': set(['Dave', 'Ram']), 'Laks': set(['Laura', 'Glynn', 'Avi'])}        

        employeeData = {}
        employeeData['DD'] = Employee('DD', 'Glynn', 'Dev', 'SF', set(['Hari']))
        employeeData['Avi'] = Employee('Avi', 'Laks', 'Dev', 'SF', set(['Dave','Ram']))
        employeeData['Dave'] = Employee('Dave', 'Avi', 'Dev', 'Canada', set([]))
        employeeData['Hari'] = Employee('Hari', 'DD', 'Dev', 'India', set([]))
        employeeData['Jin'] = Employee('Jin', 'Glynn', 'Dev', 'SF', set([]))
        employeeData['Ram'] = Employee('Ram', 'Avi', 'Dev', 'SF', set([]))
        employeeData['Laks'] = Employee('Laks', 'Laks', 'Dev', 'SF', set(['Avi','Glynn','Laura']))
        employeeData['Glynn'] = Employee('Glynn', 'Laks', 'Dev', 'SF', set(['DD','Jin']))
        employeeData['Laura'] = Employee('Laura', 'Laks', 'Dev', 'Canada', set([]))

        headManagers = Util.findSupervisorRelations(employeeData)
        self.assertEqual(expectedHeadManagers,headManagers)

    def testCreateEmployeeObjects(self):
        employeeInput = ['Avi,Laks,Dev,SF', 'Dave,Avi,Dev,Canada', 'Ram,Avi,Dev,SF', 'Laks,Laks,Dev,SF']
        employeeData = Util.createEmployeeObjects(employeeInput)

        expectedEmployeeData = {}
        expectedEmployeeData['Dave'] = Employee('Dave', 'Avi', 'Dev', 'Canada', set([]))
        expectedEmployeeData['Laks'] = Employee('Laks', 'Laks', 'Dev', 'SF', set(['Avi']))
        expectedEmployeeData['Ram'] = Employee('Ram', 'Avi', 'Dev', 'SF', set([]))
        expectedEmployeeData['Avi'] = Employee('Avi', 'Laks', 'Dev', 'SF', set(['Dave','Ram']))
        
        for name,emp in employeeData.iteritems():
            expectedEmp = expectedEmployeeData[name]
            self.assertEqual(expectedEmp.get_name(),emp.get_name())
            self.assertEqual(expectedEmp.get_manager(),emp.get_manager())
            self.assertEqual(expectedEmp.get_title(),emp.get_title())
            self.assertEqual(expectedEmp.get_location(),emp.get_location())   

if __name__== '__main__':
    unittest.main()