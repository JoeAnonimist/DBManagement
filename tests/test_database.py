import re
import pytest
from collections import namedtuple
from sqlalchemy import MetaData, create_engine
from sqlalchemy.sql import text
from DBManagement import queries
from DBManagement.objectpath import ObjectPath
from DBManagement.dbtable import DBTable
from DBManagement.database import Database


class TestDatabase:

    @pytest.fixture(scope='class')
    def db_metadata(self):
        engine = create_engine('postgresql://jon:jon@localhost/pagila')
        metadata = MetaData()
        metadata.reflect(bind=engine)
        db = Database('localhost', 'pagila', 'jon', 'jon')
        yield (metadata, db, engine)

    def test_populate_tables(self, db_metadata):

        metadata, db, _ = db_metadata

        assert len(metadata.tables) == len(db.tables)

        for table in db.tables:
            assert table.name in metadata.tables

    def test_exec_query(self, db_metadata):

        metadata, db, engine = db_metadata

        with engine.connect() as conn:
            tables = conn.execute(text(queries.GET_TABLES)).fetchall()
            assert len(tables) == len(
                db.exec_query(None, queries.GET_TABLES, ""))

        for table in metadata.tables:

            with engine.connect()as conn:

                columns = conn.execute(text(self.convert_psycopg2_to_sqlalchemy(
                    queries.GET_ATTRIBUTES, table))).fetchall()
                assert len(columns) == len(db.exec_query(
                    None, queries.GET_ATTRIBUTES, {"table_name": table}))

                primary_keys = conn.execute(text(self.convert_psycopg2_to_sqlalchemy(
                    queries.GET_PRIMARY_KEYS, table))).fetchall()
                assert len(primary_keys) == len(db.exec_query(
                    None, queries.GET_PRIMARY_KEYS, {"table_name": table}))

                foreign_keys = conn.execute(text(self.convert_psycopg2_to_sqlalchemy(
                    queries.GET_FOREIGN_KEYS, table))).fetchall()
                assert len(foreign_keys) == len(db.exec_query(
                    None, queries.GET_FOREIGN_KEYS, {"table_name": table}))

                references = conn.execute(text(self.convert_psycopg2_to_sqlalchemy(
                    queries.GET_REFERENCES, table))).fetchall()
                assert len(references) == len(db.exec_query(
                    None, queries.GET_REFERENCES, {"table_name": table}))

                triggers = conn.execute(text(self.convert_psycopg2_to_sqlalchemy(
                    queries.GET_TRIGGERS, table))).fetchall()
                assert len(triggers) == len(db.exec_query(
                    None, queries.GET_TRIGGERS, {"table_name": table}))

    def convert_psycopg2_to_sqlalchemy(self, sql_string, table_name):

        pattern = r'%\((\w+)\)s'
        sqlalchemy_string = re.sub(pattern, r':\1', sql_string)

        return sqlalchemy_string.replace(":table_name", "'" + table_name + "'")
