import os
import platform
import shutil
from pathlib import Path
import zipfile
import datetime

import logging

# Globals

TMP_FOLDER = Path("./tmp")
BACKUP_SUFFIX = datetime.datetime.now().strftime("%Y.%m.%d_%H%M%S")


def get_blender_plugin_path():
    system = platform.system()

    # Handle windows paths
    if system == "Windows":
        base_path = os.environ.get('APPDATA', None)

        if base_path is None:
            raise IOError("%APPDATA% environment variable not found!")

        base_path = Path(base_path)

        return base_path / "Blender Foundation/Blender/2.79/scripts/addons"

    else:
        raise NotImplementedError(
            'Your system: {} is currently not supported.'.format(system)
        )

BLENDER_PLUGIN_PATH = get_blender_plugin_path()


def prepare_tmp_folder():
    # Prepare tmp_folder
    tmp_folder = TMP_FOLDER

    # Clean it if necessary
    if tmp_folder.is_dir():
        cleanup_tmp_folder()

    # And always have a clean one :)
    os.mkdir(tmp_folder)
    return tmp_folder


def cleanup_tmp_folder():
    tmp_folder = TMP_FOLDER
    shutil.rmtree(tmp_folder, ignore_errors=True)
    LOG.debug("Cleanup {}".format(tmp_folder))


def install_zip_plugin(plugin):
    ''' Unpacks a zip plugin. '''

    tmp_folder = prepare_tmp_folder()

    # Unpack content into tmp folder
    zip_file = zipfile.ZipFile(plugin)
    zip_file.extractall(tmp_folder)

    # Get extracted plugin folder name
    plugin_folders = [
        folder for
        folder in tmp_folder.iterdir()
        if folder.is_dir()
    ]

    # Handle multiple plugin folders
    if len(plugin_folders) != 1:
        raise NotImplementedError(
            "Multiple plugin folders are currently not supported."
        )

    extracted_plugin_folder = plugin_folders[0]

    # Backup current plugin
    backup_plugin(extracted_plugin_folder)

    # Copy new content into blender path


def backup_plugin(plugin):
    ''' Gets the source plugin path object and backups
        the current blender installed version.
    '''

    # Handle backup path
    backup_path = BLENDER_PLUGIN_PATH / '..' / 'addons_backup_{}'.format(
        BACKUP_SUFFIX
    )
    if not backup_path.is_dir():
        os.mkdir(backup_path)

    # Current installed plugins
    installed_plugins = [
        installed_plugin
        for installed_plugin in BLENDER_PLUGIN_PATH.iterdir()
        if installed_plugin.is_dir()
    ]

    # Find plugin within blender plugins
    for installed_plugin in installed_plugins:
        if installed_plugin.name == plugin.name:
            # And move it to backups
            LOG.info(
                "Found {} in installed plugins. Move to backups.".format(
                    plugin.name
                )
            )
            plugin_backup_path = backup_path / plugin.name
            shutil.move(installed_plugin, plugin_backup_path)

    # Finally move plugin to addons folder
    plugin_install_path = BLENDER_PLUGIN_PATH / plugin.name
    LOG.info("Move {} to {}.".format(plugin, plugin_install_path))
    shutil.move(plugin, plugin_install_path)


def prepare_plugin(plugin):
    LOG.info('Prepare {}'.format(plugin))

    if plugin.suffix == '.zip':
        install_zip_plugin(plugin)


def remove_plugin(plugin):
    LOG.info('Remove {}'.format(plugin))
    os.remove(plugin)


def fetch_addons_from_gumroad():
    # Fire up a selenium docker container
    # Log into gumroad using provided credentials
    # Get all blender addons
    # Download the latest version of every single addon
    # Update the addons locally
    pass


def setup_logging(level='DEBUG'):
    ''' Setup basic logging. '''

    format_string = (
        "%(asctime)s - "
        "[%(name)s][%(levelname)s:%(lineno)s]: "
        "%(message)s"
    )

    logging.basicConfig(format=format_string)

    # Setup logger
    logger = logging.getLogger('install_log')
    logger.setLevel(level)

    # Setup filehandler
    fh = logging.FileHandler('installer.log')
    fh.setLevel(level)
    fh.setFormatter(logging.Formatter(format_string))
    logger.addHandler(fh)

    return logger


def main():
    ''' Main function. '''

    # Nasty but how to use instead if no class in sight?
    global LOG
    LOG = setup_logging()

    # Ensure valid blender plugin path
    if not BLENDER_PLUGIN_PATH.is_dir():
        raise FileNotFoundError(
            "The given blender plugin path is invalid: {}".format(
                BLENDER_PLUGIN_PATH
            )
        )

    # Path object of install script
    me = Path(__file__)

    # Iterate over plugins in current path
    for plugin in Path('.').iterdir():

        if plugin.name == me.name:
            LOG.info("Skip handling myself.")
            continue

        if 'py' in plugin.suffix or 'zip' in plugin.suffix:
            prepare_plugin(plugin)
            remove_plugin(plugin)

    cleanup_tmp_folder()

if __name__ == '__main__':
    main()
