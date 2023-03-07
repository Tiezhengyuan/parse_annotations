'''
Test class ConnectNCBI
'''
from tests.helper import *
from connector.connect_ncbi import ConnectNCBI

@ddt
class TestConnectNCBI(TestCase):

    def setUp(self):
        self.c = ConnectNCBI()

    @skip
    @mock.patch.dict(os.environ, env)
    def test_download_gene_data(self):
        self.c.download_gene_data()


    @mock.patch.dict(os.environ, env)
    def test_download_pubmed(self):
        self.c.download_pubmed()


