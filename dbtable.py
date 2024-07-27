from copy import copy
from database import Database
from objectpath import ObjectPath
from dbcolumn import DBColumn
from dbprimarykey import DBPrimaryKey
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

        columns = self.path.database.exec_query(
        self.path,
        queries.GET_ATTRIBUTES,
        {"table_name": self.path.table})
        
        column_objects = []
        
        for col in columns:
            column_path = copy(self.path)
            column_path.database = self.path.database
            column_path.column = col[1]
            column_objects.append(DBColumn(column_path, col[0], col[1], 
                col[2], col[3], col[4], col[5], col[6], col[7], col[8], 
                col[9], col[10], col[11], col[12], col[13], col[14], 
                col[15]))
        return column_objects


    def populate_primary_keys(self):

        primary_keys = self.path.database.exec_query(
            self.path,
            queries.GET_PRIMARY_KEYS,
            {"table_name": self.path.table})
        
        primary_key_objects = []
        
        for pk in primary_keys:
            pk_path = copy(self.path)
            pk_path.database = self.path.database
            pk_path.primary_key = pk[1]
            primary_key_objects.append(DBPrimaryKey(pk_path, pk[0], 
                pk[1], pk[2], pk[3], pk[4]))
        return primary_key_objects


    def populate_foreign_keys(self):

        foreign_keys = self.path.database.exec_query(
            self.path, 
            queries.GET_FOREIGN_KEYS, 
            {"table_name": self.path.table})
        return foreign_keys

        
    def populate_references(self):

        references = self.path.database.exec_query(
            self.path,
            queries.GET_REFERENCES,
            {"table_name": self.path.table})
        return references


    def populate_triggers(self):

        triggers = self.path.database.exec_query(
            self.path,
            queries.GET_TRIGGERS,
            {"table_name": self.path.table})
        return triggers


if __name__ == '__main__':
    
    db = Database('pagila')
    path = ObjectPath('172.17.0.2', db, 'film')
    tbl = DBTable(path)
    
    print('attributes:\n')
    for attr in tbl.attributes:
        #print(attr.number, attr.name, attr.data_type, 
        #    attr.data_length, attr.dt_details, attr.dimensions, 
        #    attr.not_null, attr.has_default, attr.has_missing, 
        #    attr.identity, attr.generated, attr.collation, 
        #    attr.acl, attr.options, attr.foreign_data_options, 
        #    attr.missing_value)
        print(attr.path)
    
    print('\nprimary keys:\n')
    for pk in tbl.primary_keys:
        #print(pk.constraint_name, pk.name, pk.column_keys, 
        #    pk.table_name, pk.definition)
        print(pk.path)
        
    print('\nforeign keys\n')
    for fk in tbl.foreign_keys:
        print(fk)
        
    print("\nreferences\n")
    for r in tbl.references:
        print(r)
        
    print("\ntriggers\n")
    for t in tbl.triggers:
        print(t)
