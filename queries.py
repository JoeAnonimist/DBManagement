GET_ATTRIBUTES = """
Select attnum, attname, typname, attcollation, 
    attnotnull, pg_get_expr(adbin, adrelid) , attstorage 
From pg_attribute attr
Join pg_type typ 
    On attr.atttypid = typ.oid
Left Join pg_attrdef def 
    On attr.attrelid = def.adrelid and attr.attnum = def.adnum
Where attrelid = %(table_name)s::regclass and attnum > 0;
"""

GET_PRIMARY_KEYS = """
Select tbl.relname, cls.relname, attr.attname
From pg_constraint con
Join pg_index ind On con.conindid = ind.indexrelid 
Join pg_class cls On cls.oid = ind.indexrelid
Join pg_attribute attr On attr.attrelid = cls.oid
Join pg_class tbl On tbl.oid = con.conrelid
Where contype = 'p'
And con.conrelid = %(table_name)s::regclass;
"""
