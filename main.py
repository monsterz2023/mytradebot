import json

from schwab.account import Accounts
from schwab.oauth import OAuth
from schwab import Config
from schwab.quote import Quotes

config = Config.create_from_env()
# to (re)start the oauth flow:
# 1. get code with client id, client secret and user's authorize
# 2. exchange the code with access token(30 minutes) and refresh token(7 days)
# 3. use the access token to call APIs
# 4. use the refresh token before expiration to get more access tokens.
oauth=OAuth(config.client_id, config.client_secret)
# step 1: get code
# oauth.get_code()

# step 2: get tokens after getting code from the redirect url in browser, the token is valid for 30 minutes, use refresh token to get more tokens
# tokens=oauth.get_token("C0.b2F1dGgyLmJkYy5zY2h3YWIuY29t.jBIRjBuG5TCHg7KIjF2-ySiVSf1OAUP_yy-g8BB45XU%40")
# print(json.dumps(tokens,indent=4,sort_keys=True))
# save the refresh token in system environment variable for later use, refresh token is valid for 7 days

# step 3: get token from refresh token
token=oauth.refresh_token(config.refresh_token)['access_token']

print(token)
accounts = Accounts.get_accounts(token)
for a in accounts:
    if a.account_number.endswith('549'):
        orders = a.open_orders(token)
        with open('stop_orders.csv', 'r') as f:
            lines = [l for l in f.readlines() if l.strip()]
            for line in lines:
                symbol, quantity, stop_price = line.strip().split(',')
                o = [o['orderId'] for o in orders if o['orderLegCollection'][0]['instrument']['symbol'] == symbol and o['orderLegCollection'][0]['instruction'] == 'SELL']
                if o:
                    print(f"Sell order(s) for {symbol} already exists, cancelling them")
                    [a.cancel_order(oid, token) for oid in o]
                a.sell_stop_loss_order(symbol, int(quantity), float(stop_price), token)
