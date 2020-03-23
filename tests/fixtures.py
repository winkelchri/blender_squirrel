import pytest
import shutil
import tempfile
import pathlib


@pytest.fixture
def target():
    return "./tests/test_files/addon_valid_single"


@pytest.fixture
def targets():
    return ()


def create_zip_file(target):
    ''' `target` shall either be a file or a folder. '''

    temp_dir = tempfile.TemporaryDirectory()

    # Use pathlib path's
    temp_path = pathlib.Path(temp_dir.name)
    target = pathlib.Path(target)

    # Create the target file (excluding extension)
    base_name = temp_path / target.name

    # Create the archive and return it's name
    target = shutil.make_archive(
        base_name=base_name,
        format="zip",
        root_dir=target
    )

    return (pathlib.Path(target), temp_dir)


@pytest.fixture
def zip_file(target):
    ''' Creates a zip file of the given folder or file within a temp folder
        and return its filename.

        Deletes the temp zip file afterwards.

        Usage:
            Use this fixture in the test as a parameter.
            Add the `@pytest.mark.parametrize('target', list_of_files)`
            decorator as a test.

        Example:
            @pytest.mark.parametrize('target', list_of_files)
            def my_test(zip_file):
                # Will be a single zip file of the list_of_files list
                print(zip_file)
    '''

    target_zip, temp_dir = create_zip_file(target)
    yield target_zip
    temp_dir.cleanup()
    # Everything will be deleted now ...


@pytest.fixture
def zip_files(targets):

    zipped_targets = list(map(create_zip_file, targets))
    zip_files = [item[0] for item in zipped_targets]
    temp_dirs = [item[1] for item in zipped_targets]

    yield zip_files

    for temp_dir in temp_dirs:
        temp_dir.cleanup()


valid_addons = [
    './tests/test_files/addon_valid_single',
    './tests/test_files/addon_valid_single_with_assets',
    './tests/test_files/addon_valid_folder',
]


invalid_addons = [
    './tests/test_files/addon_empty_single',
    './tests/test_files/addon_empty_folder',
    './tests/test_files/blender-2.80-test'
]
