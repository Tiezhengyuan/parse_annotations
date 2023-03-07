#!/usr/bin/python3
"""
retrieve data according to terms specifiecd and organize them into data in jtxt format.
"""
import sys
from utils.commons import Commons
from database.process_gene import ProcessGene

class App(Commons):
    def __init__(self, project_name:str, field:str, term:str):
        super(App, self).__init__()
        self.project_name = project_name
        self.field = field
        self.term = term

    def process(self):
        # print(self.project_name, self.field, self.term)
        if self.field == 'taxonomy':
            ProcessGene(self.project_name).process_taxonomy_entrez(self.term)


if __name__ == '__main__':
    project_name, field, term  = sys.argv[1:4]
    App(project_name, field, term).process()
