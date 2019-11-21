import os
import shutil
import zipfile

from pathlib import Path
from ..validators import BlenderAddonValidator
from loguru import logger


class ZipAddon():
    # TODO: Maybe something more generic required? Single python files
    #       could also be a blender addon.

    def __init__(self, addon_filename, settings):
        self.__addon_filename = Path(addon_filename)
        self.settings = settings

        self.__zip_object = None
        self.__addon_path = None

    @property
    def addon_path(self):
        return self.__addon_path

    @property
    def addon_filename(self):
        return self.__addon_filename

    def unzip(self, addon):
        ''' Extracts the addon into a temp folder. '''
        tmp_folder = self.settings.temp_folder
        logger.info(f'Unpack {addon} into {tmp_folder}')

        # Unpack content into tmp folder
        zip_file = zipfile.ZipFile(self.addon_filename)
        zip_file.extractall(tmp_folder)

        return tmp_folder

    def install(self):
        ''' Unpacks a zip addon. '''

        self.validate()

        logger.info(f'Starting installation of {self.addon_filename}')
        tmp_folder = self.unzip(self.addon_filename)

        # Get extracted addon folder name
        addon_folders = [
            folder for
            folder in tmp_folder.iterdir()
            if folder.is_dir()
        ]

        # Get all python files within the temp folder
        addon_files = [
            file
            for file in tmp_folder.iterdir()
            if file.is_file() and ".py" in file.suffixes
        ]

        # Handle multiple addon folders
        if len(addon_folders) > 1:
            raise NotImplementedError(
                "Multiple top-level addon folders are not supported."
            )
        # Handle no addons folder -> Addon directly within zip file
        elif len(addon_folders) == 0 and len(addon_files) == 1:
            addon = addon_files[0]
            logger.debug(f"Addon {addon.name} contains only a single file.")
        else:
            addon = addon_folders[0]
            logger.debug(f"Addon {addon.name} contains folders.")

        # Backup current addon
        self.backup(addon)

        # Install the addon into the blender addons path
        addon_install_path = self.settings.addon_path / addon.name
        logger.info(f"Move {addon} to {addon_install_path}.")
        shutil.move(addon, addon_install_path)

        self.__addon_path = Path(addon_install_path, addon)

    def backup(self, addon):
        ''' Gets the source addon path object and backups
            the current blender installed version.
        '''

        blender_addon_path = self.settings.addon_path
        backup_path = self.settings.backup_path
        logger.info(f"Creating backup of {addon} into {backup_path}")

        if not backup_path.is_dir():
            os.mkdir(backup_path)

        # Current installed addons
        installed_addons = [
            installed_addon
            for installed_addon in blender_addon_path.iterdir()
        ]

        # Find addon within blender addons
        for installed_addon in installed_addons:
            if installed_addon.name == addon.name:
                # And move it to backups
                addon_backup_path = backup_path / addon.name

                logger.info((
                    f"Found {addon.name} in installed addons. "
                    f"Copy {installed_addon} -> {addon_backup_path}"
                ))

                shutil.move(installed_addon.as_posix(),
                            addon_backup_path.as_posix())

    def validate(self):
        ''' Checks if the current addon is valid. '''

        validator = BlenderAddonValidator()
        validator.validate(self.addon_filename)
