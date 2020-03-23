import datetime
import os
import platform
import shutil
import tempfile

from pathlib import Path
from loguru import logger

from .loaders import YAMLSettings


class AddonInstallerSettings():

    __slots__ = (
        'system',
        'settings_file',
        'blender_version',
        '__settings',
        '__temp_dir',
        '__addon_path',
        '__backup_path',
    )

    def __init__(self, settings_file=None, blender_version="2.80"):
        self.system = platform.system()
        self.settings_file = settings_file
        self.blender_version = blender_version
        self.__settings = None
        self.__temp_dir = None
        self.__addon_path = None
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
    def addon_path(self):
        if self.__addon_path is None:
            if self.blender_version != "2.80":
                raise NotImplementedError(
                    'Currently, only Blender version 2.80 is supported')

            # Handle windows paths
            if self.system == "Windows":
                addon_path = self.__windows_addon_path(self.blender_version)

            # Raise error on unsupported platforms
            else:
                raise NotImplementedError(
                    f'Your system: {self.system} is currently not supported.'
                )

            # Create the addon directory if not existing
            if not addon_path.exists():
                addon_path.mkdir(parents=True)

            self.__addon_path = addon_path

        return self.__addon_path

    @addon_path.setter
    def addon_path(self, value):
        if Path(value).exists() is False:
            raise ValueError(f'Addon path {value} does not exist')

        self.__addon_path = value

    def __windows_addon_path(self, blender_version):
        ''' Returns the blender addons path for windows '''

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

    def find_downloaded_addons(
        self,
        additional_download_paths=[],
        addon_extensions=['.py', '.zip'],
        ignore_settings=False
    ):
        ''' Finds all downloaded packages within all provided download paths.

            Args:
                additional_download_paths (list): List of paths to search for
                    blender addons additionally.
                addon_extensions (list): default ['.py', '.zip'] list of
                    extensions to check for possible Blender addons.
                ignore_settings (bool): Switch if the settings "download_paths"
                    should be ignored. Usefull in case of testing or over-
                    writing behaviour using the `additional_download_paths`.
            Returns:
                list (pathlib.Path): List of path's of found blender addons.
        '''

        all_addon_files = []

        if not isinstance(additional_download_paths, list):
            raise ValueError((
                f"additional_download_paths has to be type of <list>, "
                f"not {type(additional_download_paths)}"
            ))

        download_paths = self.settings['download_paths'] + \
            additional_download_paths

        if ignore_settings:
            logger.debug((
                f"Ignore settings = True. "
                f"Skipping: {self.settings['download_paths']}."
            ))

            download_paths = additional_download_paths

        logger.debug(f"Searching for addons in: {download_paths}")

        for download_path in download_paths:
            download_path = Path(download_path)

            # Filter out all files with valid addon extensions
            addon_files = [
                addon_file
                for addon_file in download_path.iterdir()
                if addon_file.suffix in addon_extensions
            ]
            all_addon_files += addon_files
        return all_addon_files

    @property
    def backup_path(self, base_folder=None):
        ''' Returns the backup path for installed addons. '''

        if self.__backup_path is None:
            if base_folder is None:
                base_folder = self.addon_path

                datetime_suffix = datetime.datetime.now().strftime("%Y.%m.%d_%H%M%S")

            self.__backup_path = Path(
                base_folder, '..', f'addons_backup_{datetime_suffix}'
            )

        return self.__backup_path

    @backup_path.setter
    def backup_path(self, value):
        self.__backup_path = value
