GET_TABLES = """
select tablename, schemaname from pg_tables 
where schemaname not in ('pg_catalog', 'information_schema') 
order by tablename;
"""

GET_ATTRIBUTES = """
Select attr.attnum, attr.attname, typ.typname, attr.attlen,  
    attr.atttypmod, attr.attndims, attr.attnotnull, 
    attr.atthasdef, attr.atthasmissing, attr.attidentity,
    attr.attgenerated, attr.attcollation, attr.attacl,
    attr.attoptions, attr.attfdwoptions,attr.attmissingval,
    pg_get_expr(adbin, adrelid) , attr.attstorage 
From pg_attribute attr
Join pg_type typ 
    On attr.atttypid = typ.oid
Left Join pg_attrdef def 
    On attr.attrelid = def.adrelid and attr.attnum = def.adnum
Where attrelid = %(table_name)s::regclass and attnum > 0;
"""

GET_PRIMARY_KEYS = """
SELECT 
  con.conname, attr.attname, c.relname, con.conkey,
  pg_catalog.pg_get_constraintdef(con.oid, true)
FROM pg_catalog.pg_class c, pg_catalog.pg_class c2, pg_catalog.pg_index i
  LEFT JOIN pg_catalog.pg_constraint con ON (conrelid = i.indrelid AND conindid = i.indexrelid AND contype IN ('p','u','x'))
  join pg_attribute attr on attr.attnum = any(con.conkey)
WHERE c.oid = %(table_name)s::regclass AND c.oid = i.indrelid AND i.indexrelid = c2.oid AND con.contype = 'p' and attr.attrelid = c.oid
ORDER BY i.indisprimary DESC, c2.relname;
"""

GET_FOREIGN_KEYS = """
select con.conname, attr.attname, cls.relname, con.conkey,
fattr.attname, fcls.relname, con.confkey,  
pg_get_constraintdef(con.oid, true)
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
SELECT refcon.conname, refattr.attname, refcls.relname, refcon.conkey,
fattr.attname, fcls.relname, refcon.confkey,
pg_get_constraintdef(refcon.oid, true) AS condef
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
SELECT t.tgname, pg_catalog.pg_get_triggerdef(t.oid, true), t.tgenabled, t.tgisinternal,
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
