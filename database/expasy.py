"""
ExPASy: https://www.expasy.org/
"""
import os
from typing import Iterable
from Bio.ExPASy import Enzyme

from utils.commons import Commons
from utils.file import File
from utils.utils import Utils
from utils.handle_json import HandleJson


class ExPASy(Commons):
    db = 'expasy'
    def __init__(self):
        super(ExPASy, self).__init__()
        self.dir_local = os.path.join(self.dir_download, self.db)
        self.cache_enzyme = os.path.join(self.dir_cache, f"{self.db}_enzyme.json")

    def parse_enzyme(self)->str:
        '''
        Process ~/expasy/enzyme/enzyme.dat
        Output: expasy_enzyme.json

        format of Enzyme.dat:
        ID  Identification                         (Begins each entry; 1 per entry)
        DE  Description (official name)            (>=1 per entry)
        AN  Alternate name(s)                      (>=0 per entry)
        CA  Catalytic activity                     (>=1 per entry)
        CC  Comments                               (>=0 per entry)
        PR  Cross-references to PROSITE            (>=0 per entry)
        DR  Cross-references to Swiss-Prot         (>=0 per entry)
        '''
        data = {}
        infile = os.path.join(self.dir_local, 'enzyme', 'enzyme.dat')
        with open(infile, 'r') as f:
            for record in Enzyme.parse(f):
                rec = dict(record)
                rec['EC'] = f"EC {rec['ID']}"
                rec['name'] = rec['DE'].replace('.', '')
                # self.print_dict(rec)
                data[rec['ID']] = rec
        # save data
        File(self.cache_enzyme).save_json(data)
        HandleJson(self.json_cache).update_json({
            __name__: { f"{self.db}_enzyme": self.cache_enzyme}
        })
        return self.cache_enzyme
    
    def gene_enzyme_annotation(self, ec:str)->dict:
        '''
        arg: ec is EC Number
        '''
        ec = ec.replace(' ', '').replace('EC', '')
        enzyme = HandleJson(self.cache_enzyme).read_json()
        for id, rec in enzyme:
            if id == ec:
                return rec
        return {}

    def search_enzymes(self, term:str, search_comments:bool=None)->Iterable:
        '''
        arg: term could be part of name
        '''
        if search_comments is None:
            search_comments = False
        enzyme = HandleJson(self.cache_enzyme).read_json()
        for _, rec in enzyme:
            if term in rec['DE'] or (search_comments == \
                    True and term in rec['CC']):
                yield rec

    def uniprotkb_to_ec(self)->dict:
        '''
        map UniProtKB ~ EC Number
        '''
        map = {}
        enzyme = HandleJson(self.cache_enzyme).read_json()
        for id, rec in enzyme:
            for refs in rec.get('DR', []):
                swissprot_id, _ = refs
                Utils.update_dict(map, swissprot_id, id)
        outfile = os.path.join(self.dir_cache, 'uniprotkb_to_ec.json')
        HandleJson(outfile).save_json(map)
        HandleJson(self.json_cache).update_json({
            'map': {'UniProtKB accession': {"EC number": outfile}}
        })
        return map
                        


