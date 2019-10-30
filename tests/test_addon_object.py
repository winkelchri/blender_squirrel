import pytest

import tempfile
from fixtures import valid_addons, invalid_addons
from lib.addons.blender_addon import BlenderAddon
from lib.validators import InvalidBlenderAddon


@pytest.fixture
def addon(addon_path):
    return BlenderAddon(addon_path)


@pytest.mark.parametrize('addon_path', valid_addons)
def test_valid(addon):
    assert addon.name is not None


@pytest.mark.parametrize('addon_path', invalid_addons)
def test_invalid(addon):
    with pytest.raises(InvalidBlenderAddon):
        addon.name
