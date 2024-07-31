class DBReference():

    def __init__(self, path, values):

        self.path = path
        self.path.is_reference = True

        self.constraint_name = values.constraint_name
        self.ref_name = values.ref_name
        self.ref_table_name = values.ref_table_name
        self.ref_column_keys = values.ref_column_keys
        self.name = values.name
        self.table_name = values.table_name
        self.column_keys = values.column_keys
        self.definition = values.definition
