import pytest
import shutil
import zipfile

from pathlib import Path

from squirrel.settings import AddonInstallerSettings
from squirrel.addons import ZipAddon

from fixtures import zip_file, valid_addons, invalid_addons


@pytest.fixture
def settings():
    return AddonInstallerSettings()


@pytest.fixture
def test_addon_path():
    path = Path('./blender_test_addon_path/')
    path.mkdir(exist_ok=True, parents=True)
    yield path
    shutil.rmtree(path, ignore_errors=True)


@pytest.fixture
def addon_backup_path():
    path = Path('./addon_backup_path')
    yield path
    shutil.rmtree(path, ignore_errors=True)


def validate_addon_content(addon, target_directory):
    with zipfile.ZipFile(addon.addon_filename) as current_zipfile:
        filenames = [
            zipinfo_obj.filename
            for zipinfo_obj in current_zipfile.infolist()
        ]

        for filename in filenames:
            print(filename)
            print(Path(addon.addon_path))
            # if Path(addon.addon_path).is_dir():
            #     assert Path(target_directory, filename).exists()
            # else:
            #     assert Path(addon.addon_path, filename).exists()


@pytest.mark.parametrize('file_or_folder', valid_addons)
def test_install_valid_addons(
    settings,
    zip_file,
    test_addon_path,
    addon_backup_path,
):

    settings.addon_path = test_addon_path
    settings.backup_path = addon_backup_path
    addon = ZipAddon(addon_filename=zip_file, settings=settings)
    addon.install()

    # TODO: Do actual addon content validation.
    validate_addon_content(addon, test_addon_path)
