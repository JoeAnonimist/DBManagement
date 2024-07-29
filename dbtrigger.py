from database import Database
from objectpath import ObjectPath


class DBTrigger():
    
    def __init__(self, path, name, definition):
            
        self.path = path
        self.path.is_trigger = True
        self.name = name
        self.definition = definition

