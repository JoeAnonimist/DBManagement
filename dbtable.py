from copy import copy
#from DBManagement.database import Database
from DBManagement.objectpath import ObjectPath
from DBManagement.dbcolumn import DBColumn
from DBManagement.dbprimarykey import DBPrimaryKey
from DBManagement.dbforeignkey import DBForeignKey
from DBManagement.dbreference import DBReference
from DBManagement.dbtrigger import DBTrigger
from DBManagement import queries


class DBTable():

    def __init__(self, path, database, name, schema):
        self.path = path
        self.path.is_table = True
        self.database = database
        self.name = name
        self.schema = schema
        self.columns = self.populate_columns()
        self.primary_keys = self.populate_primary_keys()
        self.foreign_keys = self.populate_foreign_keys()
        self.references = self.populate_references()
        self.triggers = self.populate_triggers()

    def populate_columns(self):

        columns = self.database.exec_query(
            self.path,
            queries.GET_ATTRIBUTES,
            {"table_name": self.path.table})

        column_objects = []

        for col in columns:
            column_path = copy(self.path)
            column_path.is_table = False
            column_path.column = col[1]
            column_objects.append(DBColumn(column_path, col[0], col[1],
                col[2], col[3], col[4], col[5], col[6], col[7], col[8],
                col[9], col[10], col[11], col[12], col[13], col[14],
                col[15]))
        return column_objects

    def populate_primary_keys(self):

        primary_keys = self.database.exec_query(
            self.path,
            queries.GET_PRIMARY_KEYS,
            {"table_name": self.path.table})

        primary_key_objects = []

        for pk in primary_keys:
            pk_path = copy(self.path)
            pk_path.is_table = False
            pk_path.primary_key = pk[1]
            primary_key_objects.append(DBPrimaryKey(pk_path, pk[0],
                pk[1], pk[2], pk[3], pk[4]))
        return primary_key_objects

    def populate_foreign_keys(self):

        foreign_keys = self.database.exec_query(
            self.path,
            queries.GET_FOREIGN_KEYS,
            {"table_name": self.path.table})

        foreign_key_objects = []

        for fk in foreign_keys:
            fk_path = copy(self.path)
            fk_path.is_table = False
            fk_path.foreign_key = fk[1]
            foreign_key_objects.append(DBForeignKey(fk_path, fk[0],
                fk[1], fk[2], fk[3], fk[4], fk[5], fk[6], fk[7]))

        return foreign_key_objects

    def populate_references(self):

        references = self.database.exec_query(
            self.path,
            queries.GET_REFERENCES,
            {"table_name": self.path.table})

        reference_objects = []

        for ref in references:
            ref_path = copy(self.path)
            ref_path.is_table = False
            ref_path.reference = ref[1]
            reference_objects.append(DBReference(ref_path, ref[0],
                ref[1], ref[2], ref[3], ref[4], ref[5], ref[6], ref[7]))

        return reference_objects

    def populate_triggers(self):

        triggers = self.database.exec_query(
            self.path,
            queries.GET_TRIGGERS,
            {"table_name": self.path.table})

        trigger_objects = []

        for trig in triggers:
            trig_path = copy(self.path)
            trig_path.is_table = False
            trig_path.trigger = trig[0]
            trigger_objects.append(DBTrigger(trig_path, trig[0], trig[1]))

        return trigger_objects


if __name__ == '__main__':
    pass
