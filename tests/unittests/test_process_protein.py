'''
Test class ProcessProtein
'''
from tests.helper import *
from pAnnot.database.process_protein import ProcessProtein


@ddt
class TestProcessProtein(TestCase):
    
    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = ProcessProtein('')


