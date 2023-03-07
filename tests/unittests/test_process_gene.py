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
    def test_parse_taxonomy_gene2(self):
        handle = self.c.parse_taxonomy_gene2('gene2accession', '9606')
        res = next(handle)
        assert '1' in res


    @skip
    @mock.patch.dict(os.environ, env)
    def test_feed_redis(self):
        self.c.feed_redis()

    @data(
        ['A0A1J0MUK8', 'A0', 'AP_000046.1'],
        ['P19119', 'P1', 'AP_000032.1'],
        ['Q96685', 'Q9',  ['AP_000056.1', 'AP_000056']],
        # no detection
        ['wrong_acc', 'P1', None],
        ['P19119', 'wrong', None],
    )
    @unpack
    @mock.patch.dict(os.environ, env)
    def test_parse_ncbi_acc(self, acc, prefix, expect):
        infile = os.path.join(DIR_DATA, 'gene_refseq_uniprotkb_collab.txt')
        accessions = self.c.parse_ncbi_acc(infile)
        res = accessions.get(prefix, {}).get(acc)
        if type(res) == pd.Series:
            assert  list(res) == expect
        else:
            assert res == expect