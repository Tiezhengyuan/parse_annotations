'''
Test class 
'''
from tests.helper import *
from database.swissprot import Swissprot


@ddt
class TestSwissProt(TestCase):

    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = Swissprot()

    @skip
    def test_parse_protein(self):
        handle = self.c.parse_protein()
        res = next(handle)
        assert 'accessions' in res


