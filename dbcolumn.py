class DBColumn():

    def __init__(self, path, number, name, data_type, data_length,
                 dt_details, dimensions, not_null, has_default,
                 has_missing, identity, generated, collation, acl,
                 options, foreign_data_options, missing_value):

        self.path = path
        self.path.is_column = True

        self.number = number
        self.name = name
        self.data_type = data_type
        self.data_length = data_length
        self.dt_details = dt_details
        self.dimensions = dimensions
        self.not_null = not_null
        self.has_default = has_default
        self.has_missing = has_missing
        self.identity = identity
        self.generated = generated
        self.collation = collation
        self.acl = acl
        self.options = options
        self.foreign_data_options = foreign_data_options
        self.missing_value = missing_value
