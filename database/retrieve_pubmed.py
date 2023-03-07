"""
PubMed: https://pubmed.ncbi.nlm.nih.gov/
"""
import os, sys
from bs4 import BeautifulSoup
from Bio import Entrez

from connector.http import HTTP
from utils.threading import Threading
from utils.dir import Dir
from database.ncbi_entrez import NCBIEntrez

class RetrievePubmed(NCBIEntrez):
    db = 'pubmed'

    def __init__(self, ref:dict=None):
        super(RetrievePubmed, self).__init__()
        self.endpoint = 'https://eutils.ncbi.nlm.nih.gov/entrez/'
        self.ref = ref if isinstance(ref, dict) else {}

    def get_ref(self):
        return self.ref

    def create_record(self, pmid:str):
        '''
        download article in PDF format
        pmid is parsing medline records
        '''
        self.get_outerlink('eutils/elink.fcgi/', pmid)
        self.get_pdf()
        return self.ref

    def get_outerlink(self, path:str, pmid:str):
        par = {
            'dbfrom': 'pubmed',
            'id': pmid,
            'cmd': 'prlinks',
        }
        text_data = HTTP(self.endpoint).retrieve_data(path, par)
        if text_data:
            try:
                soup = BeautifulSoup(text_data, 'html.parser')
                s1 = soup.idurlset.objurl
                outerlink = {
                    'pmid': soup.idurlset.id.get_text(),
                    'outer_url': s1.url.get_text() if hasattr(s1, 'url') else '',
                    'ref_category': s1.category.get_text() if hasattr(s1, 'category') else '',
                    'provider_abbr': s1.provider.nameabbr.get_text() if hasattr(s1, 'provider') else '',
                    'provider_id': s1.provider.id.get_text() if hasattr(s1, 'provider') else '',
                }
                self.ref.update(outerlink)
                return outerlink
            except Exception as e:
                # print('###TEXT:', text_data)
                # print('ERROR\tget_outerlink():', e)
                self.ref['retrieve_status'] = 'no linkout'
        return {}
    
    def get_pdf(self, outerlink:str=None):
        links = []
        outdir = os.path.join(self.dir_download, 'NCBI', 'pubmed', 'pdf')
        Dir(outdir).init_dir()
        try:
            outerlink = self.ref.get('outer_url') if outerlink is None else None
            text_data = HTTP(outerlink).retrieve_data()
            soup = BeautifulSoup(text_data, 'html.parser')
            for i in soup.find_all('meta',attrs={'name':'citation_pdf_url'}):
                # print(i['content'])
                file_name = os.path.basename(i['content'])
                local_file = os.path.join(outdir, f"{self.ref['pmid']}.pdf")
                if not os.path.isfile(local_file):
                    HTTP().download_pdf(i['content'], local_file)
                links.append({
                    'pdf_url': i['content'],
                    'local_path': local_file,
                })
            self.ref['pdf_links'] = links
        except Exception as e:
            print('ERROR\tget_pdf()):', e)
        return links

            
    def search_pubmed(self, term:str, **kwargs):
        '''
        retrieve 20 pmids per time
        '''
        idtype = kwargs['idtype'] if 'idtype' in kwargs else 'pmid'
        return self.search_entrez(
            db=self.db,
            term=term,
            idtype=idtype
        )
    
    def search_citations(self, pmid:str):
        '''
        search citations
        '''
        res= self.fetch_elink(
            dbfrom=self.db,
            db="pmc",
            link_name="pubmed_pmc_refs",
            id=pmid
        )[0]
        if res['ERROR'] == [] and len(res['LinkSetDb']) > 0:
            pmc_ids = [link["Id"] for link in res["LinkSetDb"][0]["Link"]]
            return pmc_ids
        return []
