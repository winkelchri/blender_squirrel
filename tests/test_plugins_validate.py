import pytest

from pathlib import Path
from utils.plugins import ZipPlugin
from utils.plugins.validators import BlenderPluginValidator, InvalidBlenderPlugin

from fixtures import zip_file, valid_plugins, invalid_plugins


@pytest.fixture
def validator():
    return BlenderPluginValidator()


@pytest.mark.parametrize('file_or_folder', valid_plugins)
def test_valid(validator, zip_file):
    validator.validate(zip_file)


@pytest.mark.parametrize('file_or_folder', invalid_plugins)
def test_empty(validator, zip_file):
    with pytest.raises(InvalidBlenderPlugin):
        validator.validate(zip_file)

