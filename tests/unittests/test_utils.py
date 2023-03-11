'''
Test class Utils
'''
from tests.helper import *
from pAnnot.utils.utils import Utils

@ddt
class TestUtils(TestCase):


    @data(
        [{}, ['a',], {}, {'a':[]}],
        [{}, ['a',], None, {'a':[]}],
        [{'a':[]}, ['a',], {}, {'a':[]}],
        [{}, ['a','b','c'], '123', {'a':{'b':{'c':['123']}}}],
        [{}, ['a','b','c'], [], {'a':{'b':{'c':[]}}}],
        [{}, ['a','b','c'], None, {'a':{'b':{'c':[]}}}],
        [{'a':{'b':{'c':['1']}}}, ['a','b','c'], '1', {'a':{'b':{'c':['1']}}}],
        [{'a':{'b':{'c':['1']}}}, ['a','b','c'], '2', {'a':{'b':{'c':['1','2']}}}],
        [{'a':{'b':{'c':[]}}}, ['a','b','c'], '1', {'a':{'b':{'c':['1']}}}],
        [{'a':{'b':{'c':['1']}}}, ['a','e','c'], '1', {'a':{'b':{'c':['1']},'e':{'c':['1']}}}],
    )
    @unpack
    def test_insert_deep_dict(self, input, keys, default_val, expect):
        Utils.insert_deep_dict(input, keys, default_val)
        assert input == expect

    @data(
        [{}, ['a',], {}, {'a':{}}],
        [{}, ['a',], None, {'a':''}],
        [{'a':[]}, ['a',], {}, {'a':[]}],
        [{}, ['a','b','c'], [], {'a':{'b':{'c':[]}}}],
    )
    @unpack
    def test_init_dict(self, input, keys, default_val, expect):
        Utils.init_dict(input, keys, default_val)
        assert input == expect
    

    @data(
        [{}, 'a', 1, {'a':[1,]}],
        [{}, 'a', {'b':1}, {'a':[{'b':1},]}],
        [{}, '', 1, {}],
        [{}, '-', 1, {}],
        [{}, None, 1, {}],
        [{'a':[]}, 'a', 1, {'a':[1,]}],
        [{'a':[1,]}, 'a', 1, {'a':[1,]}],
        [{'a':[0,]}, 'a', 1, {'a':[0,1,]}],
        [{'a':[1,]}, 'b', 2, {'a':[1,],'b':[2,]}],
        # val is list
        [{}, 'a', [1,2], {'a':[1,2]}],
        [{'a':[1]}, 'a', [1,2], {'a':[1,2]}],
    )
    @unpack
    def test_update_dict(self, input, key, val, expect):
        Utils.update_dict(input, key, val)
        assert input == expect
    
    @data(
        [{'a':3}, ['a'], [3]],
        [{'a':{'b':{'c':3}}}, ['a', 'b', 'c'], [3]],
        [{'a':{'b':{'c':{'d':[1,2]}}}}, ['a', 'b', 'c'], [{'d':[1,2]}]],
        [[{'a':3},{'a':4}], ['a'], [3,4]],
        [{'b':[{'a':3},{'a':4},{'c':5}]}, ['b','a'], [3,4]],
        [{'b':[{'a':3},{'a':[4]},{'c':5}]}, ['b','a'], [3,4]],
        [{'b':[{'a':3},{'a':4},{'c':5}]}, ['a','b'], []],
        [{'b':[{'a':3},{'a':4},{'c':5}]}, [], []],
    )
    @unpack
    def test_get_deep_value(self, input, keys, expect):
        res = Utils.get_deep_value(input, keys)
        assert res == expect

    @data(
        [{'a':3}, {3:['a']}],
        [
            {'a':[1,2], 'b':[2,3]},
            {1: ['a'], 2:['a','b'], 3: ['b']}
        ],
        [
            {'a':1, 'b':'1', 'c':(1,'3'), 'd':{'d':0}, 'f':None},
            {1: ['a'], '1': ['b'], (1, '3'): ['c']}
        ],
        # alternative input
        [{}, {}],
        ['wrong', None],
    )
    @unpack
    def test_switch_key_value(self, input, expect):
        res = Utils.switch_key_value(input)
        assert res == expect
    
    @data(
        # add new
        [{'a':1}, {'b':[1,2]}, {'a': 1, 'b': [1, 2]}],
        # update
        [{'a':[1]}, {'a':[1,2]}, {'a': [1, 2]}],
        [{'a':[{'b':1}]}, {'a':[{'b':2}]}, {'a': [{'b': 1}, {'b': 2}]}],
        # 
        [{'a':1}, {}, {'a': 1}],
    )
    @unpack
    def test_mrege_dict(self, dict1, dict2, expect):
        res = Utils.merge_dict(dict1,dict2)
        assert res == expect
    
    @data(
        ['a', [10,]],
        # ['b', ['ab']],
        # ['c', [{'a':1}]],
        # ['wrong', []],
    )
    @unpack
    def test_search_series(self, key, expect):
        s = pd.Series([10, 'ab', {'a':1}, [2,3,4],20,],
            index=['a','b','c','d','e'])
        res = Utils.search_series(s, key)
        assert res == expect

    @skip
    @data(
        ['A0A1J0MUK8', ''],
        # ['Q96678', ''],
    )
    @unpack
    def test_parse_ncbi_acc(self, key, expect):
        infile = os.path.join(DIR_DATA, 'gene_refseq_uniprotkb_collab.txt')
        res = Utils.parse_ncbi_acc(infile)
        # assert res.get(key[:2]) == expect