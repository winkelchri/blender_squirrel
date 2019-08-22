import pytest
import shutil
import tempfile
import pathlib


@pytest.fixture
def file_or_folder():
    return "./tests/test_files/plugin_valid_single"


@pytest.fixture
def zip_file(file_or_folder):
    ''' Creates a zip file of the given folder or file within a temp folder
        and return its filename.

        Deletes the temp zip file afterwards.
    '''

    with tempfile.TemporaryDirectory() as temp_dir:
        # Use pathlib path's
        temp_dir = pathlib.Path(temp_dir)
        file_or_folder = pathlib.Path(file_or_folder)

        # Create the target file (excluding extension)
        base_name = temp_dir / file_or_folder.name

        # Create the archive and return it's name
        target = shutil.make_archive(
            base_name=base_name,
            format="zip",
            root_dir=file_or_folder
        )

        output = pathlib.Path(target)
        yield output

        # Everything will be deleted now ...