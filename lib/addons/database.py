from tinydb import TinyDB, Query


class LocalAddonsDatabase():
    def __init__(self, database_file):
        self.database_file = database_file
        self.db = TinyDB(self.database_file)

    def update_or_create(self, addon_object):
        ''' Updates or creates an addon database entry. '''

        pass

    def delete(self, addon_object):
        ''' Deletes an addon database entry. '''

        pass
