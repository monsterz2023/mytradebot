import requests
import json

host="https://api.schwabapi.com"

class Account:
    def __init__(self,account_number:str) -> None:
        self.account_number=account_number

class Accounts:
    @classmethod
    def get_accounts(cls,token):
        headers = {"Authorization":f"Bearer {token}"}
        resp=requests.get(f"{host}/trader/v1/accounts", headers=headers)
        print(json.dumps(resp.json(), indent=4, sort_keys=True))


if __name__ == '__main__':
    Accounts.get_accounts("I0.b2F1dGgyLmJkYy5zY2h3YWIuY29t.n0BtCpYaY50QRNHJI8UdFchUg5gTi-BtkHJlaYbWbXA@")