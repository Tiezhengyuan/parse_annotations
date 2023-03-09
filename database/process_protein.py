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
    
    def __init__(self,  debugging:bool=None):
        super(ProcessProtein, self).__init__()
        self.debugging = False if debugging is None else True
        self.expasy_file = os.path.join(self.dir_cache, 'expasy.tjxt')


    def process_protein(self):
        '''
        protein annotations
        '''
        # split Uniprot-Sprot.dat
        names = ProcessGene.get_split_names()
        split_files = {i:os.path.join(self.dir_cache, f"expasy.tmp.{i}") for i in names}
        self.split_expasy_records(split_files)
        # delete temporary files
        File.delete_tmp_files(split_files.values())

        # split gene_refseq_uniprotkb_collab
        # ProcessGene().split_gene_refseq_uniprotkb_collab()

        # parse NCBI protein accession
        self.parse_ncbi_protein(split_files)
        # delete temporary files
        File.delete_tmp_files(split_files.values())


    def split_expasy_records(self, split_files:list):
        handle = Swissprot().parse_protein()
        for rec in handle:
            for item in rec.get('accessions', []):
                acc = item.get('UniProtKB_protein_accession')
                if acc:
                    prefix = ProcessGene.convert_prefix(acc)
                    outfile = split_files[prefix]
                    Jtxt(outfile).append_jtxt(rec)
                    break
            if len(rec.get('accessions', [])) > 1:
                print(rec)


    def parse_ncbi_protein(self, split_files:list):
        with open(self.expasy_file, 'wt') as f:
            for filename, expasy_tmp in split_files.items():
                # get Series of ncbi accessions
                accessions = ProcessGene().get_ncbi_acc(filename)
                handle = Jtxt(expasy_tmp).read_jtxt()
                for rec in handle:
                    for item in rec.get('accessions', []):
                        acc = item.get('UniProtKB_protein_accession')
                        if acc:
                            match = accessions.get(acc)
                            if match is not None:
                                match = list(match) if type(match)==pd.Series else [match,]
                                Utils.update_dict(item, "protein_accession.version", match)
                                print('##matched', item)
                    # print(json.dumps(rec))
                    f.write(json.dumps(rec)+'\n')




