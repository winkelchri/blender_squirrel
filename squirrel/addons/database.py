import packaging
import dataset
from sqlalchemy.pool import NullPool
from squirrel.addons.blender_addon import BlenderAddon
from pathlib import Path

from loguru import logger


class LocalAddonsDatabase():
    def __init__(self, database_file, disable_pooling=False):
        self.database_file = database_file

        if disable_pooling is True:
            engine_kwargs = {'poolclass': NullPool}
        else:
            engine_kwargs = {}

        self.db = dataset.connect(
            url=f'sqlite:///{self.database_file}',
            engine_kwargs=engine_kwargs
        )

        self.__addons_table = None

    @property
    def addons_table(self):

        if self.__addons_table is None:
            self.__addons_table = self.db.create_table(
                table_name='addons',
                primary_id='name',
                primary_type=self.db.types.text
            )

        return self.__addons_table

    def addon_to_dict(self, addon_object):
        ''' Creates a dictionary representation of the addon_object to store it into the database. '''

        addon_data = {
            'path': addon_object.addon_path.resolve().as_posix(),
            'version': str(addon_object.version),
            'author': addon_object.author,
            'name': addon_object.name,
            'description': addon_object.description
        }

        return addon_data

    def add(self, addon_object):
        ''' Updates or creates an addon database entry. '''

        logger.debug(f'Adding {addon_object} to database')

        addon_data = self.addon_to_dict(addon_object)
        self.addons_table.upsert(addon_data, ['name'])

    def delete(self, addon_object):
        ''' Deletes an addon database entry. '''

        self.addons_table.delete(name=addon_object.name)

    def get(self, addon_name):
        if not isinstance(addon_name, str):
            raise ValueError(f'Expecting "addon_name" to be string. Got {type(addon_name)}')

        logger.debug(f'Requesting addon data for {addon_name}')
        result = self.addons_table.find_one(name=addon_name)

        # Re-create the packaging.Version object from the version string
        result['version'] = packaging.version.parse(result['version'])

        # Re-create the path object from the stored path
        result['path'] = Path(result['path'])
        return result

    def close(self):
        ''' Closes the database connection. '''
        self.db.commit()
        self.db.local.conn.close()

    def drop(self):
        ''' Removes all data from out of the addons table. '''

        logger.warning(f"Drop {self.addons_table}")
        self.addons_table.drop()
