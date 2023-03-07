'''
Test class 
'''
from tests.helper import *
from database.process_protein import ProcessProtein


@ddt
class TestProcessProtein(TestCase):
    
    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = ProcessProtein(debugging=True)

    @skip
    @mock.patch.dict(os.environ, env)
    def test_process_protein(self):
        self.c.process_protein()
        
    @mock.patch.dict(os.environ, env)
    def test_parse_ncbi_protein(self):
        self.c.parse_ncbi_protein()
