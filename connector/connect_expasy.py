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
        self.dir_local = os.path.join(self.dir_download, "ExPASy")
        Dir(self.dir_local).init_dir()

    def download_swissprot_data(self):
        '''
        download data including gz files
        '''
        ConnectFTP2.download_files(
            ftp_endpoint = self.endpoint,
            ftp_path = '/databases/swiss-prot/release',
            pattern = '.dat.gz',
            local_path = self.dir_local
        )
