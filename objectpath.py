class ObjectPath:
    
    def __init__(self, server, database, table, column="", primary_key=""):
        
        self.server = server
        self.database = database
        self.table = table
        self.column = column
        self.primary_key = primary_key
        
        self.is_table = True
        self.is_column = False
        self.is_primary_key = False
        self.is_foreign_key = False
        
    def __repr__(self):
        return self.server + ', ' + self.database.name + ', ' + self.table + ', ' + self.column + ', ' + self.primary_key
