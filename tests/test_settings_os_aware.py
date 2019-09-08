import pytest
from loguru import logger

from pathlib import Path

from utils.settings import AddonInstallerSettings
from fixtures import valid_addons
from fixtures import zip_file

logger.add('log/test_settings_os_aware.log', rotation="1 MB")


@pytest.fixture
def settings():
    return AddonInstallerSettings()


@pytest.fixture
def downloaded_addons_path():
    return [Path('./tests/test_files'), ]


@pytest.fixture
def found_download_test_addons(settings, downloaded_addons_path):
    return settings.find_downloaded_addons(
        additional_download_paths=downloaded_addons_path,
        ignore_settings=True
    )


def test_find_downloaded_addons(found_download_test_addons):
    # for file in valid_addons:
    #     zip_file = zip_file(file)

    # assert len(found_download_test_addons) == 4
    pass
