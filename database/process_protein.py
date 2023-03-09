'''
process gene/DATA
'''
from copy import deepcopy
import itertools
import os
import json
import shutil
from typing import Iterable, Callable
import pandas as pd

from utils.commons import Commons
from utils.file import File
from utils.dir import Dir
from utils.utils import Utils
from utils.jtxt import Jtxt
from utils.handle_json import HandleJson
from database.swissprot import Swissprot
from database.process_gene import ProcessGene


class ProcessProtein(Commons):
    
    def __init__(self,  project_name:str=None):
        super(ProcessProtein, self).__init__()
        self.project_name = 'project' if project_name is None else project_name
        self.expasy_file = os.path.join(self.dir_cache, project_name, 'expasy.tjxt')


    def process_taxonomy_protein(self, tax_id:str):
        '''
        protein annotations
        '''
        acc_pair = {}
        # split Uniprot-Sprot.dat
        counter = iter(range(10))
        tmp_out = os.path.join(self.dir_cache, f"expasy.tmp.{next(counter)}")
        with open(tmp_out, 'wt') as f:
            handle = Swissprot().parse_protein()
            for rec in handle:
                if tax_id in rec.get('tax_id', []):
                    for item in rec.get('accessions', []):
                        acc = item.get('UniProtKB_protein_accession')
                        if acc:
                            acc_pair[acc] = []
                    f.write(json.dumps(rec) + '\n')

        # parse uniprot_acc ~ ncbi_acc
        ProcessGene().parse_uniprot_acc_pair(acc_pair)

        # parse NCBI protein accession
        with open(self.expasy_file, 'wt') as f:
            handle = Jtxt(tmp_out).read_jtxt()
            for rec in handle:
                for item in rec.get('accessions', []):
                    acc = item.get('UniProtKB_protein_accession')
                    if acc:
                        match = acc_pair.get(acc)
                        if match not in (None, [], ''):
                            item["protein_accession.version"] = match
                            # print('##matched', item)
                f.write(json.dumps(rec)+'\n')
        # delete temporary files
        File.delete_tmp_files([tmp_out,])


