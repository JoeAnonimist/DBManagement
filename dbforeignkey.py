class DBForeignKey():

    def __init__(self, path, values):

        self.path = path
        self.path.is_foreign_key = True

        self.constraint_name = values.constraint_name
        self.name = values.name
        self.table_name = values.table_name
        self.column_keys = values.column_keys
        self.foreign_name = values.foreign_name
        self.foreign_table_name = values.foreign_table_name
        self.foreign_column_keys = values.foreign_column_keys
        self.definition = values.definition
