from copy import copy
from enum import Enum
from DBManagement.objectpath import ObjectPath
from DBManagement.dbcolumn import DBColumn
from DBManagement.dbprimarykey import DBPrimaryKey
from DBManagement.dbforeignkey import DBForeignKey
from DBManagement.dbreference import DBReference
from DBManagement.dbtrigger import DBTrigger
from DBManagement import queries


class Property(Enum):
    COLUMN = 1
    PRIMARY_KEY = 2
    FOREIGN_KEY = 3
    REFERENCE = 4
    TRIGGER = 5

class DBTable():

    def __init__(self, path, database, values):
        
        self.path = path
        self.path.is_table = True
        self.database = database
        self.name = values.name
        self.schema = values.schema
        
        self.columns = self.get_properties(Property.COLUMN)
        self.primary_keys = self.get_properties(Property.PRIMARY_KEY)
        self.foreign_keys = self.get_properties(Property.FOREIGN_KEY)
        self.references = self.get_properties(Property.REFERENCE)
        self.triggers = self.get_properties(Property.TRIGGER)

    def get_properties(self, kind):
        
        property_objects = []

        if kind == Property.COLUMN:
            properties = self.database.exec_query(
                self.path, queries.GET_ATTRIBUTES, 
                {"table_name": self.path.table})
            for prop in properties:
                path = copy(self.path)
                path.is_table = False
                path.column = prop.name
                property_objects.append(DBColumn(path, prop))
        elif kind == Property.PRIMARY_KEY:
            properties = self.database.exec_query(
                self.path, queries.GET_PRIMARY_KEYS,
                {"table_name": self.path.table})
            for prop in properties:
                path = copy(self.path)
                path.is_table = False
                path.primary_key = prop.name
                property_objects.append(DBPrimaryKey(path, prop))
        elif kind == Property.FOREIGN_KEY:
            properties = self.database.exec_query(
                self.path, queries.GET_FOREIGN_KEYS,
                {"table_name": self.path.table})
            for prop in properties:
                path = copy(self.path)
                path.is_table = False
                path.foreign_key = prop.name
                property_objects.append(DBForeignKey(path, prop))
        elif kind == Property.REFERENCE:
            properties = self.database.exec_query(
                self.path, queries.GET_REFERENCES,
                {"table_name": self.path.table})
            for prop in properties:
                path = copy(self.path)
                path.is_table = False
                path.reference = prop.ref_name
                property_objects.append(DBReference(path, prop))
        else:
            properties = self.database.exec_query(
                self.path, queries.GET_TRIGGERS,
                {"table_name": self.path.table})
            for prop in properties:
                path = copy(self.path)
                path.is_table = False
                path.trigger = prop.name
                property_objects.append(DBTrigger(path, prop))
                
        return property_objects


if __name__ == '__main__':
    pass
