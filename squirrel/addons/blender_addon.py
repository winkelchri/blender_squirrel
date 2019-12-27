from pathlib import Path
import packaging

from loguru import logger

from ..validators import InvalidBlenderAddon
import ast


class BlenderAddon():
    def __init__(self, addon_path):
        self.__addon_path = self.__to_absolute_path(addon_path)
        self.__bl_info = None

    def __to_absolute_path(self, path):
        return Path(path).resolve()

    @property
    def addon_path(self):
        if not isinstance(self.__addon_path, Path):
            self.__addon_path = self.__to_absolute_path(self.__addon_path)
        return self.__addon_path

    @addon_path.setter
    def addon_path(self, value):
        logger.debug(f"Storing new value into addon_path: {value}")
        self.__addon_path = self.__to_absolute_path(value)

    @property
    def bl_info(self):
        ''' Returns the blender addons bl_info data. '''
        if self.__bl_info is None:
            bl_info_file = self.__get_bl_info_file()
            self.__bl_info = self.__extract_bl_info(bl_info_file)
        return self.__bl_info

    @property
    def version(self):
        ''' Returns a compareable packaging.Version object. '''

        version = self.bl_info['version']
        version_string = '.'.join(map(str, version))
        packaging_version = packaging.version.parse(version_string)
        return packaging_version

    @property
    def author(self):
        return self.bl_info['author']

    @property
    def name(self):
        return self.bl_info['name']

    @property
    def description(self):
        return self.bl_info['description']

    def __get_bl_info_file(self):
        ''' Returns the file which should contain the bl_info data. '''

        if self.addon_path.is_dir():
            return self.__get_bl_info_file_from_directory()

        elif self.addon_path.is_file():
            return self.addon_path

        else:
            raise FileNotFoundError(f'No file found for getting bl_info in: {self.addon_path}.')

    def __get_bl_info_file_from_directory(self):
        ''' Returns the file containing the bl_info data within a directory. '''

        if not self.addon_path.is_dir():
            raise AttributeError(f'{self.addon_path} is not a directory.')

        files = [file for file in self.addon_path.iterdir() if file.is_file()]

        if len(files) == 0:
            raise InvalidBlenderAddon(f'Directory {self.addon_path} does not contain any files.')

        # If there is only one file in the directory - it is most likely the one
        if len(files) == 1:
            file = files[0]
            if not file.name.endswith('.py'):
                raise InvalidBlenderAddon(
                    "There is no python file in directory {self.addon_path}"
                )
            return file

        # Get the __init__.py file ... if there is any
        # TODO: There might be a file called like the addon name instead of an __init__.py file.
        init_file = files.filter(lambda file: file.name == '__init__.py', files)
        if init_file != []:
            return init_file[0]

    def __extract_bl_info(self, bl_info_file):
        ''' Extracts the bl_info data from the given file. '''

        with bl_info_file.open('rb') as fp:
            content = fp.read()

        logger.debug(bl_info_file)
        try:
            module = ast.parse(content)
        except SyntaxError:
            raise InvalidBlenderAddon(f"The file '{bl_info_file}' is not a valid python file.")
        # Get all assignments:
        #     bl_info = {} is an `ast.Assign` node
        assignments = [node for node in module.body[:] if isinstance(node, ast.Assign)]

        # Iterate over assignments to hopefully get the bl_info one.
        for node in assignments:
            # bl_info = {} ... (left side) only contains one target
            # And the target.id contains the name of the assigned variable
            if len(node.targets) == 1:
                target = node.targets[0]

                # We found the bl_info definition ...
                if target.id == 'bl_info':
                    # ... now we only have to eval() the value of the assignment
                    # which should return a dictionary
                    bl_info_data = ast.literal_eval(node.value)
                    if not isinstance(bl_info_data, dict):
                        raise ValueError(
                            f"Unexpected value of bl_info_data. Expected 'dict', got '{type(bl_info_data)}'"
                        )
                    return bl_info_data

        raise InvalidBlenderAddon(f'{bl_info_file} does not contain any "bl_info" data.')
