'''
Test class 
'''
from tests.helper import *
from utils.file import File


@ddt
class TestFile(TestCase):

    def setUp(self):
        self.rows_txt = os.path.join(DIR_DATA, 'rows.txt')
        with open(self.rows_txt, 'w') as f:
            rows = [ str(i) for i in range(10)]
            f.write('\n'.join(rows))

    @skip
    @data(
        [3, None, 4],
        [3, 1, 3],
    )
    @unpack
    def test_read_slice(self, rows, skip, expect):
        res = File(self.rows_txt).read_slice(rows, skip)
        assert len(list(res)) == expect

    @skip
    @data(
        [None, ['0',]],
        [3, ['0','1','2']],
    )
    @unpack
    def test_read_top_lines(self, rows, expect):
        res = File(self.rows_txt).read_top_lines(rows)
        assert res == expect

    def test_read_dump_file(self):
        infile = os.path.join(env['DIR_DOWNLOAD'], 'NCBI', 'taxonomy', 'names.dmp')
        File(infile).read_dump_file()