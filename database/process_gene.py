'''
process gene/DATA
'''
from copy import deepcopy
import itertools
import os
import json
from typing import Iterable, Callable
import pandas as pd

from utils.commons import Commons
from utils.file import File
from utils.dir import Dir
from utils.utils import Utils
from utils.jtxt import Jtxt
from utils.handle_json import HandleJson


class ProcessGene(Commons):
    db = 'entrez'
    
    def __init__(self, project_name:str):
        super(ProcessGene, self).__init__()
        self.project_name = project_name
        # store local file is downloaded from NCBI FTP
        self.dir_source = os.path.join(self.dir_download, \
            'NCBI', 'gene', 'DATA')
        self.tmp_dir = os.path.join(self.dir_source, \
            "tmp_gene_refseq_uniprotkb_collab")
        Dir(self.tmp_dir).init_dir()

    def process_taxonomy_entrez(self, tax_id:str):
        '''
        process *.gz and store map in cache
        '''
        outdir = os.path.join(self.dir_cache, self.project_name)
        Dir(outdir).init_dir()
        outfile = os.path.join(outdir, f"{self.db}.jtxt")
        
        #parse and integrate gene data
        file_names = ['gene2accession', 'gene2refseq', 'gene2pubmed', \
            'gene2go', 'gene2ensembl', 'gene_info', 'gene_group', \
            'gene_history', 'gene_neighbors', 'gene_orthologs', ]
        for file_name in file_names[5:]:
            print(file_name)
            map = self.parse_taxonomy_gene2(file_name, tax_id)
            # save map to cache
            for m in map:
                Jtxt(outfile).merge_jtxt('GeneID', m)
        # decorate some data format
        self.format_gene(outfile)
        # parse uniprotkb
        self.parse_uniprotkb(outfile)


    def parse_taxonomy_gene2(self, file_name:str, tax_id:str)->Iterable:
        '''
        Gieven a taxonomy
        Map Entrez Gene identifiers(uid) to some identifiers 
        Note: local file should exist
        source file is downloaded from FTP
        '''
        map = {}
        # local file is downloaded from NCBI FTP
        mapfile = os.path.join(self.dir_source, f"{file_name}.gz")
        with File(mapfile).readonly_handle() as f:
            # get column names
            header = next(f).rstrip()
            if header.startswith('#'): header = header[1:]
            col_names = header.split('\t')
            # print(col_names)
            for line in f:
                items = line.rstrip().split('\t')
                this_tax_id, geneid = items[0], items[1]
                if this_tax_id == tax_id:
                    if geneid not in map:
                        map[geneid] = {
                            col_names[0]: this_tax_id,
                            col_names[1]: geneid,
                            file_name: [],
                        }
                    rec = {}
                    for k,v in zip(col_names[2:], items[2:]):
                        rec[k] = v.split('|') if '|' in v else v
                    map[geneid][file_name].append(rec)
                # export
                if len(map) >= 1e4:
                    output = deepcopy(map)
                    map = {}
                    yield output
            else:
                if map:
                    yield map

    def format_gene(self, outfile:str):
        tmp = outfile + '.tmp'
        with open(tmp, 'wt') as f:
            handle = Jtxt(outfile).read_jtxt()
            for rec in handle:
                for info_rec in rec.get("gene_info", []): 
                    ProcessGene.format_dbxrefs(info_rec)
                for go_rec in rec.get("gene2go", []):
                    if '|' in go_rec["PubMed"]:
                        go_rec["PubMed"] = go_rec["PubMed"].split('|')
                    elif go_rec["PubMed"] == '-':
                        go_rec["PubMed"] = []
                    else:
                        go_rec["PubMed"] = [go_rec["PubMed"],]
                # print(json.dumps(rec.get("gene2go", []), indent=4))
                if rec:
                    f.write(json.dumps(rec)+'\n')
        os.remove(outfile)
        os.rename(tmp, outfile)


    @staticmethod
    def format_dbxrefs(rec:dict):
        if rec.get("dbXrefs") not in (None, '-'):
            if isinstance(rec["dbXrefs"], str):
                rec["dbXrefs"] = [rec["dbXrefs"],]
            for item in rec["dbXrefs"]:
                name, id = item.split(':', 1)
                Utils.update_dict(rec, name, id)


    def parse_uniprotkb(self, outfile:str):
        #initialize acc_pair
        acc_pair = {}
        handle = Jtxt(outfile).read_jtxt()
        for rec in handle:
            for key1 in ("gene2accession", "gene2refseq", "gene2ensembl"):
                for item in rec.get(key1, []):
                    pro_acc = item.get("protein_accession.version", '-')
                    if pro_acc != '-':
                        acc_pair[pro_acc] = []

        # parse acc_pair
        infile = os.path.join(self.dir_source, "gene_refseq_uniprotkb_collab.gz")
        with File(infile).readonly_handle() as f:
            # skip the first line
            _ = next(f)
            for line in f:
                val1, val2 = line.rstrip().split('\t')
                if val1 in acc_pair and val2 not in acc_pair[val1]:
                    acc_pair[val1].append(val2)
        
        #update outfile
        tmp = outfile + '.tmp'
        with open(tmp, 'wt') as f:
            handle = Jtxt(outfile).read_jtxt()
            for rec in handle:
                for key1 in ("gene2accession", "gene2refseq", "gene2ensembl"):
                    for item in rec.get(key1, []):
                        pro_acc = item.get("protein_accession.version", '-')
                        if pro_acc != '-' and pro_acc in acc_pair:
                            Utils.update_dict(
                                item,
                                'UniProtKB_protein_accession',
                                acc_pair[pro_acc]
                            )
                            # print(json.dumps(rec[key1], indent=4))
                if rec:
                    f.write(json.dumps(rec)+'\n')
            os.remove(outfile)
            os.rename(tmp, outfile)


    def split_gene_refseq_uniprotkb_collab(self):
        '''
        source file: *_gene_refseq_uniprotkb_collab.gz
        '''
        infile = os.path.join(self.dir_source, "gene_refseq_uniprotkb_collab.gz")
        handle = File(infile).readonly_handle()
        header = next(handle)
        map, start = {}, 0
        for line in handle:
            start += 1
            items = line.split('\t')
            prefix = ProcessGene.convert_prefix(items[1])
            if prefix not in map:
                map[prefix] = [line]
            else:
                map[prefix].append(line)
            if start >= 1e5:
                for k, lines in map.items():
                    outfile = os.path.join(self.tmp_dir, k)
                    with open(outfile, 'a+') as f:
                        f.writelines(lines)
                map, start = {}, 0
        else:
            if map:
                for k, lines in map.items():
                    outfile = os.path.join(self.tmp_dir, k)
                    with open(outfile, 'a+') as f:
                        f.writelines(lines)

    @staticmethod
    def convert_prefix(uniprotkb_acc):
        '''
        group uniprotkb accession based on some head letters
        '''
        if uniprotkb_acc[0] == 'A':
            if uniprotkb_acc[1] == '0':
                if uniprotkb_acc[2] == 'A':
                    if uniprotkb_acc[3] == '0':
                        return 'A0'
                    elif uniprotkb_acc[3] == '1':
                        if uniprotkb_acc[4] in 'ABCDEFGHIJ':
                            return 'A1'
                        return 'A2'
                    elif uniprotkb_acc[3] == '2':
                        return 'A3'
                    elif uniprotkb_acc[3] == '3':
                        return 'A4'
                    elif uniprotkb_acc[3] == '4':
                        return 'A5'
                    elif uniprotkb_acc[3] == '5':
                        return 'A6'
                    elif uniprotkb_acc[3] == '6':
                        return 'A7'
                    elif uniprotkb_acc[3] == '7':
                        return 'A8'
                    elif uniprotkb_acc[3] == '8':
                        return 'A9'
                    return 'A9'
                return 'A9'
            return 'A9'
        elif uniprotkb_acc[0] in 'BCDEFGHIJK':
            return 'P1'
        return 'P2'

    def get_ncbi_acc(self, filename:str)->dict:
        '''
        value: NCBI_protein_accession, index: UniProtKB_protein_accession
        source file: *_gene_refseq_uniprotkb_collab.gz
        '''
        accessions = {}
        infile = os.path.join(self.tmp_dir, filename)
        if os.path.isfile(infile):
            df = pd.read_csv(infile, sep='\t', header=None, names=\
                ['NCBI_protein_accession', 'UniProtKB_protein_accession'])
            accessions = df.iloc[:,0].squeeze()
            accessions.index = df.iloc[:,1]
        return accessions


