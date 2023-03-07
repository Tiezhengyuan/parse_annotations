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

    def save_jtxt(self, input:dict, is_online=False):
        '''
        save value of a key-value as one line
        '''
        if not isinstance(input, dict):
            return False
        try:
            with open(self.file, 'w') as f:
                if is_online:
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

   
    def merge_jtxt(self, index_key:str, input:dict, debugging=False):
        '''
        in-place replace/merge/insert/add
        for input: the value of a key-value is one line
        '''
        if not isinstance(input, dict):
            return False
        if not os.path.isfile(self.file):
            return self.save_jtxt(input)
        else:
            tmp = self.file + '.tmp'
            with open(tmp, 'wt') as f:
                handle = self.read_jtxt()
                for origin_dict in handle:
                    index = origin_dict.get(index_key)
                    if index and input.get(index):
                        origin_dict = Utils.merge_dict(origin_dict, input[index])
                        del input[index]
                    f.write(json.dumps(origin_dict)+'\n')
                #append new value
                if input:
                    for _,v in input.items():
                        f.write(json.dumps(v)+'\n')
            #
            if debugging is False:
                if os.path.isfile(self.file):
                    os.remove(self.file)
                os.rename(tmp, self.file)
                print(f"{self.file} is updated by {__name__}.merge_jtxt().")
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
