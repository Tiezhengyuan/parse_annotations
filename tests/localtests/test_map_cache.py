'''
Test class MapCache
'''
from tests.helper import *
from pAnnot.parser.map_cache import MapCache


@ddt
class TestMapCache(TestCase):

    @mock.patch.dict(os.environ, env)
    def test_(self):
        MapCache('', '', '')

    @mock.patch.dict(os.environ, env)
    def test_get_map(self):
        res = MapCache('human', 'GeneID', 'Symbol').get_map()
        assert '1' in res

