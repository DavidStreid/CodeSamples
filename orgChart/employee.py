class Employee:
    """Employee Object

    Attributes:
        name (str): Employee's name
        manager (str): Employee's Manager
        title (str): Employee's Title
        location(str): Employee's Location
        supervised(set([str])): supervised employees
    """

    def __init__(self,name,manager,title,location,supervised):
        self.name = name
        self.manager = manager
        self.title = title
        self.location = location
        self.supervised = supervised

    def get_name(self):
        return self.name
    def set_name(self,name):
        self.name = name

    def get_manager(self):
        return self.manager
    def set_manager(self, manager):
        self.manager = manager

    def get_title(self):
        return self.title
    def set_title(self,title):
        self.title = title

    def get_location(self):
        return self.location
    def set_location(self,location):
        self.location = location

    def get_supervised(self):
        return self.supervised
    def set_supervised(self,supervised):
        self.supervised = supervised