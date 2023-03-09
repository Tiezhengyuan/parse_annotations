
from typing import Iterable, Callable
import os
import json
from utils.commons import Commons
from utils.utils import Utils
from utils.file import File
from utils.dir import Dir
from utils.handle_json import HandleJson
from utils.jtxt import Jtxt
from annotation.map_cache import MapCache

class Map(Commons):
    def __init__(self):
        super(Map, self).__init__()

    def get_map0(self, file_name:str, key1_name:str, key2:str, func:Callable=None)->tuple:
        '''
        gene uid ~ <terms>
        Note: local cache should exist
        '''
        map = {}
        tax_id = file_name.split('_', 2)[0]
        tax_dir = Dir.cascade_dir(self.dir_map, tax_id, self.cascade_num)
        infile = os.path.join(tax_dir, file_name)
        handle = Jtxt(infile).read_jtxt()
        for uid, terms in handle:
            # print(uid, terms)
            rec = []
            for term in terms:
                if term.get(key2) not in (rec, '-', None):
                    if isinstance(term[key2], list):
                        rec += term[key2]
                    else:
                        rec.append(term[key2])
            map[uid] = rec if func is None else func(rec)
        #save map
        MapCache([key1_name, key2,]).save_taxonomy_map(map, tax_id)
        return map


    def get_intra_map(self, jtxt_file:str, key1:str, key2:str)->dict:
        '''
        map key1~key2 within the uid list
        '''
        map = {}
        handle = Jtxt(jtxt_file).read_jtxt()
        for _, terms in handle:
            for term in terms:
                if key1 in term and key2 in term:
                    # k and v could be list, str, or tuple etc
                    k, v = term[key1], term[key2]
                    if isinstance(k, list):
                        for sub in k:
                            Utils.update_dict(map, sub, v)    
                    else:
                        Utils.update_dict(map, k, v)
        return map

    def build_taxonomy_map(self, file_name:str, key1:str, key2:str, func:Callable=None):
        tax_id = file_name.split('_')[0]
        tax_dir = Dir.cascade_dir(self.dir_map, tax_id, self.cascade_num)
        jtxt_file = os.path.join(tax_dir, file_name)
        # parse data and build map
        map = self.get_intra_map(jtxt_file, key1, key2)
        if func:
            func(map)
        #save map
        map_file = MapCache([key1, key2,]).save_taxonomy_map(map, tax_id)
        return map, map_file
    
    def map_term(self, handle:Iterable, key1:list, key2:list):
        '''
        map key1 ~ key2
        '''
        map = {}
        for rec in handle:
            val1 = Utils.get_deep_value(rec, key1)
            val2 = Utils.get_deep_value(rec, key2)
            # print(val1, val2)
            if val1 and val2:
                for k in val1:
                    map[k] = val2
        return map
    
    
    def switch_map(self, keys:list)->str:
        '''
        switch key-value of a certain map cache
        '''
        map = MapCache(keys).get_map_cache()
        return MapCache(keys[:-2] + keys[-2:][::-1]).save_map(
            Utils.switch_key_value(map),
            os.path.dirname(self.get_map_path(keys))
        )