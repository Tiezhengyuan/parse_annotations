"""
FTP of ExPASy: ftp.expasy.org
"""
import os
from connector.connect_ftp2 import ConnectFTP2
from utils.commons import Commons
from utils.dir import Dir

class ConnectExPASy(Commons):

    def __init__(self, endpoint:str=None):
        super(ConnectExPASy, self).__init__()
        self.endpoint = 'ftp.expasy.org' if endpoint is None else endpoint
        Dir(self.dir_expasy).init_dir()

    def download_swissprot_data(self):
        '''
        download data including gz files
        '''
        ConnectFTP2.download_files(
            ftp_endpoint = self.endpoint,
            ftp_path = '/databases/swiss-prot/release',
            pattern = '.dat.gz',
            local_path = self.dir_expasy
        )
