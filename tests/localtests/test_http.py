'''
Test class 
'''
from tests.helper import *
from connector.http import HTTP

class Test_(TestCase):

    def setUp(self):
        pass

    @mock.patch.dict(os.environ, env)
    def test_download_pdf(self):
        endpoint = 'http://eutils.ncbi.nlm.nih.gov'
        url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id=32563999&retmode=ref&cmd=prlinks'
        outfile = os.path.join(env['DIR_DOWNLOAD'], 'article')
        HTTP().download_pdf(url, outfile)