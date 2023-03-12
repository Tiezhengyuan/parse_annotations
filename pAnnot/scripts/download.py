#!/usr/bin/python3
"""
Download source from NCBI and ExPASy
"""
from pAnnot.connector.connect_ncbi import ConnectNCBI
from pAnnot.connector.connect_expasy import ConnectExPASy
from pAnnot.utils.commons import Commons

class App(Commons):
    def __init__(self):
        super(App, self).__init__()
    
    def process(self):
        # download gene data from Entrez
        ConnectNCBI().download_gene_data()

        #download protein data from SwissProt
        ConnectExPASy().download_swissprot_data()
        


if __name__ == '__main__':
    App().process()
    print('Great! Download succeeded!!!')