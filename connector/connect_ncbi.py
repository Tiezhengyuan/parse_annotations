"""
download data from NCIB FTP
"""
import os
from connector.connect_ftp import ConnectFTP
from connector.connect_ftp2 import ConnectFTP2

class ConnectNCBI(ConnectFTP):
    def __init__(self, endpoint:str=None):
        self.endpoint = 'ftp.ncbi.nlm.nih.gov' if endpoint is None else endpoint
        super(ConnectNCBI, self).__init__(endpoint)
        self.dir_local_ncbi = os.path.join(self.dir_download, "NCBI")
    
    def process(self):
        self.download_gene_data()
        self.download_pubmed()

    def download_gene_data(self):
        '''
        download /gene/DATA including subdirectories and files
        '''
        local_files = self.download_tree(
            local_name = os.path.join('NCBI', 'gene', 'DATA'),
            ftp_path = 'gene/DATA',
            file_pattern = '.gz'
        )
        return local_files

    def download_pubmed(self):
        '''
        download /PubMed including subdirectories and files
        '''
        ConnectFTP2.download_tree(
            ftp_endpoint = self.endpoint,
            ftp_path = '/pubmed',
            pattern = '.gz',
            local_path = self.dir_local_ncbi
        )
