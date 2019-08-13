import os
import shutil
import zipfile

from pathlib import Path

from loguru import logger


class ZipPlugin():
    # TODO: Maybe something more generic required? Single python files
    #       could also be a blender plugin.

    def __init__(self, plugin_filename, settings):
        self.__plugin_filename = Path(plugin_filename)
        self.settings = settings

        self.__zip_object = None

    @property
    def plugin_filename(self):
        return self.__plugin_filename

    def unzip(self, plugin):
        ''' Extracts the plugin into a temp folder. '''
        tmp_folder = self.settings.temp_folder
        logger.info(f'Unpack {plugin} into {tmp_folder}')

        # Unpack content into tmp folder
        zip_file = zipfile.ZipFile(self.plugin_filename)
        zip_file.extractall(tmp_folder)

        return tmp_folder

    def install(self):
        ''' Unpacks a zip plugin. '''

        logger.info(f'Starting installation of {self.plugin_filename}')
        tmp_folder = self.unzip(self.plugin_filename)

        # Get extracted plugin folder name
        plugin_folders = [
            folder for
            folder in tmp_folder.iterdir()
            if folder.is_dir()
        ]

        # Get all python files within the temp folder
        plugin_files = [
            file
            for file in tmp_folder.iterdir()
            if file.is_file() and ".py" in file.suffixes
        ]

        # Handle multiple plugin folders
        if len(plugin_folders) > 1:
            raise NotImplementedError(
                "Multiple top-level plugin folders are not supported."
            )
        # Handle no plugins folder -> Plugin directly within zip file
        elif len(plugin_folders) == 0 and len(plugin_files) == 1:
            plugin = plugin_files[0]
            logger.debug(f"Plugin {plugin.name} contains only a single file.")
        else:
            plugin = plugin_folders[0]
            logger.debug(f"Plugin {plugin.name} contains folders.")

        # Backup current plugin
        self.backup(plugin)

        # Install the plugin into the blender plugins path
        plugin_install_path = self.settings.plugin_path / plugin.name
        logger.info(f"Move {plugin} to {plugin_install_path}.")
        shutil.move(plugin, plugin_install_path)

    def backup(self, plugin):
        ''' Gets the source plugin path object and backups
            the current blender installed version.
        '''

        blender_plugin_path = self.settings.plugin_path
        backup_path = self.settings.backup_path
        logger.info(f"Creating backup of {plugin} into {backup_path}")

        if not backup_path.is_dir():
            os.mkdir(backup_path)

        # Current installed plugins
        installed_plugins = [
            installed_plugin
            for installed_plugin in blender_plugin_path.iterdir()
        ]

        # Find plugin within blender plugins
        for installed_plugin in installed_plugins:
            if installed_plugin.name == plugin.name:
                # And move it to backups
                plugin_backup_path = backup_path / plugin.name

                logger.info((
                    f"Found {plugin.name} in installed plugins.\n"
                    f"Copy {installed_plugin} -> {plugin_backup_path}"
                ))

                shutil.move(installed_plugin, plugin_backup_path)
