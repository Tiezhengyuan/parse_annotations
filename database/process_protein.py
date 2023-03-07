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
    
    def __init__(self, debugging:bool=None):
        super(ProcessProtein, self).__init__()
        self.debugging = False if debugging is None else True
        self.expasy_file = os.path.join(self.dir_cache, 'expasy.tjxt')


    def process_protein(self):
        '''
        protein annotations
        '''
        # startup: Uniprot-Sprot
        with open(self.expasy_file, 'wt') as f:
            handle = Swissprot().parse_protein()
            for rec in handle:
                # print(json.dumps(rec))
                f.write(json.dumps(rec)+'\n')
        
        # parse NCBI protein accession
        ProcessGene().split_gene_refseq_uniprotkb_collab()
        self.parse_ncbi_protein()

    def parse_ncbi_protein(self):
        tmp = self.expasy_file + '.tmp'
        tmp_in = self.expasy_file + '.tmp_in'
        shutil.copyfile(self.expasy_file, tmp_in)
        tmp_other = self.expasy_file + '.tmp_other'
        split_filenames = ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', \
                'A6', 'A7', 'A8', 'A9', 'P1', 'P2']
        with open(tmp, 'wt') as f:
            for filename in split_filenames:
                print(filename)
                # get Series of ncbi accessions
                accessions = ProcessGene().get_ncbi_acc(filename)
                with open(tmp_other, 'wt') as f_other:
                    handle = Jtxt(tmp_in).read_jtxt()
                    for rec in handle:
                        to_other = False
                        for item in rec.get('accessions', []):
                            acc = item.get('UniProtKB_protein_accession')
                            if acc:
                                prefix = ProcessGene.convert_prefix(acc)
                                if prefix == filename:
                                    match = accessions.get(acc)
                                    if match is not None:
                                        match = list(match) if type(match)==pd.Series else [match,]
                                        Utils.update_dict(item, "protein_accession.version", match)
                                        print('##matched', item)
                                else:
                                    to_other = True
                        if to_other:
                            f_other.write(json.dumps(rec) + '\n')
                        else:
                            f.write(json.dumps(rec) + '\n')
                # switch
                tmp_in, tmp_other = tmp_other, tmp_in
            else:
                # usually the file tmp_in should be empty
                handle = Jtxt(tmp_in).read_jtxt()
                for rec in handle:
                    Jtxt(tmp).append_jtxt(rec)
        # remove temporary files
        if self.debugging is False:
            os.remove(tmp_in)
            os.remove(tmp_other)
            os.remove(self.expasy_file)
            os.rename(tmp, self.expasy_file)


