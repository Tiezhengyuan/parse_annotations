'''
the class parse is used for interactive-programing in python env
'''
from copy import deepcopy
import itertools
import os
import sys
import json
from typing import Iterable, Callable
import pandas as pd

from pAnnot.utils.commons import Commons
from pAnnot.utils.file import File
from pAnnot.utils.dir import Dir
from pAnnot.utils.utils import Utils
from pAnnot.utils.jtxt import Jtxt
from pAnnot.utils.handle_json import HandleJson
from pAnnot.parser.map_cache import MapCache

# print(f"{}.", file=sys.stdout)
class Parse(Commons):
    def __init__(self, df:pd.DataFrame):
        super(Parse, self).__init__()
        self.df = df
        self.map_path, self.column_name, self.key1, \
            self.key2 = {}, None, None, None

    def declare_project(self, project_name:str):
        '''
        step1
        '''
        projects = os.listdir(self.dir_cache)
        if project_name in projects:
            self.project_name = project_name
            infile = os.path.join(self.dir_cache, self.project_name, self.json_cache)
            map_path = HandleJson(infile).to_dict()
            if map_path:
                self.map_path = map_path
            else:
                print(f"Error: no map data showed as the file {infile}")    
        else:
            print(f"Error: project_name should be selected from {projects}")

    def parse_column(self, column_name:str, key1:str):
        '''
        step2
        '''
        if self.map_path:
            if key1 in list(self.map_path) and column_name in self.df.columns:
                self.key1 = key1
                self.column_name = column_name
                print(f"OK! The column {column_name} is parsed with {self.key1}")
            else:
                print(f"Error: parsing key name should be selected from {list(self.map_path)}")
  
    def parse_term(self, key2:str):
        if self.key1 is None:
            print(f"Please run the method specify_gene_identifer(<gene identifier>) firstly.")
        res = self.map_path[self.key1].get(key2)
        if len(res) == 1:
            self.key2 = key2
            print(f"OK! {key2} is specified. The next,  parse terms using the method parse()...")
        elif res == []:
            print(f"Error: No such a term is detected.")
            print(f"You might as well use search_term(<term>) to get a correct term.")
        else:
            print(f"Error: Mutliple terms are detected. {res}")
            print(f"You might as well specify one of them.")
    
    def add_parsing(self):
        def _func(x, map):
            if x in map:
                if isinstance(map[x], list):
                    if len(map[x])==1:
                        return map[x][0]
                    return '|'.join(map[x])
                return map[x]
            return ''
        if self.key1 and self.key2:
            map = MapCache(self.key1, self.key2).get_map()
            self.df[self.key2] = self.df[self.column_name].apply(
                lambda x: _func(x, map))

    

    
    def search_term(self, term:str):
        pass

