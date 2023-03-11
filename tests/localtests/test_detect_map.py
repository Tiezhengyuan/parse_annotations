'''
Test class DetectMap
'''
from tests.helper import *
from parser.detect_map import DetectMap

@ddt
class TestUtils(TestCase):

    @data(
        ['entrez.jtxt', 34],
        ['expasy.jtxt', 64]
    )
    @unpack
    @mock.patch.dict(os.environ, env)
    def test_detect_map(self, filename, expect):
        infile = os.path.join(env['DIR_CACHE'], 'human', filename)
        _, fields =  DetectMap(infile).get_fields()
        assert len(fields) >= expect

