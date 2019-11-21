from tinydb import TinyDB, Query


class LocalAddonsDatabase():
    def __init__(self, database_file):
        self.database_file = database_file
        self.db = TinyDB(self.database_file)
        self.addon = Query()

    def addon_to_dict(self, addon_object):
        ''' Returns a dictionary containing all addon informations. '''

        addon_data = {
            'path': addon_object.addon_path.resolve().as_posix(),
            'version': addon_object.version,
            'author': addon_object.author,
            'name': addon_object.name,
            'description': addon_object.description
        }

        return addon_data

    def add(self, addon_object):
        ''' Updates or creates an addon database entry. '''

        addon_data = self.addon_to_dict(addon_object)

        # Update the existing entry
        if self.get(addon_object.name) is not None:
            self.db.update(addon_data, self.addon.name == addon_object.name)

        # Add an new entry
        else:
            self.db.insert(addon_data)

    def delete(self, addon_object):
        ''' Deletes an addon database entry. '''
        self.db.remove(self.addon.name == addon_object.name)

    def get(self, addon_name):
        result = self.db.search(self.addon.name == addon_name)
        if len(result) != 1:
            return None
        return result[0]

    def close(self):
        ''' Closes the database connection. '''
        self.db.close()
