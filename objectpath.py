class ObjectPath:

    def __init__(self, server, database, table=None, column="", primary_key="",
                 foreign_key="", reference="", trigger=""):

        self.server = server
        self.database = database
        self.table = table
        self.column = column
        self.primary_key = primary_key
        self.foreign_key = foreign_key
        self.reference = reference
        self.trigger = trigger

        self.is_table = False
        self.is_column = False
        self.is_primary_key = False
        self.is_foreign_key = False
        self.is_reference = False
        self.is_trigger = False

    def __repr__(self):
        return 'Server: ' + self.server + ', Database: ' + self.database \
            + ', Table: ' + self.table + ', Column: ' + self.column \
            + ', Primary key: ' + self.primary_key + ', Foreign key: ' \
            + self.foreign_key + ', Reference: ' + self.reference \
            + ', Trigger: ' + self.trigger + '\n' \
            + '\t\tIs table: ' + str(self.is_table) + ', Is column: ' \
            + str(self.is_column) + ', Is primary key: ' \
            + str(self.is_primary_key) + ', Is foreign key: ' \
            + str(self.is_foreign_key) + ', Is reference: ' \
            + str(self.is_reference) + ', Is trigger: ' + str(self.is_trigger)
