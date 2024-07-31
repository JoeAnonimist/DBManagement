class DBPrimaryKey():

    def __init__(self, path, values):

        self.path = path
        self.path.is_primary_key = True

        self.constraint_name = values.constraint_name
        self.name = values.name
        self.table_name = values.table_name
        self.column_keys = values.column_keys
        self.definition = values.definition
