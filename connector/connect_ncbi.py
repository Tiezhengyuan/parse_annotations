"""
download data from NCIB FTP
"""
import os
from connector.connect_ftp2 import ConnectFTP2
from utils.commons import Commons
from utils.dir import Dir

class ConnectNCBI(Commons):
    def __init__(self, endpoint:str=None):
        super(ConnectNCBI, self).__init__()
        self.endpoint = 'ftp.ncbi.nlm.nih.gov' if endpoint is None else endpoint
        # inherit from Commons
        Dir(self.dir_ncbi).init_dir()
    
    def download_gene_data(self):
        '''
        download /gene/DATA. only gz files
        '''
        ConnectFTP2.download_files(
            ftp_endpoint = self.endpoint,
            ftp_path = 'gene/DATA',
            pattern = '.gz',
            local_path = self.dir_ncbi
        )


