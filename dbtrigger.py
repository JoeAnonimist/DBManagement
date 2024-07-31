class DBTrigger():

    def __init__(self, path, values):

        self.path = path
        self.path.is_trigger = True
        self.name = values.name
        self.definition = values.definition
