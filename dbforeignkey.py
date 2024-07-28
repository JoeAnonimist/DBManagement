from database import Database
from objectpath import ObjectPath
import queries

class DBForeignKey():
    
    def __init__(self, path, constraint_name, name, 
        column_keys, table_name, definition):
            
        self.path = path
        self.constraint_name = constraint_name
        self.name = name
        self.table_name = table_name
        self.column_keys = column_keys
        self.foreign_table_name = foreign_table_name
        self.foreign_column_keys = foreign_column)keys
        self.definition = definition

