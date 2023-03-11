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
    def __init__(self, key1:str, key2:str):
        super(MapCache, self).__init__()
        self.key1 = key1
        self.key2 = key2

    def save_map(self, map:dict, outdir:str=None)->str:
        '''
        save map dictionary to cache directory
        '''
        # save map
        if outdir is None: outdir = self.dir_cache
        dir_map = os.path.join(outdir, 'map')
        Dir(dir_map).init_dir()
        outfile = os.path.join(dir_map, f"{self.key1}_{self.key2}.json")
        HandleJson(outfile).save_json(map)

        # update map path stored in self.json_cache
        outfile = os.path.join(outdir, self.json_cache)
        local_cache_path = HandleJson(outfile).to_dict()
        Utils.init_dict(local_cache_path, [self.key1, self.key2], outfile)
        HandleJson(outfile).save_json(local_cache_path)


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


