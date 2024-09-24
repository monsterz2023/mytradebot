import requests

from schwab import API_HOST

class PriceHistory:
    @classmethod
    def price_history(cls, symbol: str, period_type: str, token):
        headers = {"Authorization": f"Bearer {token}"}
        url=f"{API_HOST}/marketdata/v1/pricehistory?symbol={symbol}&periodType={period_type}"
        print(url)
        resp = requests.get(url, headers=headers)
        return resp.json()
        
