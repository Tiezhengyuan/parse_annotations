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

from utils.commons import Commons
from utils.file import File
from utils.dir import Dir
from utils.utils import Utils
from utils.jtxt import Jtxt
from utils.handle_json import HandleJson
from parser.map import Map
from parser.map_gene import MapGene
from parser.map_protein import MapProtein
from parser.map_cache import MapCache

# print(f"{}.", file=sys.stdout)
class Parse(Commons):
    def __init__(self, df:pd.DataFrame):
        super(Parse, self).__init__()
        self.df = df
        self.key1, self.key2 = None, None


    def search_term(self, term:str):
        pass


    def specify_gene_identifier(self, key1:str):
        pool = ['NCBI Gene ID', 'NCBI RefSeq Genomic DNA accession', 'Ensembl Gene Identifier',]
        if key1 not in pool:
            print(f"Error: Please select one from {pool}.")
        self.key1 = key1
        print(f"OK! {key1} is specified. The next, specify a " + 
                "parsing term using the method parse_term()...")

    def specify_term(self, key2:str):
        if self.key1 is None:
            print(f"Please run the method specify_gene_identifer(<gene identifier>) firstly.")
        res = self.search_term(key2)
        if len(res) == 1:
            self.key2 = key2
            print(f"OK! {key2} is specified. The next,  parse terms using the method parse()...")
        elif res == []:
            print(f"Error: No such a term is detected.")
            print(f"You might as well use search_term(<term>) to get a correct term.")
        else:
            print(f"Error: Mutliple terms are detected. {res}")
            print(f"You might as well specify one of them.")
    
    def parse_term(self):
        if self.key1 and self.key2:
            map_df = MapCache().get_map(self.key1, self.key2)
    

    
