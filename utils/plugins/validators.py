from loguru import logger
import zipfile


class InvalidBlenderPlugin(Exception):
    pass


class BlenderPluginValidator():
    def __zipinfo_is_python(self, zipinfo_object):
        ''' Returns True, if the given zipinfo object is a python file. '''

        def endswith_py(filename):
            if filename.split('.')[-1] == "py":
                return True
            return False

        def is_file(zipinfo_object):
            return not zipinfo_object.is_dir()

        if is_file(zipinfo_object) and endswith_py(zipinfo_object.filename):
            return True
        return False

    def validate(self, filename):
        ''' Validates the given plugin_object.

            Args:
                filename (pathlib.Path): A file to check if it is a valid
                    blender plugin.

            Raises:
                InvalidBlenderPlugin
        '''

        logger.info(f"Validating {filename}")

        if zipfile.is_zipfile(filename):
            logger.debug(f"{filename} is a zip-file")
            self.__validate_zip_file(filename)
        else:
            raise InvalidBlenderPlugin(f'{filename} has an invalid file format.')

    def __validate_zip_file(self, filename):
        ''' Validates a blender plugin zip file. '''

        zipfile_object = zipfile.ZipFile(filename)
        infolist = zipfile_object.infolist()

        if not self.__is_not_a_blender_zip_archive(infolist):
            raise InvalidBlenderPlugin(
                f"{filename} is a blender application zip file."
            )
        else:
            logger.debug(f'{filename} is not a blender application zip file.')

        # Only one file found in zipfile_object
        if len(infolist) == 1:
            zipinfo_object = infolist[0]
            first_filename = zipinfo_object.filename

            if self.__zipinfo_is_python(zipinfo_object):
                logger.debug(
                    f"Found single file '{first_filename}' in '{filename}'"
                )
                self.__validate_zip_python(first_filename, zipfile_object)

        # Multiple files/folders found in zipfile_object
        elif len(infolist) > 1:
            logger.info(f"Found multiple files in {filename}: {len(infolist)}")

            # Validate all __init__.py files. There could be multiple ones.
            init_files = [
                file.filename
                for file in infolist
                if '__init__.py' in file.filename
            ]

            no_init_was_valid = True

            for file in init_files:
                try:
                    self.__validate_zip_python(file, zipfile_object)
                    no_init_was_valid = False
                except InvalidBlenderPlugin:
                    pass

            if no_init_was_valid:
                raise InvalidBlenderPlugin(
                    f'No valid __init__.py found in: {init_files}'
                )

    def __validate_zip_python(self, filename, zipfile_object):
        ''' Validates a blender plugin python file.
        '''

        with zipfile_object.open(filename, 'r') as fp:
            file_data = fp.read()

            if b'bl_info' not in file_data:
                raise InvalidBlenderPlugin((
                    f"Missing 'bl_info' section within file {filename}"
                ))
        logger.info(f"{zipfile_object.filename}/{filename} is valid.")
        return True

    def __is_not_a_blender_zip_archive(self, infolist):
        ''' Returns True if the given file is not a blender.org
            application zip file (which contains plenty of valid plugins)
            which we most likely not want to install into the addons
            directory.

            Args:
                infolist (ZipFile().infolist): Info listing of all contained
                    files within this zip file.

            Returns: (bool) True if the plugin is not a blender application.
        '''

        # Search pattern for a folder only existing in blender application zip
        # files.
        addons_path_stub_in_blender_zip = "scripts/addons"

        filename_list = [
            zipinfo.filename
            for zipinfo in infolist
        ]
        print(filename_list)

        for filename in filename_list:
            if addons_path_stub_in_blender_zip in filename:
                return False

        return True



