import sys
import pytest
import shutil
import pathlib

from squirrel.addon_sources.gumroad import GumroadProducts


@pytest.fixture
def download_folder():
    folder = pathlib.Path('download_test')
    if not folder.is_dir():
        folder.mkdir(parents=True)
    yield folder
    shutil.rmtree(folder.as_posix())


@pytest.fixture(scope='module')
def gumroad_addons():
    products_manager = GumroadProducts(debug_html_requests=True)
    yield products_manager


@pytest.mark.skipif(not sys.platform.startswith("win"), reason="currently only works on windows")
def test_gumroad_listing(gumroad_addons):
    assert len(gumroad_addons.list()) > 0


@pytest.mark.skipif(not sys.platform.startswith("win"), reason="currently only works on windows")
def test_gumroad_product_download_links(gumroad_addons):
    product_list = gumroad_addons.list()
    print(product_list)
    assert len(product_list) > 0

    product = product_list[0]
    print(product.download_links)
