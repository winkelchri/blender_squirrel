import pytest
import shutil
import zipfile

from pathlib import Path

from squirrel.settings import AddonInstallerSettings
from squirrel.addons import ZipAddon

from test_addon_install import test_addon_install_path
from test_addon_install import test_addon_backup_path
from test_addon_install import settings

from fixtures import zip_files
from fixtures import valid_addons
from fixtures import invalid_addons


# Gather valid addons
# Install them
# @pytest.mark.parametrize('file_or_folder', valid_addons)

@pytest.mark.parametrize('targets', [valid_addons, ])
def test_install_valid_addons_and_index(
    settings,
    zip_files,
    test_addon_install_path,
    test_addon_backup_path,
):
    settings.addon_path = test_addon_install_path
    settings.backup_path = test_addon_backup_path

    addons = [ZipAddon(zip_file, settings=settings) for zip_file in zip_files]

    for addon in addons:
        addon.install()

    # addon = ZipAddon(addon_filename=zip_file, settings=settings)
    # addon.install()


# Run the indexing
# Check the index content
