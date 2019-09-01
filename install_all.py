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


def install_zip_addon(addon):


def backup_addon(addon):

def main():
    ''' Main function. '''

    # Nasty but how to use instead if no class in sight?
    global LOG
    LOG = setup_logging(level=LOG_LEVEL)

    # Ensure valid blender addon path
    if not BLENDER_PLUGIN_PATH.is_dir():
        raise FileNotFoundError(
            "The given blender addon path is invalid: {}".format(
                BLENDER_PLUGIN_PATH
            )
        )

    # Path object of install script
    me = Path(__file__)

    # Iterate over addons in current path
    for addon in Path('.').iterdir():
        try:
            if addon.name == me.name:
                LOG.info("Skip handling myself.")
                continue

            if 'py' in addon.suffix or 'zip' in addon.suffix:
                prepare_addon(addon)
                remove_addon(addon)
        except:
            LOG.exception(f"Error in handling addon: {addon.name}")

    cleanup_tmp_folder()

if __name__ == '__main__':
    main()
