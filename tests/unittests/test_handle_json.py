'''
Test class 
'''
from tests.helper import *

from utils.handle_json import HandleJson


infile = os.path.join(DIR_DATA, 'example.json')

@ddt
class TestHandleJson(TestCase):
    

    def setUp(self):
        with open(infile, 'w') as f:
            data = {
                'a':1,
            }
            json.dump(data, f, indent=4, sort_keys=True)

    @data(
        [infile, 'a', 1],
        ['wrong_file', None, None],
    )
    @unpack
    def test_read_json(self, infile, expect_key, expect_value):
        res = HandleJson(infile).read_json()
        first = next(res)
        if first:
            assert   first[0] == expect_key
            assert   first[1] == expect_value
        else:
            assert   first == expect_key

    @data(
        [{'a':4}, {'a':4}],
        [{}, {'a':1}],
        [{'b':2}, {'a':1,'b':2}],
    )
    @unpack
    def test_update_json(self, input, expect):
        HandleJson(infile).update_json(input)
        with open(infile, 'r') as f:
            res = json.load(f)
            assert res == expect


    @data(
        [['a'], [1]],
        [['b', 'a'], [2]],
        [['b', 'c'], [1,2]],
        [['b', 'd'], [{'e':[]}]],
        [['b', 'd','e'], []],
        [['c','a'], [1,2]],
        [['wrong'], None],
    )
    @unpack
    def test_update_json(self, keys, expect):
        with open(infile, 'r') as f:
            data = {
                'a':1,
                'b':{'a':2, 'c':[1,2], 'd':{'e':[]}},
                'c':[{'a':1},{'a':2},{'c':3},],
            }
            HandleJson(infile).save_json(data)
        res = HandleJson(infile).search_value(keys)
        print(res)
        assert res == expect
