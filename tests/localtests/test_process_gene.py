'''
Test class ProcessGene
'''
from tests.helper import *
from pAnnot.database.process_gene import ProcessGene


@ddt
class TestProcessGene(TestCase):
    
    @mock.patch.dict(os.environ, env)
    def setUp(self):
        dir_db = os.path.join(env['DIR_CACHE'], 'human')
        self.c = ProcessGene(dir_db)

    @skip
    @mock.patch.dict(os.environ, env)
    def test_process_taxonomy_entrez(self):
        self.c.process_taxonomy_entrez('9606')


    @skip
    @mock.patch.dict(os.environ, env)
    def test_split_gene_refseq_uniprotkb_collab(self):
        self.c.split_gene_refseq_uniprotkb_collab()


    @mock.patch.dict(os.environ, env)
    def test_get_fields(self):
        res = self.c.get_fields()