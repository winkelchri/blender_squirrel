import pytest
import shutil
import pathlib

from utils.plugin_sources.gumroad import GumroadProducts


@pytest.fixture
def download_folder():
    folder = pathlib.Path('download_test')
    if not folder.is_dir():
        folder.mkdir(parents=True)
    yield folder
    shutil.rmtree(folder.as_posix())


@pytest.fixture(scope='module')
def gumroad_plugins():
    products_manager = GumroadProducts()
    yield products_manager


def test_gumroad_listing(gumroad_plugins):
    assert len(gumroad_plugins.list()) > 0


def test_gumroad_product_download_links(gumroad_plugins):
    product_list = gumroad_plugins.list()
    product = product_list[0]
    print(product.download_links)
