'''
Test class 
'''
from tests.helper import *
from database.ncbi_entrez import NCBIEntrez


@ddt
class TestmyEntrez(TestCase):

    def setUp(self):
        self.c = NCBIEntrez()

    def test_get_db_infos(self):
        res = self.c.get_db_infos()
        pubmed = res['pubmed']
        assert pubmed['DbName'] == 'pubmed'
        assert int(pubmed['Count']) >1e6
        update = datetime.strptime(pubmed['LastUpdate'], "%Y/%m/%d %H:%M")
        assert update < datetime.now()