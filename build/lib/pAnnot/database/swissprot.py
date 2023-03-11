"""
UniProt: https://www.uniprot.org/
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


class Swissprot(Commons):
    db = 'swiss-prot'

    def __init__(self)->None:
        super(Swissprot, self).__init__()

    def parse_protein(self)->Iterable:
        handle = File(self.uniprot_sprot_dat).readonly_handle()
        for record in SwissProt.parse(handle):
            rec = {
                'accessions': [{'UniProtKB_protein_accession':acc} \
                                for acc in record.accessions],
                'entry_name': record.entry_name,
                'data_class': record.data_class,
                'molecule_type': record.molecule_type,
                'sequence_length': int(record.sequence_length),
                'create': self.parse_date(record.created),
                'sequence_update': self.parse_date(record.sequence_update),
                'annotation_update': self.parse_date(record.annotation_update),
                'description': record.description,
                'gene_name': record.gene_name,
                'organism': record.organism,
                'organelle': record.organelle,
                'organism_classification': record.organism_classification,
                'tax_id': record.taxonomy_id,
                'host': self.parse_host(record),
                'comments': record.comments,
                'keywords': record.keywords,
                'features': self.parse_features(record.features),
                'protein_existence': record.protein_existence,
                'seqinfo': self.parse_seqinfo(record.seqinfo),
                'protein_sequence': record.sequence,
                'references': self.parse_references(record.references),
                'cross_references': self.parse_cross_references(record.cross_references),
            }
            # self.print_dict(rec)
            yield rec

    def parse_date(self, rec_date):
        return {k:v for k,v in zip(('date', 'release'), rec_date)}
    
    def parse_host(self, record):
        return [{'host_organism':a, 'host_taxonomy_id':b,} for a,b \
                in zip(record.host_organism, record.host_taxonomy_id)]

    def parse_seqinfo(self, seqinfo):
        keys = ['length', 'molecular_weight', 'CRC32_value']
        return {k:v for k,v in zip(keys, seqinfo)}
    
    def parse_features(self, features):
        fts = []
        if features:
            for feature in features:
                ft = {
                    'location': {
                        'start': str(feature.location.start),
                        'end': str(feature.location.end),
                        'strand': feature.location.strand,
                        'ref': feature.location.ref,
                        'ref_db': feature.location.ref_db,
                    },
                    'type': feature.type,
                    'id': feature.id,
                    'qualifiers': feature.qualifiers,
                }
                fts.append(ft)
        return fts

    def parse_references(self, references):
        refs = []
        if references:
            for reference in references:
                ref = {
                        'number': reference.number,
                        'positions': reference.positions,
                        'comments': reference.comments,
                        'authors': reference.authors,
                        'title': reference.title,
                        'location': reference.location,
                }
                for r in reference.references:
                    ref[r[0]] = r[1]
                refs.append(ref)
        return refs

    def parse_cross_references(self, cross_references):
        refs = {}
        if cross_references:
            for items in cross_references:
                Utils.init_dict(refs, [items[0],], [])
                id_name = 'id'
                if items[0] == 'EMBL':
                    id_name = 'embl_acc'
                elif items[0] == 'GO':
                    id_name = 'go'
                elif items[0] == 'RefSeq':
                    id_name = 'refseq_acc'
                elif items[0] == 'KEGG':
                    id_name = 'kegg_gene'
                refs[items[0]].append({
                    id_name: items[1],
                    'other': list(items[2:]),
                })
        return refs



