import os
import pytest

import tempfile
from pathlib import Path
from squirrel.addons.database import LocalAddonsDatabase

from squirrel.addons.blender_addon import BlenderAddon
from squirrel.addons.zip_addon import ZipAddon

from fixtures import zip_file, valid_addons, invalid_addons


@pytest.fixture()
def database():
    ''' Creates a local test database. '''
    db_location = Path('temp')
    db_file = Path(db_location, 'db.sqlite')

    if not db_location.exists():
        db_location.mkdir()

    addon_database = LocalAddonsDatabase(db_file, disable_pooling=True)
    addon_database.drop()
    yield addon_database
    addon_database.drop()
    addon_database.close()


@pytest.fixture
def addon():
    file = Path('tests/test_files/addon_valid_single')
    return BlenderAddon(file)


def test_create(database, addon):
    addon_name = addon.name
    database.add(addon)
    database_entry = database.get(addon_name)
    assert database_entry['name'] == addon_name


def test_delete(database, addon):
    test_create(database, addon)

    database.delete(addon)
    assert list(database.addons_table.all()) == []


def test_update(database, addon):
    # Initially add the addon with the default path
    test_create(database, addon)

    # Modify the addon location
    # Must be the absolute (to be compared against later), in because the blender
    # BlenderAddon object will only always resolve the path.
    new_addon_location = Path('.').resolve()
    addon.addon_path = new_addon_location

    # Update (double add == update) the addon data
    database.add(addon)
    entry = database.get(addon.name)

    # There should still only be one addon stored into the database (updated)
    assert len(list(database.addons_table.all())) == 1

    # And the query should return the updated path from the database
    assert entry['path'] == new_addon_location


def test_get(database, addon):
    test_create(database, addon)

    result = database.get(addon.name)

    assert result['path'] == addon.addon_path
    assert result['version'] == addon.version
    assert result['author'] == addon.author
    assert result['name'] == addon.name
    assert result['description'] == addon.description


@pytest.mark.parametrize('file_or_folder', valid_addons)
def test_store_zip_addons(database, zip_file):
    zip_addon = ZipAddon(addon_filename=zip_file, settings=None)
    addon_path = zip_addon.unzip()
    blender_addon = BlenderAddon(addon_path)

    test_create(database, blender_addon)

    del blender_addon
    del zip_addon

