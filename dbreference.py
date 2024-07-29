from database import Database
from objectpath import ObjectPath


class DBReference():
    
    def __init__(self, path, constraint_name, ref_name, ref_table_name, 
        ref_column_keys, name, table_name, column_keys, definition):
            
        self.path = path
        self.path.is_reference = True
        
        self.constraint_name = constraint_name
        self.ref_name = ref_name
        self.ref_table_name = ref_table_name
        self.ref_column_keys = ref_column_keys
        self.name = name
        self.table_name = table_name
        self.column_keys = column_keys
        self.definition = definition

