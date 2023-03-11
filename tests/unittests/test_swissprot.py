'''
Test class 
'''
from tests.helper import *
from pAnnot.database.swissprot import Swissprot


@ddt
class TestSwissProt(TestCase):
    
    @mock.patch.dict(os.environ, env)
    def test_parse_protein(self):
        infile = os.path.join(DIR_DATA, 'uniprot_sprot.dat')
        c = Swissprot()
        setattr(c, 'uniprot_sprot.dat', infile)
        handle = c.parse_protein()
        res = next(handle)
        assert 'accessions' in res


