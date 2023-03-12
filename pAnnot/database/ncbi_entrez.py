"""
Entrez: https://eutils.ncbi.nlm.nih.gov
"""
from datetime import datetime
import os, sys, time
from bs4 import BeautifulSoup
import wget
from Bio import Entrez
# Entrez.api_key = "MyAPIkey"
Entrez.email = "tiezhengyuan@hotmail.com"

from pAnnot.utils.commons import Commons


class NCBIEntrez(Commons):
    def __init__(self):
        super(NCBIEntrez, self).__init__()
        # self.endpoint = 'https://eutils.ncbi.nlm.nih.gov/entrez/'

    
    def get_db_infos(self):
        db_infos = {}
        handle = Entrez.einfo()
        record = Entrez.read(handle)
        for db in record["DbList"]:
            db_handle = Entrez.einfo(db=db)
            db_info = Entrez.read(db_handle)['DbInfo']
            # print(db_info)
            db_infos[db] = db_info
        return db_infos

    def search_entrez(self, db:str, term:str, idtype:str=None):
        '''
        retrieve 20 ids per time
        example: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=asthma
        '''
        ret_start = 0
        try_times = 1
        while ret_start is not None:
            if try_times == 3:
                print("Error: HTTP connection failed. Trying 3 times")
                break
            try:
                handle = Entrez.esearch(
                    db=db,
                    term = term,
                    RetStart=ret_start,
                    idtype=idtype
                )
                record = Entrez.read(handle)
                ret_start += 20
                if int(record['Count']) < ret_start:
                    ret_start = None
                print(record['IdList'])
                try_times = 1
                yield record['IdList']
            except Exception as e:
                print(e)
                try_times +=1
                time.sleep(5)


    def efetch(self, db:str, id:str, rettype:str=None,\
            retmode:str=None):
        try:
            handle = Entrez.efetch(
                db=db,
                id=id,
                rettype=rettype,
                retmode=retmode
            )
            # return instance of Record class
            return handle.read()
        except Exception as e:
            print('failed retrieve record from Entrez', e)

    def fetch_elink(self, dbfrom:str, db:str, link_name:str, id:str):
        handle = Entrez.elink(
            dbfrom=dbfrom,
            db=db,
            LinkName=link_name,
            id=id
        )
        return Entrez.read(handle)
    
