from typing import Iterable, Callable
import os
import json
from pAnnot.utils.commons import Commons
from pAnnot.utils.utils import Utils
from pAnnot.utils.file import File
from pAnnot.utils.dir import Dir
from pAnnot.utils.handle_json import HandleJson
from pAnnot.utils.jtxt import Jtxt

class MapCache(Commons):
    def __init__(self, project_name: str, key1:str, key2:str):
        super().__init__()

        self.project_name = project_name
        self.dir_project = os.path.join(self.dir_cache, self.project_name)
        self.dir_map = os.path.join(self.dir_project, 'map')
        Dir(self.dir_map).init_dir()
        self.file_json_cache = os.path.join(self.dir_project, self.json_cache)
        self.key1 = key1
        self.key2 = key2

    def save_map(self, map:dict)->str:
        '''
        save map dictionary to cache directory
        '''
        # save map
        map_json = os.path.join(self.dir_map, f"{self.key1}_{self.key2}.json")
        HandleJson(map_json).save_json(map)

        # update map path stored in self.json_cache
        local_cache_path = HandleJson(self.file_json_cache).to_dict()
        Utils.init_dict(local_cache_path, [self.key1, self.key2], map_json)
        HandleJson(self.file_json_cache).save_json(local_cache_path)


    def get_map(self)->dict:
        '''
        get map as dict
        '''
        c = HandleJson(self.file_json_cache)
        json_path = c.search_value([self.key1, self.key2])
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
        c = HandleJson(self.file_json_cache)
        return c.search_value(self.keys)

    def scan_map_meta(self)->list:
        HandleJson(self.file_json_cache).read_json()


