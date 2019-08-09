import datetime
import os
import platform
import shutil
import tempfile

from pathlib import Path
from loguru import logger

from .loaders import YAMLSettings


class AddonInstallerSettings():
    def __init__(self, settings_file=None, blender_version="2.80"):
        self.system = platform.system()
        self.settings_file = settings_file
        self.blender_version = blender_version
        self.__settings = None
        self.__temp_dir = None
        self.__plugin_path = None
        self.__backup_path = None

    @property
    def settings(self):
        if self.__settings is None:
            yaml_settings = YAMLSettings()
            if self.settings_file is None:
                self.settings_file = yaml_settings.find()

            self.__settings = yaml_settings.load(self.settings_file)
        return self.__settings

    @property
    def plugin_path(self):
        if self.__plugin_path is None:
            if self.blender_version != "2.80":
                raise NotImplementedError(
                    'Currently, only Blender version 2.80 is supported')

            # Handle windows paths
            if self.system == "Windows":
                plugin_path = self.__windows_plugin_path(self.blender_version)

            # Raise error on unsupported platforms
            else:
                raise NotImplementedError(
                    f'Your system: {self.system} is currently not supported.'
                )

            # Create the plugin directory if not existing
            if not plugin_path.exists():
                plugin_path.mkdir(parents=True)

            self.__plugin_path = plugin_path

        return self.__plugin_path

    @plugin_path.setter
    def plugin_path(self, value):
        if Path(value).exists() is False:
            raise ValueError(f'Plugin path {value} does not exist')

        self.__plugin_path = value

    def __windows_plugin_path(self, blender_version):
        ''' Returns the blender plugins path for windows '''

        base_path = os.environ.get('APPDATA', None)

        if base_path is None:
            raise IOError("%APPDATA% environment variable not found!")

        base_path = Path(base_path)

        return Path(
            base_path,
            f"Blender Foundation/Blender/{blender_version}/scripts/addons"
        )

    @property
    def temp_folder(self):
        if self.__temp_dir is not None:
            logger.info(
                f"Cleaning up existing temp directory {self.__temp_dir}")
            shutil.rmtree(self.__temp_dir, ignore_errors=True)

        self.__temp_dir = Path(tempfile.mkdtemp())
        return self.__temp_dir

    def find_downloaded_plugins(
        self,
        additional_download_paths=[],
        plugin_extensions=['.py', '.zip']
    ):
        ''' Finds all downloaded packages within all provided download paths.
        '''
        all_plugin_files = []

        logger.debug(f'Searching in: {self.settings["download_paths"]}')
        logger.debug(f'And: {additional_download_paths}')

        download_paths = self.settings['download_paths'] + additional_download_paths
        for download_path in download_paths:
            download_path = Path(download_path)

            # Filter out all files with valid plugin extensions
            plugin_files = [
                plugin_file
                for plugin_file in download_path.iterdir()
                if plugin_file.suffix in plugin_extensions
            ]
            all_plugin_files += plugin_files
        return all_plugin_files

    @property
    def backup_path(self, base_folder=None):
        ''' Returns the backup path for installed plugins. '''

        if self.__backup_path is None:
            if base_folder is None:
                base_folder = self.plugin_path

                datetime_suffix = datetime.datetime.now().strftime("%Y.%m.%d_%H%M%S")

            self.__backup_path = Path(
                base_folder, '..', f'addons_backup_{datetime_suffix}'
            )

        return self.__backup_path

    @backup_path.setter
    def backup_path(self, value):
        self.__backup_path = value
