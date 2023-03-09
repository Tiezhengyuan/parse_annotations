import os
import xml.dom.minidom
from dotenv import load_dotenv
load_dotenv()

class Commons:
    cascade_num = 2
    
    def __init__(self):
        # default directory
        self.dir_download = os.environ.get('DIR_DOWNLOAD', '')
        self.dir_cache = os.environ.get('DIR_CACHE', '')
        self.dir_map = os.path.join(self.dir_cache, 'map')

        # mdata data
        # format: {<class name>:{<method name>:<local path>}}
        self.json_cache = os.path.join(self.dir_cache, 'cache_local_path.json')
        self.json_download = os.path.join(self.dir_cache, 'download_local_path.json')

        # initialize local path of downloaded data
        self.dir_ncbi = os.path.join(self.dir_download, 'NCBI')
        self.dir_ncbi_gene = os.path.join(self.dir_ncbi, 'gene', 'DATA')
        self.dir_expasy = os.path.join(self.dir_download, 'ExPASy')
        self.dir_swissprot = os.path.join(self.dir_expasy, \
                        'databases', 'swiss-prot', 'release')
        self.uniprot_sprot_dat = os.path.join(self.dir_swissprot, \
                                            'uniprot_sprot.dat.gz')

    
    def print_xml(self, xml_str:str):
        temp = xml.dom.minidom.parseString(xml_str)
        new_xml = temp.toprettyxml()
        print(new_xml)
    
    def print_dict(self, indict):
        '''
        print dictionary to stdout for debugging
        '''
        n = 1
        for key in sorted(indict.keys()):
            print('{:5}: {:10}\t{}'.format(n, key, indict[key]))
            n += 1
