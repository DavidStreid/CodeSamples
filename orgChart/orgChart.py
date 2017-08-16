from employee import Employee
from util import Util
import unittest

import sys # TODO - Remove

class OrgChart:
    """OrgChart Object

    Attributes:
        employeeData (dic {str -> Employee}): Dictionary tracking all employees in organization
        headManager (set): Set maintaining all managers who report to no one
        logging (boolean): Sets logging to true to print method logging to standard out
    """
    logging = True

    def __init__(self,employeeData,headManagers):
        self.employeeData = employeeData
        self.headManagers = headManagers

    def setLogging(self,logStatus):
        """ Allows logging of methods """

        self.logging = logStatus

    def printOrgChartLine(self, numIndents, emp):
        """ Returns string output of an organization chart line 
        Args:
            emp (Employee): Employee object
            numIndents (int): number of '\t' characters that should preced data when printed

        Returns: none
        """

        indent = '\t' * numIndents
        name = emp.get_name()
        loc = emp.get_location()
        title = emp.get_title()
        return ("%s%s [%s, %s]\n" % (indent,name,title,loc))

    def addSupervisedToStack(self, stack, e, numIndents):
        """ Called by printOrgChar() - Appends supervised employees in a sorted manner to the stack
        Args:
            stack (list): list of (Employee,numIndent) tuples utilized as stack
            e (string): name of employee
            numIndents (int): number of '\t' characters that should preced data when printed

        Returns: none
        """

        for e in sorted(self.employeeData[e].get_supervised(), reverse=True):
            stack.append([e,numIndents])

    def printOrgChart(self):
        """ Prints organization chart using class employeeData and headManagers objects
            Implements DFS from each employee considered to be a headManager (reports to no one)

            Returns: 
                chartOutput (string): String representation of organization chart 
        """

        chartOutput = ""    # Each line of output appended

        # Iterate through the headManagers as roots of trees
        for m in sorted(self.headManagers):
            numIndents = 0              # Track number of indents employee data should be prepended with when printed
            emp = self.employeeData[m]
            chartOutput += self.printOrgChartLine(numIndents,emp)

            # DFS of supervised employees from headManager
            stack = []
            self.addSupervisedToStack(stack, m, numIndents)
            while(stack):
                nextEmp, prevIndent = stack.pop()
                currIndent = prevIndent + 1     # Increment indent count to indicate "popped-off" employee supervises employees about to be added to stack
                chartOutput += self.printOrgChartLine(currIndent, self.employeeData[nextEmp])
                self.addSupervisedToStack(stack, nextEmp, currIndent)

        return chartOutput

    def addNewEmployee(self, empName, empManager, empTitle, empLocation,supervised):
        """ Creates Employee instance and adds it to employeeData
        Args:
            empName (str): Employee's name
            empManager (str): Employee's Manager
            empTitle (str): Employee's Title
            empLocation(str): Employee's Location
            supervised(set([str])): supervised employees
        """

        if(self.logging):
            print ("Adding %s to %s" % (empName,empManager))
        if empName in self.employeeData:
            raise ValueError("addNewEmployee::Employee already exists - %s" % empName)
        if empManager not in self.employeeData and empName != empManager:   # Check whether manager is tracked and not a head manager
            raise ValueError("addNewEmployee::Adding manager w/o employee data - %s" % empManager)

        # Add employee inforomation
        emp = Employee(empName, empManager, empTitle, empLocation, supervised)            
        self.employeeData[empName] = emp        

        # If new employee is a head manager, add to headManager list
        if(empName == empManager):
            self.headManagers.add(empName)
        # If not a head manager, add the link to the child node
        else:
            self.employeeData[empManager].get_supervised().add(empName)

    def removeEmployee(self, empName):
        """ Removes Employee instance from employeeData
        Args:
            empName (str): Employee's name
        """

        if(self.logging):
            print ("Removing %s" % (empName))
        if empName not in self.employeeData:
            raise ValueError("removeEmployee::employee %s does not exist in employeeData" % (empName))
            
        manager = self.employeeData[empName].get_manager()          # Employee Manager
        supervised = self.employeeData[empName].get_supervised()    # Supervised Employees
        
        del self.employeeData[empName]                              # Remove employee as a supervisor
        
        # If employee is headManager, remove from headManagers and supervised employees become headManagers
        if manager==empName:
            self.headManagers.remove(empName)
            for emp in supervised:
                self.headManagers.add(emp)
                self.employeeData[emp].set_manager(emp)

        # Else, supervised employees. Set supervised employees manager to deleted's manager
        else:
            self.employeeData[manager].get_supervised().remove(empName)     # Remove childLink to deleted 
            self.employeeData[manager].get_supervised().update(supervised)  # re-assign childLinks of deleted
            for emp in supervised:
                self.employeeData[emp].set_manager(manager)

    def findSupervisedChain(self,supervisor,emp):
        """ Determines if a chain of employees from emp -> supervisor exists, i.e. supervisor indirectly/directly supervises emp
        Args:
            emp (str): Employee's name
            supervisor (str): Employee's Manager

        Returns: 
            chain (list): If empty, no chain exists. Else, chain of employees from emp -> supervisor
        """

        chain = []
        if emp == supervisor:           # Base case - One employee is not a chain
            return chain
        chain.append(emp)
        # Find supervisor chain starting at emp until head manager is reached
        while (self.employeeData[emp].get_manager() != emp):
            emp = self.employeeData[emp].get_manager()
            chain.append(emp)
            if(emp==supervisor):        # Chain has been found, return chain
                return chain

        return [] # Returns empty list because no chain exists from supervisor -> emp


    def reAssignEmployee(self, empName, newManager):
        """ Reassigns employee, empName, to a new Manager
        Args:
            empName (str): Employee's name
            newManager (str): Name of manager empName is being assigne dto

        Returns: none
        """
        if(self.logging):
            print ("Re-assigning %s to manager %s" % (empName, newManager))
        if empName not in self.employeeData:
            raise ValueError("reAssignEmployee::employee %s does not exist in employeeData" % (empName))
        if newManager not in self.employeeData:
            raise ValueError("reAssignEmployee::manager %s does not exist in employeeData" % (newManager))

        oldManager = self.employeeData[empName].get_manager()        
        if(oldManager == newManager):
            raise ValueError("reAssignEmployee::manager %s already assigned to  employee %s" % (newManager, empName))

        
        self.employeeData[empName].set_manager(newManager)   # reassign empName to newManager

        # Check if newManager exists in empName's "supervised" chain (empName -supervises-> ... -supervises-> newManager)
        supervisedChain = self.findSupervisedChain(empName,newManager)
        if(supervisedChain):
            self.employeeData[newManager].get_supervised().add(empName)
            self.employeeData[supervisedChain[1]].get_supervised().remove(newManager)   # Remove new Manager from its previous managers list            

            # Check if empName is a headManager
            if(empName in self.headManagers):
                self.headManagers.remove(empName)
                self.headManagers.add(newManager)
                self.employeeData[newManager].set_manager(newManager)           # New Manager becomes headManager
            else:
                self.employeeData[oldManager].get_supervised().remove(empName)  # Remove empName from oldManager
                self.employeeData[oldManager].get_supervised().add(newManager)
                self.employeeData[newManager].set_manager(oldManager)           # Set manager of newManager to empName's oldManager
        else:
            # If empName is a headManager, add empName to childList of newManager and reassign its parentLink to manager
            if(empName in self.headManagers):
                self.headManagers.remove(empName)                               # Remove from headManager list
                self.employeeData[newManager].get_supervised().add(empName)     # Add child Link to new manager
                self.employeeData[empName].set_manager(newManager)              # Re-assign parent

            # Employee is being made headManager, reassign parent & child links
            elif(empName == newManager):
                if(empName in self.headManagers):
                    raise ValueError("reAssignEmployee::%s already in headManagers" % (empName))    
                self.headManagers.add(empName)                                  # Add employee as headManager
                self.employeeData[oldManager].get_supervised().remove(empName)  # Remove child link from previous supervisor assignment
                self.employeeData[empName].set_manager(empName)                 # Re-assign parent

            # Employee is not a headManager and not being assigned to a headManager position
            else:
                self.employeeData[oldManager].get_supervised().remove(empName)  # Remove childLink from oldManager
                self.employeeData[newManager].get_supervised().add(empName)     # Add new childLink to newManager
