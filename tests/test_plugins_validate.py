import pytest

from pathlib import Path
from utils.plugins import ZipPlugin
from utils.plugins.validators import BlenderPluginValidator, InvalidBlenderPlugin


@pytest.fixture
def validator():
    return BlenderPluginValidator()


@pytest.fixture
def empty_single_plugin():
    return Path('./tests/test_files/empty_single_plugin.zip')


@pytest.fixture
def empty_folder_plugin():
    return Path('./tests/test_files/empty_folder_plugin.zip')


@pytest.fixture
def valid_single_plugin():
    return Path('./tests/test_files/valid_single_plugin.zip')


@pytest.fixture
def valid_folder_plugin():
    return Path('./tests/test_files/valid_folder_plugin.zip')


def test_validate_empty_single_plugin(validator, empty_single_plugin):
    with pytest.raises(InvalidBlenderPlugin) as excinfo:
        validator.validate(empty_single_plugin)
    assert "Missing 'bl_info'" in str(excinfo.value)


def test_validate_empty_folder_plugin(validator, empty_folder_plugin):
    with pytest.raises(InvalidBlenderPlugin) as excinfo:
        validator.validate(empty_folder_plugin)
    assert "No valid __init__.py found" in str(excinfo.value)


def test_validate_valid_single_plugin(validator, valid_single_plugin):
    validator.validate(valid_single_plugin)


def test_validate_valid_folder_plugin(validator, valid_folder_plugin):
    validator.validate(valid_folder_plugin)

