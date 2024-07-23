from database import Database
from objectpath import ObjectPath
import queries


class DBTable():
    
    def __init__(self, path):
        self.path = path
        self.attributes = self.populate_columns()
        self.primary_keys = self.populate_primary_keys()
    
    def populate_columns(self):
        with self.path.__db_database__.get_connection_pool(path).getconn() as connection:
            with connection.cursor() as cursor:
                table_name = {"table_name": self.path.__db_table__}
                cursor.execute(queries.GET_ATTRIBUTES, table_name)
                attributes = []
                for row in cursor.fetchall():
                    attributes.append(row[1])
        return attributes
        
    def populate_primary_keys(self):
        with self.path.__db_database__.get_connection_pool(path).getconn() as connection:
            with connection.cursor() as cursor:
                table_name = {"table_name": self.path.__db_table__}
                cursor.execute(queries.GET_PRIMARY_KEYS, table_name)
                primary_keys = []
                for row in cursor.fetchall():
                    primary_keys.append(row[2])
        return primary_keys


if __name__ == '__main__':
    
    db = Database('pagila')
    path = ObjectPath('localhost', db, 'film')
    tbl = DBTable(path)
    print('attributes:\n')
    for attr in tbl.attributes:
        print(attr)
    print('\nprimary keys:\n')
    for pk in tbl.primary_keys:
        print(pk)
