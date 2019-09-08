from pathlib import Path
from loguru import logger
import yaml

from ..validators import YAMLSettingsValidator


class YAMLSettings():
    common_directories = (
        Path('.'),
    )
    settings_filename = 'settings.yaml'

    def find(self, search_directories=[], settings_filename=None):
        ''' Finds settings yaml files. '''

        # Fallback if no settings_filename was provided
        if settings_filename is None:
            settings_filename = YAMLSettings.settings_filename

        possible_settings_locations = search_directories

        # Fallback if no search paths are provided
        if len(possible_settings_locations) == 0:
            possible_settings_locations = YAMLSettings.common_directories

        # Return a list of existing files (if any)
        existing_settings_files = [
            Path(file, settings_filename)
            for file in possible_settings_locations
            if Path(file, settings_filename).exists()
        ]

        # One settings file found
        if len(existing_settings_files) == 1:
            return existing_settings_files[0]

        # More than one settings file found
        elif len(existing_settings_files) > 1:
            chosen_settings_file = existing_settings_files[0]
            logger.warning((
                f"Found two settings files {existing_settings_files}. "
                f"Using the first one: {chosen_settings_file}"
            ))

            return chosen_settings_file

        # No settings file found
        else:
            raise FileNotFoundError('Did not found any `settings.yaml`.')

    def load(self, yaml_settings_file):
        ''' Loads the given yaml settings file. '''
        validator = YAMLSettingsValidator()

        if not Path(yaml_settings_file).exists():
            raise FileNotFoundError(f'No such file: {yaml_settings_file}')

        # Will raise if format is invalid
        settings_yaml_data = validator.validate(yaml_settings_file)
        return settings_yaml_data
