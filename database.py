from copy import copy
import psycopg2.pool
import queries
from objectpath import ObjectPath


class Database:
    
    def __init__(self, server_name, name):
        self.connection_pool = None
        self.name = name
        self.server = server_name
        self.path = ObjectPath(self.name, self.server)
        self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
            5, 100, user='jon',
            password = 'jon',
            host=self.server, 
            database=self.name)
        self.tables = self.populate_tables()
    
    
    def populate_tables(self):
        
        from dbtable import DBTable
        
        tables = self.exec_query(self.path, queries.GET_TABLES, "")
        
        table_objects = []
        
        for table in tables:
            table_path = copy(self.path)
            table_path.table = table[0]
            table_objects.append(DBTable(table_path, self, table[0], table[1]))
        return table_objects

    
    def associators_of(self):
        pass
    
    def delete(self):
        pass
        
    def exec_query(self, path, query, parameters):
        
        connection =  self.connection_pool.getconn()
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        return_values = cursor.fetchall()
        self.connection_pool.putconn(connection)
        return return_values
        
        
    def get(self, path):
        
        with self.connection_pool.getconn():
            pass
        
    def instances_of(self, path):
        
        with self.connection_pool.getconn() as connection:
            with connection.cursor() as cursor:
                cursor.execute("Select * From " + path.table)
                for row in cursor.fetchall():
                    print(row[1], row[2])
        
    def references_to(self):
        pass


if __name__ == '__main__':
    
    db = Database('localhost', 'pagila')
    path = ObjectPath('localhost', 'pagila', 'actor')
    #db.instances_of(path)
    
    for t in db.tables:
        print(t.name)
        print('\t--- Columns ---')
        for c in t.columns:
            print('\t' + c.name)
        print('\t--- Primary keys ---')
        for pk in t.primary_keys:
            print('\t' + pk.name)
        print('\t--- Foreign keys ---')
        for fk in t.foreign_keys:
            print('\t' + fk.name)
        print('\t--- References ---')
        for ref in t.references:
            print('\t' + ref.name, ref.ref_table_name, ref.ref_name)
        print('\t--- Triggers ---')
        for trig in t.triggers:
            print('\t' + trig.name)

