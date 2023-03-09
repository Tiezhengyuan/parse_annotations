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
    
    def __init__(self, project_name:str=None):
        super(ProcessGene, self).__init__()
        self.project_name = project_name if project_name else 'project'
        # store local file is downloaded from NCBI FTP
        self.dir_source = os.path.join(self.dir_download, 'NCBI', 'gene', 'DATA')
        self.tmp_dir = os.path.join(self.dir_source, "tmp_gene_refseq_uniprotkb_collab")
        Dir(self.tmp_dir).init_dir()

    def process_taxonomy_entrez(self, tax_id:str):
        '''
        process *.gz and store map in cache
        '''
        outdir = os.path.join(self.dir_cache, self.project_name)
        Dir(outdir).init_dir()
        outfile = os.path.join(outdir, f"{self.db}.jtxt")
        
        #parse and integrate gene data
        counter = iter(range(1, 500))
        tmp_infile = outfile + f".{next(counter)}"
        file_names = ['gene2accession', 'gene2refseq', 'gene2pubmed', \
            'gene2go', 'gene2ensembl', 'gene_info', 'gene_group', \
            'gene_history', 'gene_neighbors', 'gene_orthologs', ]
        for file_name in file_names:
            # print(file_name)
            map_iter = self.parse_taxonomy_gene2(file_name, tax_id)
            # save map to cache
            for map in map_iter:
                if not os.path.isfile(tmp_infile):
                    Jtxt(tmp_infile).save_jtxt(map, False)
                else:
                    tmp_outfile = outfile + f".{next(counter)}"
                    Jtxt(tmp_infile).merge_jtxt('GeneID', map, tmp_outfile)
                    tmp_infile = tmp_outfile

        # decorate some data format
        tmp_outfile = outfile + f".{next(counter)}"
        print(tmp_infile, tmp_outfile)
        self.format_gene(tmp_infile, tmp_outfile)
        tmp_infile = tmp_outfile
        # parse uniprotkb
        tmp_outfile = outfile + f".{next(counter)}"
        print(tmp_infile, tmp_outfile)
        tmp_outfile = self.parse_uniprotkb(tmp_infile, tmp_outfile)
        os.rename(tmp_outfile, outfile)
        del counter

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
        print(f"parse {mapfile}")
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
                if len(map) >= 1e5:
                    output = deepcopy(map)
                    map = {}
                    yield output
            else:
                if map:
                    yield map

    def format_gene(self, infile:str, outfile:str):
        with open(outfile, 'wt') as f:
            handle = Jtxt(infile).read_jtxt()
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
        try:
            os.remove(infile)
        except Exception as e:
            print(e)
        return outfile

    @staticmethod
    def format_dbxrefs(rec:dict):
        if rec.get("dbXrefs") not in (None, '-'):
            if isinstance(rec["dbXrefs"], str):
                rec["dbXrefs"] = [rec["dbXrefs"],]
            for item in rec["dbXrefs"]:
                name, id = item.split(':', 1)
                Utils.update_dict(rec, name, id)


    def parse_uniprotkb(self, infile:str, outfile:str):
        #initialize acc_pair
        acc_pair = {}
        handle = Jtxt(infile).read_jtxt()
        for rec in handle:
            for key1 in ("gene2accession", "gene2refseq", "gene2ensembl"):
                for item in rec.get(key1, []):
                    pro_acc = item.get("protein_accession.version", '-')
                    if pro_acc != '-':
                        acc_pair[pro_acc] = []

        # parse acc_pair
        self.parse_ncbi_acc_pair(acc_pair)
        
        #update outfile
        with open(outfile, 'wt') as f:
            handle = Jtxt(infile).read_jtxt()
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
        try:
            os.remove(infile)
        except Exception as e:
            print(e)
        return outfile

    def parse_ncbi_acc_pair(self, acc_pair:dict):
        parse_infile = os.path.join(self.dir_source, "gene_refseq_uniprotkb_collab.gz")
        with File(parse_infile).readonly_handle() as f:
            # skip the first line
            _ = next(f)
            for line in f:
                val1, val2 = line.rstrip().split('\t')
                if val1 in acc_pair and val2 not in acc_pair[val1]:
                    acc_pair[val1].append(val2)

    def parse_uniprot_acc_pair(self, acc_pair:dict):
        parse_infile = os.path.join(self.dir_source, "gene_refseq_uniprotkb_collab.gz")
        with File(parse_infile).readonly_handle() as f:
            # skip the first line
            _ = next(f)
            for line in f:
                val1, val2 = line.rstrip().split('\t')
                if val2 in acc_pair and val1 not in acc_pair[val2]:
                    acc_pair[val2].append(val1)

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
                    if uniprotkb_acc[3] == '1':
                        return 'A0'
                    elif uniprotkb_acc[3] in '02':
                        return 'A1'
                    elif uniprotkb_acc[3] in '345':
                        return 'A2'
                    return 'A3'
                return 'A4'
            return 'A4'
        return 'A4'

    @staticmethod
    def get_split_names():
        '''
        determined by convert_prefix()
        '''
        return ['A0', 'A1', 'A2', 'A3', 'A4']

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


