class DBColumn():

    def __init__(self, path, values):

        self.path = path
        self.path.is_column = True

        self.number = values.number
        self.name = values.name
        self.data_type = values.data_type
        self.data_length = values.data_length
        self.dt_details = values.dt_details
        self.dimensions = values.dimensions
        self.not_null = values.not_null
        self.has_default = values.has_default
        self.has_missing = values.has_missing
        self.identity = values.identity
        self.generated = values.generated
        self.collation = values.collation
        self.acl = values.acl
        self.options = values.options
        self.foreign_data_options = values.foreign_data_options
        self.missing_value = values.missing_value
