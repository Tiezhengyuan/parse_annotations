"""
bio-broker define a customary format file that combines json and text
jtxt format could hanlde huge data up to ~GB due RAM limits
"""
from typing import Iterable
import json
import os
from utils.utils import Utils
from utils.commons import Commons

class Jtxt(Commons):
    def __init__(self, file:str):
        super(Jtxt, self).__init__()
        self.file = file

    def print_jtxt(self, line_num=1):
        '''
        for debugging
        '''
        with open(self.file, 'rt') as f:
            n = 1
            for line in f:
                rec = json.loads(line)
                if n == line_num:
                    print(json.dumps(rec, indent=4))
                    break


    def read_jtxt(self)->Iterable:
        '''
        return one line one dict
        '''
        with open(self.file, 'rt') as f:
            for line in f:
                records = json.loads(line)
                yield records

    def save_jtxt(self, input:dict, is_oneline=False):
        '''
        save value of a key-value as one line
        '''
        if not isinstance(input, dict):
            return False
        try:
            with open(self.file, 'w') as f:
                if is_oneline is True:
                    f.write(json.dumps(input)+'\n')
                else:
                    for _,v in input.items():
                        f.write(json.dumps(v) + '\n')
            return True
        except Exception as e:
            print(e)
            return False

    def append_jtxt(self, input:dict):
        '''
        append the input dict as the last line
        '''
        with open(self.file, 'a+') as f:
            line = json.dumps(input)
            f.write(line+'\n')
            # print(f"Append data into {self.file}")
        return True

   
    def merge_jtxt(self, index_key:str, input:dict, outfile:str):
        '''
        in-place replace/merge/insert/add
        for input: the value of a key-value is one line
        '''
        if not isinstance(input, dict):
            return False
        with open(outfile, 'wt') as f:
            handle = self.read_jtxt()
            for origin in handle:
                index = origin.get(index_key)
                if index and input.get(index):
                    origin = Utils.merge_dict(origin, input[index])
                    if isinstance(origin[index_key], list) and len(origin[index_key])==1:
                        origin[index_key] = origin[index_key][0]
                    del input[index]
                f.write(json.dumps(origin)+'\n')
            #append new value
            if input:
                for _,v in input.items():
                    f.write(json.dumps(v)+'\n')
        try:
            os.remove(self.file)
        except Exception as e:
            print(e)
        return True

        
    def search_jtxt(self, keys:list):
        if not keys: return []
        res = []
        handle = self.read_jtxt()
        for record in handle:
            val = Utils.get_deep_value(record, keys)
            if val not in (res, None, [], {}):
                res.append(val)
        return res
