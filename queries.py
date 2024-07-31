GET_TABLES = """
select tablename as name, 
       schemaname as schema from pg_tables
where schemaname not in ('pg_catalog', 'information_schema')
order by tablename;
"""

GET_ATTRIBUTES = """
Select attr.attnum as number, 
       attr.attname as name, 
       typ.typname as data_type, 
       attr.attlen as data_length,
       attr.atttypmod as dt_details, 
       attr.attndims as dimensions, 
       attr.attnotnull as not_null,
       attr.atthasdef as has_default, 
       attr.atthasmissing as has_missing, 
       attr.attidentity as identity,
       attr.attgenerated as generated, 
       attr.attcollation as collation, 
       attr.attacl as acl,
       attr.attoptions as options, 
       attr.attfdwoptions as foreign_data_options,
       attr.attmissingval as missing_value,
       pg_get_expr(adbin, adrelid) , 
       attr.attstorage
From pg_attribute attr
Join pg_type typ
    On attr.atttypid = typ.oid
Left Join pg_attrdef def
    On attr.attrelid = def.adrelid and attr.attnum = def.adnum
Where attrelid = %(table_name)s::regclass and attnum > 0;
"""

GET_PRIMARY_KEYS = """
SELECT con.conname as constraint_name, 
       attr.attname as name,
       c.relname as table_name,
       con.conkey as column_keys,
       pg_catalog.pg_get_constraintdef(con.oid, true) as definition
FROM pg_catalog.pg_class c, pg_catalog.pg_class c2, pg_catalog.pg_index i
  LEFT JOIN pg_catalog.pg_constraint con
  ON (conrelid = i.indrelid AND conindid = i.indexrelid AND contype IN ('p','u','x'))
  join pg_attribute attr on attr.attnum = any(con.conkey)
WHERE c.oid = %(table_name)s::regclass AND c.oid = i.indrelid AND i.indexrelid = c2.oid AND con.contype = 'p' and attr.attrelid = c.oid
ORDER BY i.indisprimary DESC, c2.relname;
"""

GET_FOREIGN_KEYS = """
select con.conname as constraint_name,
       attr.attname as name,
       cls.relname as table_name,
       con.conkey as column_keys,
       fattr.attname as foreign_name,
       fcls.relname as foreign_table_name,
       con.confkey as foreign_column_keys,
       pg_get_constraintdef(con.oid, true) as definition
from pg_constraint con
join pg_class cls on con.conrelid = cls.oid
join pg_attribute attr on con.conrelid = attr.attrelid
join pg_class fcls on con.confrelid = fcls.oid
join pg_attribute fattr on con.confrelid = fattr.attrelid
where con.contype = 'f'
and attr.attnum = any(con.conkey)
and fattr.attnum = any(con.confkey)
and cls.oid = %(table_name)s::regclass;
"""


GET_REFERENCES = """
SELECT refcon.conname as constraint_name,
       refattr.attname as ref_name,
       refcls.relname as ref_table_name,
       refcon.conkey as ref_column_keys,
       fattr.attname as name,
       fcls.relname as table_name,
       refcon.confkey as column_keys,
       pg_get_constraintdef(refcon.oid, true) AS definition
FROM pg_constraint refcon
join pg_class refcls on refcon.conrelid = refcls.oid
join pg_attribute refattr on refcon.conrelid = refattr.attrelid
join pg_class fcls on refcon.confrelid = fcls.oid
join pg_attribute fattr on refcon.confrelid = fattr.attrelid
 WHERE refcon.confrelid IN (SELECT pg_partition_ancestors(%(table_name)s)
                     UNION ALL VALUES (%(table_name)s::regclass))
AND refcon.contype = 'f'
AND refcon.conparentid = 0
and refattr.attnum = any(refcon.conkey)
and fattr.attnum = any(refcon.confkey);
"""

GET_TRIGGERS = """
SELECT t.tgname as name,
       pg_catalog.pg_get_triggerdef(t.oid, true) as definition,
       t.tgenabled, 
       t.tgisinternal,
          CASE WHEN t.tgparentid != 0 THEN
            (SELECT u.tgrelid::pg_catalog.regclass
             FROM pg_catalog.pg_trigger AS u,
                  pg_catalog.pg_partition_ancestors(t.tgrelid) WITH ORDINALITY AS a(relid, depth)
             WHERE u.tgname = t.tgname AND u.tgrelid = a.relid
                   AND u.tgparentid = 0
             ORDER BY a.depth LIMIT 1)
          END AS parent
FROM pg_catalog.pg_trigger t
WHERE t.tgrelid = %(table_name)s::pg_catalog.regclass AND (NOT t.tgisinternal OR (t.tgisinternal AND t.tgenabled = 'D')
    OR EXISTS (SELECT 1 FROM pg_catalog.pg_depend WHERE objid = t.oid
        AND refclassid = 'pg_catalog.pg_trigger'::pg_catalog.regclass))
ORDER BY 1;
"""
