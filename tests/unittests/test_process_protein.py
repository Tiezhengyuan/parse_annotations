'''
Test class ProcessProtein
'''
from tests.helper import *
from database.process_protein import ProcessProtein


@ddt
class TestProcessProtein(TestCase):
    
    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = ProcessProtein(debugging=True)

    @mock.patch.dict(os.environ, env)
    @mock.patch('database.process_gene.ProcessGene.parse_acc')
    @mock.patch('utils.jtxt.Jtxt.read_jtxt')
    def test_parse_ncbi_protein(self, mock_jtxt, mock_parse):
        mock_jtxt.return_value = iter([
            {"accessions": [{"UniProtKB_protein_accession": "Q6GZX4"},
                {"UniProtKB_protein_accession": "Q64843"}], },
        ])
        mock_parse.return_value = {
            'AP': pd.Series(['AP_000010.1', 'AP_000013.1',
                'AP_000021.1', 'AP_000022.1', 'AP_000023.1'],
                index= ['Q96624', 'Q96629', 'Q64842', 'Q64843', 'Q64844']
            )
        }
        self.c.parse_ncbi_protein()

