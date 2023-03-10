#!/usr/bin/python3
"""
create map of references ~ <other annotation terms>
"""
import sys
from utils.commons import Commons
from parser.check import Check
from parser.map_gene import MapGene

class App(Commons):
    def __init__(self, project_name:str, ref_term:str):
        super(App, self).__init__()
        self.project_name = project_name
        self.ref_term = ref_term

    def process(self):
        if not Check().jtxt_build(self.project_name):
            print(f"error: No *.jtxt are detected. Please launch build.py firstly.")
            sys.exit(1)
        if self.ref_term not in ('GeneID', 'EnsemblID', 'TranscriptID'):
            print(f"error: reference term is wrong.")
            sys.exit(1)

        #do mapping
        # print(self.project_name, self.ref_term)
        c = MapGene(self.project_name)
        if self.ref_term == 'GeneID':
            c.map_entrez(['GeneID',])
        if self.ref_term == 'EnsemblID':
            c.map_entrez(["gene2ensembl", 'Ensembl_gene_identifier'])
        if self.ref_term == 'TranscriptID':
            c.map_entrez(['gene2refseq', "RNA_nucleotide_accession.version"])


if __name__ == '__main__':
    project_name, ref_term = sys.argv[1], sys.argv[2]
    App(project_name, ref_term).process()
    print('great!!!!')