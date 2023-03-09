from typing import Iterable, Callable
import os
import json
from utils.commons import Commons
from utils.utils import Utils
from utils.file import File
from utils.dir import Dir
from utils.handle_json import HandleJson
from utils.jtxt import Jtxt

class MapCache(Commons):
    def __init__(self, keys:list=None):
        super(MapCache, self).__init__()
        self.keys = keys

    def save_map(self, map:dict, outdir:str=None)->str:
        '''
        save map dictionary to cache directory
        '''
        if len(self.keys) < 2:
            return None
        # save map
        if outdir is None: outdir =  self.dir_cache
        Dir(outdir).init_dir()
        outfile = os.path.join(outdir, f"{self.keys[-2]}_{self.keys[-1]}.json")
        HandleJson(outfile).save_json(map)

        # update map path stored in self.json_cache
        local_cache_path = HandleJson(self.json_cache).to_dict()
        Utils.init_dict(local_cache_path, self.keys, outfile)
        HandleJson(self.json_cache).save_json(local_cache_path)
        return outfile   

    def save_taxonomy_map(self, map:dict, tax_id:str)->str:
        self.keys = ['taxonomy', tax_id, ] + self.keys
        tax_dir = Dir.cascade_dir(self.dir_map, tax_id, self.cascade_num)
        return self.save_map(map, tax_dir)

    def read_map(self)->Iterable:
        '''
        read map dictionary using keys in list
        for example: {'a':{'b':4}}: keys = ['a', 'b'], return 4
        '''
        c = HandleJson(self.json_cache)
        json_path = c.search_value(self.keys)
        return HandleJson(json_path).read_json()

    def get_map(self)->dict:
        '''
        get map cache as dict
        '''
        c = HandleJson(self.json_cache)
        json_path = c.search_value(self.keys)
        try:
            with open(json_path[0], 'r') as f:
                return json.load(f)
        except Exception as e:
            print(e)
        return {}

    def get_map_path(self)->dict:
        '''
        get path of a map cache from self.json_cache
        '''
        c = HandleJson(self.json_cache)
        return c.search_value(self.keys)

    def scan_map_meta(self)->list:
        HandleJson(self.json_cache).read_json()


