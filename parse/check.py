'''
Confirm if current configurations and local data are ready for further work.
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

# print(f"{}.", file=sys.stdout)
class Check(Commons):
    def __init__(self):
        super(Check, self).__init__()
    
    def entrez_gene_download(self, dir_download:str=None)->bool:
        '''
        gene data from NCBI
        '''
        print("\nCheck if local data from NCBI-Entrez are available...", file=sys.stdout)
        if dir_download:
            self.dir_download = dir_download
        if os.path.isdir(self.dir_download):
            # gene data from NCBI
            this_dir = os.path.join(self.dir_download, 'NCBI', 'gene', 'DATA')
            file_names = ['gene2accession', 'gene2refseq', 'gene2pubmed', \
                'gene2go', 'gene2ensembl', 'gene_info', 'gene_group', \
                'gene_history', 'gene_neighbors', 'gene_orthologs', ]
            tag = 1
            for name in file_names:
                path = os.path.join(this_dir, f"{name}.gz")
                if not os.path.isfile(path):
                    print(f"Warning: Cannot detect {name} in {this_dir}.", file=sys.stdout)
                    tag = 0
            else:
                if tag == 1:
                    print(f"GOOD: All source data {file_names} " + \
                        f"are detected in {this_dir}.", file=sys.stdout)
                    return True
        else:
            print(f"Warning: The direcotry {self.dir_download} " + \
                "does not exist.", file=sys.stdout)
        return False

    def swissprot_download(self, dir_download:str=None)->bool:
        '''
            protein data from SwissProt - UniProt
        '''
        print("\nCheck if local data from ExPASy-SwissProt are available...", file=sys.stdout)
        if dir_download:
            self.dir_download = dir_download
        if os.path.isdir(self.dir_download):
            this_dir = os.path.join(self.dir_download, 'expasy', 'swiss-prot', 'release')
            file_names = ['uniprot_sprot.dat', 'uniprot_trembl.dat']
            tag = 1
            for name in file_names:
                path = os.path.join(this_dir, f"{name}.gz")
                if not os.path.isfile(path):
                    print(f"Warning: Cannot detect {name} in {this_dir}.", file=sys.stdout)
                    tag = 0
            else:
                if tag == 1:
                    print(f"GOOD: All source data {file_names} " + \
                        f"are detected in {this_dir}.", file=sys.stdout)
                    return True
        else:
            print(f"Warning: The direcotry {self.dir_download} " + \
                "does not exist.", file=sys.stdout)
        return False