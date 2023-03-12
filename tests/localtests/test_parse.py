'''
Test class ProcessGene
'''
from tests.helper import *
from pAnnot.parser.parse import Parse


@ddt
class TestParse(TestCase):

    @mock.patch.dict(os.environ, env)
    def test_parse_1(self):
        df = pd.DataFrame({
            'id': ['1','2','3','4','5','6'],
            's1': [4,5,78,3,0,40],
            's2': [14,25,8,31,100,20],
        })
        df.index = df['id']
    
        c = Parse(df)
        c.declare_project('human')
        c.parse_column('id', 'GeneID')

        # parse symbol
        c.parse_term('Symbol')
        c.add_parsing()
        assert df.loc['1', 'Symbol'] == 'A1BG'
        assert df.loc['4', 'Symbol'] == ''

        c.parse_term('Ensembl_rna_identifier')
        c.add_parsing()
        assert df.loc['2', 'Ensembl_rna_identifier'] == 'ENST00000318602.12'

    @mock.patch.dict(os.environ, env)
    def test_parse_2(self):
        df = pd.DataFrame({
            'id': ["NM_000016.6", "NM_000023.4","NM_000224.3",\
                   "NM_000265.7","NM_000257.4","NM_000726.5"],
            's1': [4,5,78,3,0,40],
            's2': [14,25,8,31,100,20],
        })
        df.index = df['id']
    
        c = Parse(df)
        c.declare_project('human')
        c.parse_column('id', 'RNA_nucleotide_accession.version')
        c.parse_term('GO_ID')
        c.add_parsing()
        assert 'GO:0005634' in df.loc['NM_000016.6', 'GO_ID']

    @mock.patch.dict(os.environ, env)
    def test_parse_3(self):
        df = pd.DataFrame({
            'id': ["NM_000016.6", "NM_000023.4","NM_000224.3",\
                   "NM_000265.7","NM_000257.4","NM_000726.5"],
            's1': [4,5,78,3,0,40],
            's2': [14,25,8,31,100,20],
        })
    
        c = Parse(df)
        c.declare_project('human')
        c.parse_column('id', 'RNA_nucleotide_accession.version')
        c.parse_term("chromosome")
        c.add_parsing()
        c.parse_term("start_position_on_the_genomic_accession")
        c.add_parsing()
        c.parse_term("end_position_on_the_genomic_accession")
        c.add_parsing()

        print(df[['id', "chromosome", "start_position_on_the_genomic_accession", \
                "end_position_on_the_genomic_accession"]])
