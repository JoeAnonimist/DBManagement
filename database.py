import psycopg2.pool
from objectpath import ObjectPath


class Database:
    
    def __init__(self, name):
        self.connection_pools = {}
        self.name = name
    
    
    def get_connection_pool(self, object_path):
        
        if not object_path.__db_database__ in self.connection_pools:
            pool = psycopg2.pool.SimpleConnectionPool(
                5, 10, user='jon',
                password = 'jon',
                host=object_path.__db_server__, 
                database=object_path.__db_database__.name)
            self.connection_pools[object_path.__db_database__] = pool
            
        return self.connection_pools[object_path.__db_database__]
        
    
    def associators_of(self):
        pass
    
    def delete(self):
        pass
        
    def exec_query(self):
        pass
        
    def get(self, path):
        
        with self.get_connection_pool(path).getconn():
            pass
        
    def instances_of(self, path):
        
        with self.get_connection_pool(path).getconn() as connection:
            with connection.cursor() as cursor:
                cursor.execute("Select * From " + path.__db_table__)
                for row in cursor.fetchall():
                    print(row[1], row[2])
        
    def references_to(self):
        pass


if __name__ == '__main__':
    
    db = Database('pagila')
    path = ObjectPath('172.17.0.2', db, 'actor')
    db.instances_of(path)
