
import requests
import json
import os

class HTTP:
    def __init__(self, endpoint:str=None):
        self.endpoint = endpoint
    
    def retrieve_data(self, path=None, parameters=None):
        url = f"{self.endpoint}{path}" if path else self.endpoint
        if parameters:
            par = '&'.join([ f"{k}={v}" for k,v in parameters.items()])
            url += f"?{par}"
        # print(url)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        res = requests.get(url, headers=headers)
        # print(res)
        if res.status_code == 200:
            return res.text
        return None
    
    def retrieve_json(self, path=None, parameters=None):
        res = self.retrieve_data(path, parameters)
        try:
            return json.loads(res)
        except Exception as e:
            pass
        return {}
    
    def download_file(self, outdir, path=None):
        '''
        Download file from HTTP web 
        '''
        url = f"{self.endpoint}{path}" if path else self.endpoint
        outfile = os.path.join(outdir, os.path.basename(path))
        try:
            with open(outfile, 'wb') as f:
                res = requests.get(url)
                f.write(res.content)
            return outfile
        except Exception as e:
            print(e)
        return False

    def download_pdf(self, pdf_url, local_path, headers=None):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        res = requests.get(pdf_url, headers=headers, allow_redirects=True)
        try:
            with open(local_path, 'wb') as f:
                f.write(res.content)
        except Exception as e:
            print(e)
        return False


