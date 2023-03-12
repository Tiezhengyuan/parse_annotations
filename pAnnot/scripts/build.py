#!/usr/bin/python3
"""
retrieve data according to terms specifiecd and organize them into data in jtxt format.
"""
import os
import sys
from pAnnot.utils.dir import Dir
from pAnnot.utils.commons import Commons
from pAnnot.database.process_gene import ProcessGene
from pAnnot.database.process_protein import ProcessProtein
from pAnnot.parser.check import Check

class App(Commons):
    def __init__(self, project_name:str, field:str, term:str):
        super(App, self).__init__()
        self.project_name = project_name
        self.field = field
        self.term = term

    def process(self):
        # check download
        c = Check()
        is_ncbi = c.entrez_gene_download()
        is_expasy = c.swissprot_download()
        if is_expasy is False or is_ncbi is False:
            sys.exit(1)

        # print(self.project_name, self.field, self.term)
        if not self.project_name:
            self.project_name = 'project'
        dir_db = os.path.join(self.dir_cache, self.project_name)
        Dir(dir_db).init_dir()

        if self.field == 'taxonomy':
            # entrez gene
            ProcessGene(dir_db).process_taxonomy_entrez(self.term)
            # swissprot protein
            # ProcessProtein(dir_db).process_taxonomy_protein(self.term)


if __name__ == '__main__':
    project_name, field, term  = sys.argv[1:4]
    App(project_name, field, term).process()
