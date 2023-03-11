'''
Test class Check
'''
from tests.helper import *
from pAnnot.parser.check import Check


@ddt
class TestCheck(TestCase):
    
    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = Check()

    @data(
        [None, True],
        [env['DIR_DOWNLOAD'], True],
        ['wrong_dir', False],
    )
    @unpack
    @mock.patch.dict(os.environ, env)
    def test_entrez_gene_download(self, input, expect):
        res = self.c.entrez_gene_download(input)
        assert res == expect


    @data(
        [None, True],
        [env['DIR_DOWNLOAD'], True],
        ['wrong_dir', False],
    )
    @unpack
    @mock.patch.dict(os.environ, env)
    def test_swissprot_download(self, input, expect):
        res = self.c.swissprot_download(input)
        assert res == expect
    
    @mock.patch.dict(os.environ, env)
    def test_get_projects(self):
        res = self.c.get_projects()
        assert len(res) >= 1
