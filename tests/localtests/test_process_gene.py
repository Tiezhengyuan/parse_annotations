'''
Test class ProcessGene
'''
from tests.helper import *
from database.process_gene import ProcessGene


@ddt
class TestProcessGene(TestCase):
    
    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = ProcessGene()

    @skip
    @mock.patch.dict(os.environ, env)
    def test_process_taxonomy_entrez(self):
        self.c.process_taxonomy_entrez('9606')


    @skip
    @mock.patch.dict(os.environ, env)
    def test_split_gene_refseq_uniprotkb_collab(self):
        self.c.split_gene_refseq_uniprotkb_collab()

