'''
Map Entrez Gene 
'''
import os
import json
from utils.commons import Commons
from utils.file import File
from utils.dir import Dir
from utils.utils import Utils
from annotation.map import Map
from utils.handle_json import HandleJson
from utils.jtxt import Jtxt
from annotation.map_cache import MapCache

class MapGene(Map):

    def __init__(self):
        super(MapGene, self).__init__()

    def process_taxonomy_map(self, tax_id:str):
        # db = 'entrez'
        infile = f"{tax_id}_gene2accession.jtxt"
        self.get_map(infile, 'Symbol', lambda x: list(set(x)))
        self.get_map(infile, 'start_position_on_the_genomic_accession')

        infile = f"{tax_id}_gene_info.jtxt"
        self.get_map(infile, 'GeneID', 'chromosome')
        self.get_map(infile, 'GeneID', "Full_name_from_nomenclature_authority")
        self.get_map(infile, 'GeneID', "type_of_gene")
        self.get_map(infile, 'GeneID', "map_location")
        self.get_map(infile, 'GeneID', "Ensembl")
        self.get_map(infile, 'GeneID', "MIM")
        self.get_map(infile, 'GeneID', "HGNC")

        infile = f"{tax_id}_gene2refseq.jtxt"
        self.get_map(infile, 'GeneID', "protein_accession.version", lambda x: list(set(x)))

        infile = f"{tax_id}_gene2go.jtxt"
        self.get_map(infile, 'GeneID', "GO_ID", lambda x: list(set(x)))

        # within record
        infile = f"{tax_id}_gene2ensembl.jtxt"
        self.build_taxonomy_map(infile, "Ensembl_gene_identifier", "GeneID")
        self.build_taxonomy_map(infile, "Ensembl_protein_identifier", "GeneID")
        self.build_taxonomy_map(infile, "Ensembl_rna_identifier", "GeneID")

        #parse uniprotkb
        self.map_gene_to_uniprotkb(tax_id)


    def map_gene_to_uniprotkb(self, tax_id:str):
        '''
        source: cache\gene_refseq_uniprotkb_collab.jtxt
            NCBI_protein_accession ~ UniProtKB_protein_accession
        source: cache\<tax_id>\protein_accession.version_GeneID.json
            protein_accession.version ~ GeneID
        '''
        map = {}
        # protein accession ~ geneid
        proacc_geneid = MapCache(["taxonomy", tax_id, "protein_accession.version", "GeneID"]).get_map()
        # protein accession ~uniprotkb accession
        infile = os.path.join(self.dir_cache, 'gene_refseq_uniprotkb_collab.jtxt')
        handle = Jtxt(infile).read_jtxt()
        for pro_acc, uniprotkb_acc_list in handle:
            if pro_acc in proacc_geneid:
                for geneid in proacc_geneid[pro_acc]:
                    Utils.update_dict(map, geneid, uniprotkb_acc_list)
        # save map
        keys = ['GeneID', 'UniProtKB_protein_accession',]
        MapCache(keys).save_taxonomy_map(map, tax_id)




    

