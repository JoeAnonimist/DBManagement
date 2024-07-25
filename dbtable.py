from database import Database
from objectpath import ObjectPath
import queries


class DBTable():
    
    def __init__(self, path):
        self.path = path
        self.attributes = self.populate_columns()
        self.primary_keys = self.populate_primary_keys()
        self.foreign_keys = self.populate_foreign_keys()
        self.references = self.populate_references()
        self.triggers = self.populate_triggers()
    
    def populate_columns(self):
        with self.path.__db_database__.get_connection_pool(path).getconn() as connection:
            with connection.cursor() as cursor:
                table_name = {"table_name": self.path.__db_table__}
                cursor.execute(queries.GET_ATTRIBUTES, table_name)
                attributes = []
                for row in cursor.fetchall():
                    attributes.append(row[0])
        return attributes
        
    def populate_primary_keys(self):
        with self.path.__db_database__.get_connection_pool(path).getconn() as connection:
            with connection.cursor() as cursor:
                table_name = {"table_name": self.path.__db_table__}
                cursor.execute(queries.GET_PRIMARY_KEYS, table_name)
                primary_keys = []
                for row in cursor.fetchall():
                    primary_keys.append(row[0])
        return primary_keys
        
    def populate_foreign_keys(self):
        with self.path.__db_database__.get_connection_pool(path).getconn() as connection:
            with connection.cursor() as cursor:
                table_name = {"table_name": self.path.__db_table__}
                cursor.execute(queries.GET_FOREIGN_KEYS, table_name)
                foreign_keys = []
                for row in cursor.fetchall():
                    foreign_keys.append(row[1])
        return foreign_keys
        
    def populate_references(self):
        with self.path.__db_database__.get_connection_pool(path).getconn() as connection:
            with connection.cursor() as cursor:
                table_name = {"table_name": self.path.__db_table__}
                cursor.execute(queries.GET_REFERENCES, table_name)
                references = []
                for row in cursor.fetchall():
                    references.append(row[1] + ', ' + row[2])
        return references

    def populate_triggers(self):
        with self.path.__db_database__.get_connection_pool(path).getconn() as connection:
            with connection.cursor() as cursor:
                table_name = {"table_name": self.path.__db_table__}
                cursor.execute(queries.GET_REFERENCES, table_name)
                triggers = []
                for row in cursor.fetchall():
                    triggers.append(row[1] + ', ' + row[2])
        return triggers


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
        
    print('\nforeign keys\n')
    for fk in tbl.foreign_keys:
        print(fk)
        
    print("\nreferences\n")
    for r in tbl.references:
        print(r)
        
    print("\ntriggers\n")
    for t in tbl.triggers:
        print(t)
