from database import Database
from objectpath import ObjectPath


class DBForeignKey():
    
    def __init__(self, path, constraint_name, name, table_name,
        column_keys, foreign_name, foreign_table_name, 
        foreign_column_keys, definition):
            
        self.path = path
        self.path.is_foreign_key = True
        
        self.constraint_name = constraint_name
        self.name = name
        self.table_name = table_name
        self.column_keys = column_keys
        self.foreign_name = foreign_name
        self.foreign_table_name = foreign_table_name
        self.foreign_column_keys = foreign_column_keys
        self.definition = definition

