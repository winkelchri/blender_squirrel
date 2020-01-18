import pytest
import sys

import browser_cookie3


@pytest.mark.skipif(not sys.platform.startswith("win"), reason="currently only works on windows")
def test_get_cookie():
    ''' More of a general test if browser_cookie3 works as expected. '''
    cj = browser_cookie3.firefox()
    assert cj is not None
