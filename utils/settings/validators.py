import jsonschema
import yaml
import json
from pathlib import Path


class YAMLSettingsValidator():
    schema_file = Path(
        Path(__file__).parent,
        'settings_schema.json'
    )

    def validate(self, yaml_settings_file):
        ''' Validates the given yaml file against the schema file. '''

        yaml_settings_file = Path(yaml_settings_file)
        settings_yaml_data = None

        # Load the schema file
        with YAMLSettingsValidator.schema_file.open('r') as sfp:
            schema = json.load(sfp)

            with yaml_settings_file.open('r') as yfp:
                settings_yaml_data = yaml.safe_load(yfp)

                # Validate the yaml settings file against the schema file
                jsonschema.validate(
                    settings_yaml_data,
                    schema
                )

        return settings_yaml_data

