class ObjectPath:
    
    def __init__(self, server, database, table="", column="", primary_key="",
        foreign_key="", reference="", trigger=""):
        
        self.server = server
        self.database = database
        self.table = table
        self.column = column
        self.primary_key = primary_key
        self.foreign_key = foreign_key
        self.reference = reference
        self.trigger = trigger
        
        self.is_table = False
        self.is_column = False
        self.is_primary_key = False
        self.is_foreign_key = False
        self.is_reference = False
        self.is_trigger = False
        
    def __repr__(self):
        return self.server + ', ' + self.database + ', ' 
        + self.table + ', ' + self.column + ', ' + self.primary_key
        + self.foreign_key + ', ' + self.reference + ', ' + self.trigger
