import pytest

from pathlib import Path

from utils.settings import AddonInstallerSettings
from utils.plugins import ZipPlugin


@pytest.fixture
def settings():
    return AddonInstallerSettings()


@pytest.fixture
def downloaded_plugins_path():
    return Path('./tests/test_files')


def test_find_downloaded_plugins(settings, downloaded_plugins_path):
    downloaded_plugins = settings.find_downloaded_plugins(
        additional_download_paths=downloaded_plugins_path
    )
    assert len(downloaded_plugins) == 2
