'''
Test class ProcessGene
'''
from tests.helper import *
from pAnnot.database.process_gene import ProcessGene


@ddt
class TestProcessGene(TestCase):
    
    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = ProcessGene('')

