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


