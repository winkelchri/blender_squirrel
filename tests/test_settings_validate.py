import pytest
from jsonschema.exceptions import ValidationError

from squirrel.validators import YAMLSettingsValidator

from pathlib import Path


@pytest.fixture
def validator():
    return YAMLSettingsValidator()


@pytest.fixture
def valid_settings_file():
    return Path('./tests/test_files/valid_settings.yaml')


@pytest.fixture
def invalid_settings_file():
    return Path('./tests/test_files/invalid_settings.yaml')


def test_valid_settings_file(validator, valid_settings_file):
    validator.validate(valid_settings_file)


def test_invalid_settings_file(validator, invalid_settings_file):
    with pytest.raises(ValidationError):
        validator.validate(invalid_settings_file)
