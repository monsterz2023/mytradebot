
import requests
from urllib.parse import quote

from schwab import API_HOST

class Quotes:
    @classmethod
    def quote(cls, symbols:str,  token,  fields="quote,reference",):
        
        headers = {"Authorization":f"Bearer {token}"}
        resp=requests.get(f"{API_HOST}/marketdata/v1/quotes?symbols={symbols}&fields={fields}&indicative=false",headers=headers)
        return resp.json()