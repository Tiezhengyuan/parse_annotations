"""

"""
from copy import deepcopy
import json
import os
from typing import Iterable
from Bio import SwissProt

from utils.commons import Commons
from utils.file import File
from utils.dir import Dir
from utils.utils import Utils
from utils.handle_json import HandleJson
from annotation.map import Map
from annotation.map_cache import MapCache
from database.swissprot import Swissprot

class MapProtein(Map):
    def __init__(self)->None:
        super(MapProtein, self).__init__()

    def process(self):
        # map swissprot accession number to
        db = 'swissprot'
        metadata=(
            (['accessions','uniprotkb_acc',], ['taxonomy_id',]),
            (['accessions','uniprotkb_acc',], ['protein_sequence',]),
            (['accessions','uniprotkb_acc'], ['cross_reference','EMBL', 'embl_acc']),
            (['accessions','uniprotkb_acc'], ['cross_reference','GO', 'go']),
        )
        for keys1, keys2 in metadata:
            key1, key2 = keys1[-1], keys2[-1]
            handle = Swissprot().parse_protein()
            map = self.map_term(handle, keys1, keys2)
            outdir = os.path.join(self.dir_cache, db)
            MapCache([db, key1, key2]).save_map_cache(map, outdir)
    

