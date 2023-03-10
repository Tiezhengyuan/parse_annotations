
from typing import Iterable, Callable
import os
import json
from utils.commons import Commons
from utils.utils import Utils
from utils.file import File
from utils.dir import Dir
from utils.handle_json import HandleJson
from utils.jtxt import Jtxt
from parser.map_cache import MapCache

class Map(Commons):
    def __init__(self):
        super(Map, self).__init__()

    def get_map(self, infile:str, key2:str, func:Callable=None)->dict:
        '''
        gene uid ~ <terms>
        Note: local cache should exist
        '''
        map = {}
        handle = Jtxt(infile).read_jtxt()
        for key1, terms in handle:
            # print(uid, terms)
            rec = []
            for term in terms:
                if term.get(key2) not in (rec, '-', None):
                    if isinstance(term[key2], list):
                        rec += term[key2]
                    else:
                        rec.append(term[key2])
            map[key1] = rec if func is None else func(rec)
        return map


    def get_intra_map(self, infile:str, key1:str, key2:str)->dict:
        '''
        map key1~key2 within the uid list
        '''
        map = {}
        handle = Jtxt(infile).read_jtxt()
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