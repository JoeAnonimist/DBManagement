class ObjectPath:
    
    def __init__(self, server, database, table):
        
        self.__db_server__ = server
        self.__db_database__ = database
        self.__db_table__ = table
        
        self.__is_table__ = True
