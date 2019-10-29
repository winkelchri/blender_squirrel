import pytest

from pathlib import Path
from lib.addons import ZipAddon
from lib.validators import BlenderAddonValidator, InvalidBlenderAddon

from fixtures import zip_file, valid_addons, invalid_addons


@pytest.fixture
def validator():
    return BlenderAddonValidator()


@pytest.mark.parametrize('file_or_folder', valid_addons)
def test_valid(validator, zip_file):
    validator.validate(zip_file)


@pytest.mark.parametrize('file_or_folder', invalid_addons)
def test_empty(validator, zip_file):
    with pytest.raises(InvalidBlenderAddon):
        validator.validate(zip_file)

