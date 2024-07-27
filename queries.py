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
SELECT true as sametable, conname,
  pg_catalog.pg_get_constraintdef(r.oid, true) as condef,
  conrelid::pg_catalog.regclass AS ontable
FROM pg_catalog.pg_constraint r
WHERE r.conrelid = %(table_name)s::regclass AND r.contype = 'f'
     AND conparentid = 0
ORDER BY conname;
"""


GET_REFERENCES = """
SELECT conname, conrelid::pg_catalog.regclass AS ontable,
       pg_catalog.pg_get_constraintdef(oid, true) AS condef
  FROM pg_catalog.pg_constraint c
 WHERE confrelid IN (SELECT pg_catalog.pg_partition_ancestors(%(table_name)s)
                     UNION ALL VALUES (%(table_name)s::pg_catalog.regclass))
       AND contype = 'f' AND conparentid = 0
ORDER BY conname;
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
