from copy import copy
import psycopg2.pool
from psycopg2.extras import NamedTupleCursor
from DBManagement import queries
from DBManagement.objectpath import ObjectPath
from DBManagement.dbtable import DBTable

class Database:

    def __init__(self, server_name, name):
        self.connection_pool = None
        self.name = name
        self.server = server_name
        self.path = ObjectPath(self.name, self.server)
        self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
            5, 100, user='jon',
            password='jon',
            host=self.server,
            database=self.name)
        self.tables = self.populate_tables()

    def populate_tables(self):

        tables = self.exec_query(self.path, queries.GET_TABLES, "")

        table_objects = []

        for table in tables:
            table_path = copy(self.path)
            table_path.table = table[0]
            table_objects.append(DBTable(table_path, self, table))
        return table_objects

    def associators_of(self):
        pass

    def delete(self):
        pass

    def exec_query(self, path, query, parameters):

        connection = self.connection_pool.getconn()
        cursor = connection.cursor(cursor_factory=NamedTupleCursor)
        #cursor = connection.cursor()
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
    pass
