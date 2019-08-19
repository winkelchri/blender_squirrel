import pytest
import shutil

from pathlib import Path

from utils.settings import AddonInstallerSettings
from utils.plugins import ZipPlugin


@pytest.fixture
def settings():
    return AddonInstallerSettings()


@pytest.fixture
def test_plugin_path():
    path = Path('./blender_test_plugin_path/')
    path.mkdir(exist_ok=True, parents=True)
    yield path
    shutil.rmtree(path, ignore_errors=True)


@pytest.fixture
def plugin_backup_path():
    path = Path('./plugin_backup_path')
    yield path
    shutil.rmtree(path, ignore_errors=True)


@pytest.fixture
def single_file_plugin():
    return Path('./tests/test_files/valid_single_plugin.zip')


@pytest.fixture
def folder_plugin():
    return Path('./tests/test_files/valid_folder_plugin.zip')


def test_install_singlefile_plugin(
    settings,
    single_file_plugin,
    test_plugin_path,
    plugin_backup_path
):

    settings.plugin_path = test_plugin_path
    settings.backup_path = plugin_backup_path
    plugin = ZipPlugin(plugin_filename=single_file_plugin, settings=settings)
    plugin.install()

    # The plugin file has to exist within the plugin path
    assert Path(test_plugin_path, 'valid_plugin.py').exists()


def test_install_folder_plugin(
    settings,
    folder_plugin,
    test_plugin_path,
    plugin_backup_path
):

    settings.plugin_path = test_plugin_path
    settings.backup_path = plugin_backup_path
    plugin = ZipPlugin(plugin_filename=folder_plugin, settings=settings)
    plugin.install()

    # Plugin root folder must exist
    assert Path(test_plugin_path, 'valid_folder_plugin').exists()

    assert Path(test_plugin_path, 'valid_folder_plugin', '__init__.py').exists()

    assert Path(test_plugin_path, 'valid_folder_plugin', 'folder1').exists()
    assert Path(test_plugin_path, 'valid_folder_plugin', 'folder1', 'test_file.py').exists()


def test_multiple_plugin_install(
    settings,
    folder_plugin,
    single_file_plugin,
    test_plugin_path,
    plugin_backup_path
):
    for i in range(2):
        test_install_singlefile_plugin(settings,
                                       single_file_plugin,
                                       test_plugin_path,
                                       plugin_backup_path)
    for i in range(2):
        test_install_folder_plugin(settings,
                                   folder_plugin,
                                   test_plugin_path,
                                   plugin_backup_path)
