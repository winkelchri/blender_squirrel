import pytest
import shutil
import zipfile

from pathlib import Path

from lib.settings import AddonInstallerSettings
from lib.addons import ZipAddon

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


# @pytest.fixture
# def single_file_addon():
#     return Path('./tests/test_files/valid_single_addon.zip')


# @pytest.fixture
# def folder_addon():
#     return Path('./tests/test_files/valid_folder_addon.zip')


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

    validate_addon_content(addon, test_addon_path)

    # The addon file has to exist within the addon path
    # assert Path(test_addon_path, 'valid_addon.py').exists()


# def test_install_folder_addon(
#     settings,
#     folder_addon,
#     test_addon_path,
#     addon_backup_path
# ):

#     settings.addon_path = test_addon_path
#     settings.backup_path = addon_backup_path
#     addon = ZipAddon(addon_filename=folder_addon, settings=settings)
#     addon.install()

#     # Addon root folder must exist
#     assert Path(test_addon_path, 'valid_folder_addon').exists()

#     assert Path(test_addon_path, 'valid_folder_addon', '__init__.py').exists()

#     assert Path(test_addon_path, 'valid_folder_addon', 'folder1').exists()
#     assert Path(test_addon_path, 'valid_folder_addon', 'folder1', 'test_file.py').exists()


# def test_multiple_addon_install(
#     settings,
#     folder_addon,
#     single_file_addon,
#     test_addon_path,
#     addon_backup_path
# ):
#     for i in range(2):
#         test_install_singlefile_addon(settings,
#                                        single_file_addon,
#                                        test_addon_path,
#                                        addon_backup_path)
#     for i in range(2):
#         test_install_folder_addon(settings,
#                                    folder_addon,
#                                    test_addon_path,
#                                    addon_backup_path)
