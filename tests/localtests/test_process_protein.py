'''
Test class 
'''
from tests.helper import *
from pAnnot.database.process_protein import ProcessProtein


@ddt
class TestProcessProtein(TestCase):
    
    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = ProcessProtein('')

    @skip
    @mock.patch.dict(os.environ, env)
    def test_process_protein(self):
        self.c.process_protein()
    
    @skip
    @mock.patch.dict(os.environ, env)
    def test_parse_ncbi_protein(self):
        self.c.parse_ncbi_protein()
