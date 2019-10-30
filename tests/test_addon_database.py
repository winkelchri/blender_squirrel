import os
import pytest

import tempfile
from pathlib import Path
from lib.addons.database import LocalAddonsDatabase
from lib.addons.blender_addon import BlenderAddon


@pytest.fixture
def database():
    with tempfile.TemporaryDirectory() as temp_dir:
        db_file = Path(temp_dir, 'db.json')
        yield LocalAddonsDatabase(db_file)

@pytest.fixture
def addon():
    return BlenderAddon('test_files/addon_valid_single')


def test_create(database, addon):
    database.update_or_create(addon)
