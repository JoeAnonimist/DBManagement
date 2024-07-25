class ObjectPath:
    
    def __init__(self, server, database, table):
        
        self.server = server
        self.database = database
        self.table = table
        
        self.is_table = True
        self.is_column = False
