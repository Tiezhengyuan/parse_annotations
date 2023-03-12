
from typing import Iterable, Callable
import os
import json
from pAnnot.utils.commons import Commons
from pAnnot.utils.utils import Utils
from pAnnot.utils.file import File
from pAnnot.utils.dir import Dir
from pAnnot.utils.handle_json import HandleJson
from pAnnot.utils.jtxt import Jtxt
from pAnnot.parser.map_cache import MapCache

class DetectMap(Commons):
    def __init__(self, infile:str=None):
        super(DetectMap, self).__init__()
        self.infile = infile

    def get_fields(self):
        handle = Jtxt(self.infile).read_jtxt()
        rec = next(handle)
        pool = [[i,] for i in list(rec)]
        paths = []
        while pool:
            keys = pool.pop(0)
            val = Utils.get_deep_value(rec, keys)
            if isinstance(val, dict):
                for k in val:
                    pool.append(keys + [k,])
            elif isinstance(val, list) and len(val) > 0:
                if isinstance(val[0], dict):
                    for k in val[0]:
                        pool.append(keys + [k,])
                else:
                    if set(keys) not in paths:
                        paths.append(set(keys))
            else:
                if set(keys) not in paths:
                    paths.append(set(keys))
        del handle
        fields = list(set([list(i)[-1] for i in paths]))
        return paths, fields

    def get_map(self, key2:str, func:Callable=None)->dict:
        '''
        gene uid ~ <terms>
        Note: local cache should exist
        '''
        map = {}
        handle = Jtxt(self.infile).read_jtxt()
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


    def get_intra_map(self, key1:str, key2:str)->dict:
        '''
        map key1~key2 within the uid list
        '''
        map = {}
        handle = Jtxt(self.infile).read_jtxt()
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