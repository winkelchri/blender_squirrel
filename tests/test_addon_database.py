import os
import pytest

import tempfile
from pathlib import Path
from squirrel.addons.database import LocalAddonsDatabase
from squirrel.addons.blender_addon import BlenderAddon


@pytest.fixture
def database():
    with tempfile.TemporaryDirectory() as temp_dir:
        db_file = Path(temp_dir, 'db.json')
        addon_database = LocalAddonsDatabase(db_file)
        yield addon_database
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
    assert database.db.all() == []


def test_update(database, addon):
    test_create(database, addon)
    print(addon)
    addon.addon_path = "."

    database.add(addon)
    entry = database.get(addon)
    print(entry)


