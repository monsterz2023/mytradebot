from datetime import datetime, timedelta
import requests
import json

host = "https://api.schwabapi.com"


class Position:
    def __init__(self, symbol: str, quantity: int, average_price: float) -> None:
        self.symbol = symbol
        self.quantity = quantity
        self.average_price = average_price

    def __repr__(self) -> str:
        return f"Position: symbol({self.symbol}) quantity({self.quantity}) average_price({self.average_price})"


class Account:
    def __init__(self, account_number: str, hash_value: str, positions: list[Position]) -> None:
        self.account_number = account_number
        self.hash_value = hash_value
        self.positions = positions

    def _market_order(self, symbol, quantity, instruction, token):
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "orderType": "MARKET",
            "session": "NORMAL",
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": instruction,
                    "quantity": quantity,
                    "instrument": {
                        "symbol": symbol,
                        "assetType": "EQUITY"
                    }
                }
            ]
        }
        url = f"{host}/trader/v1/accounts/{self.hash_value}/orders"
        resp = requests.post(url, headers=headers, json=data)
        return resp

    def sell_market_order(self, symbol, quantity, token):
        return self._market_order(symbol, quantity, "SELL", token)

    def buy_market_order(self, symbol, quantity, token):
        return self._market_order(symbol, quantity, "BUY", token)

    def sell_stop_loss_order(self, symbol, quantity, stop_price,  token, stop_price_offset_percent=0.4):
        headers = {"Authorization": f"Bearer {token}"}
        stop_price = round(stop_price*(1-stop_price_offset_percent/100), 2)
        data = {
            "orderType": "STOP",
            "session": "NORMAL",
            "duration": "GOOD_TILL_CANCEL",
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": "SELL",
                    "quantity": quantity,
                    "instrument": {
                        "symbol": symbol,
                        "assetType": "EQUITY"
                    }
                }
            ],
            "stopPrice": stop_price
        }
        
        print(f"Creating stop loss order for {symbol} with quantity {quantity} and stop price {stop_price}")
        url = f"{host}/trader/v1/accounts/{self.hash_value}/orders"
        resp = requests.post(url, headers=headers, json=data)
        return resp

    def open_orders(self, token):
        # from entered time is 3 months ago
        now = datetime.today()
        from_entered_date = now - timedelta(days=90)
        end_entered_date = now
        # ISO-8601 format for dates yyyy-MM-dd'T'HH:mm:ss.SSSZ
        from_entered_date = from_entered_date.isoformat(
            timespec='seconds')+'.000Z'
        end_entered_date = end_entered_date.isoformat(
            timespec='seconds')+'.000Z'
        url = f"{host}/trader/v1/accounts/{self.hash_value}/orders?fromEnteredTime={
            from_entered_date}&toEnteredTime={end_entered_date}&status=PENDING_ACTIVATION"
        resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        return resp.json()

    def cancel_order(self, order_id, token):
        headers = {"Authorization": f"Bearer {token}"}
        url = f"{host}/trader/v1/accounts/{self.hash_value}/orders/{order_id}"
        resp = requests.delete(url, headers=headers)
        return resp
    def __repr__(self) -> str:
        return f"Schwab account: account_number({self.account_number}) hash_value({self.hash_value}) positions({self.positions})"


class Accounts:
    @classmethod
    def user_preferences(cls, token):
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(
            f"{host}/trader/v1/userPreference", headers=headers)
        return resp.json()
    @classmethod
    def get_accounts(cls, token):
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(
            f"{host}/trader/v1/accounts?fields=positions", headers=headers)
        hash_resp = requests.get(
            f"{host}/trader/v1/accounts/accountNumbers", headers=headers)
        accounts = []
        for a in resp.json():
            for h in hash_resp.json():
                if a['securitiesAccount']['accountNumber'] == h['accountNumber']:
                    positions = [Position(p['instrument']['symbol'], p['longQuantity'],
                                          p['averageLongPrice']) for p in a['securitiesAccount']['positions']]
                    accounts.append(
                        Account(a['securitiesAccount']['accountNumber'], h['hashValue'], positions))
                    break
        return accounts
