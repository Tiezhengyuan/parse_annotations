"""
PubMed
"""
import os, sys
from bs4 import BeautifulSoup
from Bio import Entrez

from utils.commons import Commons
from utils.file import File
from utils.dir import Dir
from utils.utils import Utils
from utils.handle_json import HandleJson

from database.retrieve_pubmed import RetrievePubMed

class ProcessPubMed(Commons):
    db = 'pubmed'

    def __init__(self):
        super(ProcessPubMed, self).__init__()
        self.outdir = os.path.join(self.dir_cache, 'pubmed')
        Dir(self.outdir).init_dir()
        
    def process(self):
        self.prepare_pmid()

    def retrieve_pubmed(self):
        files = Dir(self.outdir).recrusive_files()
        for file in files:
            data = {}
            for pmid, rec in HandleJson(file).read_json():
                print('###:', pmid)
                data[pmid] = rec
                res = RetrievePubMed().create_record(pmid)
                data[pmid].update(res)
                print(res)
            break

    def prepare_pmid(self):
        """
        group pmid in id_list.txt
        """
        Dir(self.outdir).clear_dir()
        map, n = {}, 0
        infile = os.path.join(self.dir_download, 'NCBI', 'pubmed', 'id_list.txt.gz')
        for line in File(infile).readonly_handle():
            n += 1
            pmid = line.strip()
            group = self.group_pmid(pmid)
            Utils.init_dict(map, [group, pmid], {'PMID': pmid})
            if n >= 1e9:
                self.save_map(map)
                map, n = {}, 0
        else:
            self.save_map(map)


    def group_pmid(self, pmid:str):
        name = str(pmid)
        if name.endswith('A'):
            return 'A'
        elif name.endswith('R'):
            if int(name[:-1]) < 1e7:
                return 'R0'
            elif int(name[:-1]) < 4.5e7:
                return 'R1'
            return 'R'
        else:
            levels = [.4, 8.2, 9, 9.5, 10.1, 101, 101.1, 101.2, \
                101.31, 101.48, 101.59, 101.7]
            levels = [i*1000000 for i in levels]
            for a,b in enumerate(levels):
                if int(name) < b:
                    return str(a+1)
        return '0'


    def save_map(self, map:dict):
        for group, data in map.items():
            outfile = os.path.join(self.outdir, f"{group}.json")
            HandleJson(outfile).update_json(data)