import os

import shutil
from pathlib import Path
import zipfile
import datetime

import logging
from loguru import logger


# Globals
BACKUP_SUFFIX = datetime.datetime.now().strftime("%Y.%m.%d_%H%M%S")
LOG_LEVEL = 'DEBUG'


def install_zip_plugin(plugin):


def backup_plugin(plugin):

def main():
    ''' Main function. '''

    # Nasty but how to use instead if no class in sight?
    global LOG
    LOG = setup_logging(level=LOG_LEVEL)

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
        try:
            if plugin.name == me.name:
                LOG.info("Skip handling myself.")
                continue

            if 'py' in plugin.suffix or 'zip' in plugin.suffix:
                prepare_plugin(plugin)
                remove_plugin(plugin)
        except:
            LOG.exception(f"Error in handling plugin: {plugin.name}")

    cleanup_tmp_folder()

if __name__ == '__main__':
    main()
