'''
Test class 
'''
from tests.helper import *
from pAnnot.utils.jtxt import Jtxt


@ddt
class TestJtxt(TestCase):
    jtxt_file = os.path.join(DIR_DATA, 'test_jtxt.jtxt')

    @mock.patch.dict(os.environ, env)
    def setUp(self):
        if os.path.isfile(self.jtxt_file):
            os.remove(self.jtxt_file)
        self.c = Jtxt(self.jtxt_file)

    @mock.patch.dict(os.environ, env)
    def tearDown(self):
        if os.path.isfile(self.jtxt_file):
            os.remove(self.jtxt_file)

    @data(
        [{}, [{}]],
        [
            {'a':1, 'b':[1,2], 'c':[{'a':1},{'a':2},], 'd':'', 'e':None},
            [{'a':1, 'b':[1,2], 'c':[{'a':1},{'a':2},], 'd':'', 'e':None}],
        ],
    )
    @unpack
    def test_save_jtxt(self, input, expect):
        self.c.save_jtxt(input, True)
        res = self.read_file()
        assert res == expect

    @data(
        [ ['a',], [[1]] ],
        [ ['b',], [[1,2]] ],
        [ ['c','a'], [[1,2]] ],
        [ ['d',], []],
        [ ['e',], []],
        # alternative cases
        [ [], []],
        [ ['wrong'], []],
        [ ['c', 'wrong'], []],
    )
    @unpack
    def test_search_jtxt(self, keys, expect):
        data = {
            'a':1,
            'b':[1,2],
            'c':[{'a':1},{'a':2},{'d':3},],
            'd':'',
            'e':None,
        }
        self.c.save_jtxt(data, True)
        res = self.c.search_jtxt(keys)
        assert res == expect


    def test_append_jtxt(self):
        # one line
        self.c.save_jtxt({1:{'a':0}})

        # two lines
        self.c.append_jtxt({2:{'a':1}})
        handle = self.c.read_jtxt()
        res = next(handle)
        assert res == {'a':0}
        assert len(list(handle)) == 1

        # three lines
        self.c.append_jtxt({3:{'b':2}})
        handle = self.c.read_jtxt()
        assert len(list(handle)) == 3

    def test_merge_jtxt(self):
        outfile = self.jtxt_file + '.tmp'
        #empty file
        self.c.merge_jtxt('id', {1:{'id':1,'name':'a'}}, outfile)
        os.rename(outfile, self.jtxt_file)
        res = self.read_file()
        assert res == [{'id': 1, 'name': 'a'}]

        #merge record
        self.c.merge_jtxt('id', {1:{'id':1,'age':4}}, outfile)
        os.rename(outfile, self.jtxt_file)
        res = self.read_file()
        assert res == [{'id': 1, 'name': 'a', 'age': 4}]

        # update record
        self.c.merge_jtxt('id', {1:{'id':1,'age':5}}, outfile)
        os.rename(outfile, self.jtxt_file)
        res = self.read_file()
        assert res == [{'id': 1, 'name': 'a', 'age': [4, 5]}]

        #add record
        self.c.merge_jtxt('id', {2:{'id':2,'name':'b'}}, outfile)
        os.rename(outfile, self.jtxt_file)
        res = self.read_file()
        assert res == [{'id': 1, 'name': 'a', 'age': [4, 5]}, {'id': 2, 'name': 'b'}]
    

    def read_file(self):
        with open(self.jtxt_file, 'r') as f:
            res = [json.loads(i) for i in f.readlines()]
            return res