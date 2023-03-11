'''
Map Entrez Gene 
'''
import os
import json
from utils.commons import Commons
from utils.file import File
from utils.dir import Dir
from utils.utils import Utils
from parser.detect_map import Map
from utils.handle_json import HandleJson
from utils.jtxt import Jtxt
from parser.map_cache import MapCache

class MapAnnot:

    def __init__(self, project_name:str):
        self.dir_project = os.path.join(self.dir_cache, project_name)

    def map_entrez(self, key1:list):
        '''
        example: key1 = ['GeneID',]
        '''
        file_entrez = os.path.join(self.dir_project, 'entrez.jtxt')
        keys2 = [
            (['GeneID',], None),
            (["gene2accession", "Symbol"], None),
            (["gene2accession", "start_position_on_the_genomic_accession"], None),
            (["gene2accession", "UniProtKB_protein_accession"], None),
            (["gene_info", "dbXrefs"], None),
            (["gene_info", "chromosome"], None),
            (["gene_info", "map_location"], None),
            (["gene_info", "assembly"], None),
            (["gene_info", "Full_name_from_nomenclature_authority"], None),
            (["gene_info", "MIM"], None),
            (["gene_info", "HGNC"], None),
            (["gene2ensembl", 'Ensembl_gene_identifier'], None),
            (["gene2ensembl", 'Ensembl_rna_identifier'], None),
            (["gene2ensembl", 'Ensembl_protein_identifier'], None),
            (['gene2refseq', "genomic_nucleotide_accession.version"], None),
            (['gene2refseq', "protein_accession.version"], 'refseq_protein_id'),
            (['gene2refseq', "RNA_nucleotide_accession.version"], 'refseq_transcript_id'),
            (['gene2pubmed', 'PubMed_ID'], None),
            (['gene2go', 'GO_ID'], None),
        ]
        keys2 = [i for i in keys2 if i[0] != key1]
        for key2, key_name in keys2:
            map = {}
            handle = Jtxt(file_entrez).read_jtxt()
            for rec in handle:
                val1 = Utils.get_deep_value(rec, key1)
                val2 = Utils.get_deep_value(rec, key2)
                # print(val1, val2)
                if val1 and val2:
                    for k in val1:
                        Utils.update_dict(map, k, val2)
            if key_name is None: key_name = key2[-1]
            MapCache(key1[-1], key_name).save_map(map, self.dir_project)


    def map_expasy(self, key1:list):
        '''
        example: key1 = ['accessions','UniProtKB_protein_accession']
        '''
        file_expasy = os.path.join(self.dir_project, 'expasy.jtxt')
        keys2 = [
            (['accessions','UniProtKB_protein_accession'], None),
            (['accessions','protein_accession.version'], None),
            (['gene_name','Name'], 'gene_name'),
            (['protein_sequence',], None),
            (['seqinfo','length'], 'amino_acid_length'),
            (['seqinfo', 'molecular_weight'], None),
            (['seqinfo', 'CRC32_value'], None),
            (['cross_references','EMBL', 'embl_acc'], 'EMBL_accession'),
            (['cross_references','CCDS', 'id'], 'CCCDS'),
            (['cross_references','PIR', 'id'], 'PIR'),
            (['cross_references',"RefSeq","refseq_acc"], 'RefSeq_protein_accession'),
            (['cross_references','PDB', 'id'], 'PDB'),
            (['cross_references','PDBsum', 'id'], 'PDBsum'),
            (['cross_references',"DrugBank",'id'], "DrugBank"),
            (['cross_references',"Ensembl", 'id'], "Ensembl_protein_accession"),
            (['cross_references',"GeneID", 'id'], "GeneID"),
            (['cross_references',"KEGG", 'kegg_gene'], None),
            (['cross_references',"HGNC", 'id'], "HGNC"),
            (['cross_references',"MIM", 'id'], "MIM"),
            (['cross_references',"Proteomes",'id'], "Proteomes"),
            (['cross_references',"GO", 'go'], 'GO_ID'),
            (['cross_references',"InterPro", 'go'], "InterPro"),
            (['cross_references',"PROSITE",'id'], "PROSITE"),
            (['cross_references',"PIRSF",'id'], "PIRSF"),
            (['cross_references',"Pfam",'id'], "Pfam"),
            (['cross_references',"ExpressionAtlas",'id'], "ExpressionAtlas"),
        ]
        keys2 = [i for i in keys2 if i[0] != key1]
        for key2, key_name in keys2:
            map = {}
            handle = Jtxt(file_expasy).read_jtxt()
            for rec in handle:
                val1 = Utils.get_deep_value(rec, key1)
                val2 = Utils.get_deep_value(rec, key2)
                # print(val1, val2)
                if val1 and val2:
                    for k in val1:
                        Utils.update_dict(map, k, val2)
            if key_name is None: key_name = key2[-1]
            MapCache(key1[-1], key_name).save_map(map, self.dir_project)

    

