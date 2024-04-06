import json
import os

from oauth import OAuth
from schwab import Config

config = Config.create_from_env()
# to (re)start the oauth flow:
# 1. get code with client id, client secret and user's authorize
# 2. exchange the code with access token(30 minutes) and refresh token(7 days)
# 3. use the access token to call APIs
# 4. use the refresh token before expiration to get more access tokens.
oauth=OAuth(config.client_id, config.client_secret)
# oauth.get_code()
# tokens=oauth.get_token("C0.b2F1dGgyLmJkYy5zY2h3YWIuY29t.dWcpJtfd-Y4GTEQby6thHn2b32ih9kCM2aldthrshjw%40")
# print(json.dumps(tokens,indent=4,sort_keys=True))

token=oauth.refresh_token(config.refresh_token)
print(token['access_token'])
# print(json.dumps(token,indent=4,sort_keys=True))
