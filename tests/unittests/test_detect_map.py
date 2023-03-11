'''
Test class DetectMap
'''
from tests.helper import *
from parser.detect_map import DetectMap

@ddt
class TestUtils(TestCase):

    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = DetectMap()

    @mock.patch.dict(os.environ, env)
    @mock.patch('utils.jtxt.Jtxt.read_jtxt')
    def test_detect_map(self, mock_jtxt):
        mock_jtxt.return_value = iter([
            {
                'a':'1',
                'b': {'b1':4, 'b2':5},
                'c':[{'c1':3}, {'c1':4}],
                'd': [],
                'e': {'e1':[{'e2':1},{'e2':2}], 'e2':{'f':4, 'g':5}},
            },
        ])
        res, _ = self.c.get_fields()
        expect =  [{'a'}, {'d'}, {'b', 'b1'}, {'b2', 'b'}, {'c', 'c1'}, \
            {'e', 'e1', 'e2'}, {'e', 'f', 'e2'}, {'g', 'e', 'e2'}]
        assert res == expect
