import pytest

from pathlib import Path

from utils.settings import AddonInstallerSettings


@pytest.fixture
def settings():
    return AddonInstallerSettings()


@pytest.fixture
def downloaded_plugins_path():
    return [Path('./tests/test_files'), ]


@pytest.fixture
def found_download_test_plugins(settings, downloaded_plugins_path):
    return settings.find_downloaded_plugins(
        additional_download_paths=downloaded_plugins_path,
        ignore_settings=True
    )


@pytest.fixture
def validator():
    return BlenderPluginValidator()


def test_find_downloaded_plugins(found_download_test_plugins):
    assert len(found_download_test_plugins) == 4
