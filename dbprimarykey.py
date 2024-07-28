from database import Database
from objectpath import ObjectPath
import queries

class DBPrimaryKey():
    
    def __init__(self, path, constraint_name, name, 
        table_name, column_keys, definition):
            
        self.path = path
        self.constraint_name = constraint_name
        self.name = name
        self.table_name = table_name
        self.column_keys = column_keys
        self.definition = definition
