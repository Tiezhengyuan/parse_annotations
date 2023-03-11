'''
Test class ProcessGene
'''
from tests.helper import *
from parser.parse import Parse


@ddt
class TestParse(TestCase):
    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.df = pd.DataFrame({
            'id': [1,2,3,4,5,6],
            's1': [4,5,78,3,0,40],
            's2': [14,25,8,31,100,20],
        })

    @mock.patch.dict(os.environ, env)
    @mock.patch('parser.map_cache.MapCache.get_map')
    @data(
        ['-','acc', 'id', ['ab', 'c', '', '', 'a|b', ''] ],
    )
    @unpack
    def test_add_parsing(self, key1, key2, col, expect, mock_map):
        mock_map.return_value = {
            2: 'c',
            1: 'ab',
            5: ['a', 'b'],
            30: 'e'
        }
        c = Parse(self.df)
        setattr(c, 'key1', key1)
        setattr(c, 'key2', key2)
        setattr(c, 'column_name', col)
        c.add_parsing()
        assert list(c.df[key2]) == expect


    @mock.patch.dict(os.environ, env)
    @mock.patch('os.listdir')
    @mock.patch('utils.handle_json.HandleJson.read_json')
    @data(
        [{'a':{'b':'4'}}, 'human', {'a':{'b':'4'}}],
        # no map data
        [{}, None, {}],
        # wrong project name
        [{'a':{'b':'4'}}, 'worng_project', {}],
    )
    @unpack
    def test_declare_project(self, map, project, expect, mock_json, mock_list):
        mock_json.return_value = map
        mock_list.return_value=['human',]
        c = Parse(self.df)
        c.declare_project(project)
        assert getattr(c, 'map_path') == expect
        
    @mock.patch.dict(os.environ, env)
    @data(
        ['id', 'ID', 'id'],
        ['id', 'wrong', None],
        ['wrong', 'ID', None],
    )
    @unpack
    def test_parse_column(self, column_name, key1, expect):
        c = Parse(self.df)
        setattr(c, 'map_path', {'ID':{'acc': '-'}})
        c.parse_column(column_name, key1)
        assert getattr(c, 'column_name') == expect


