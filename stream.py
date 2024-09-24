import asyncio
import json

import websockets

from schwab.account import Accounts
from schwab.oauth import OAuth
from schwab import Config
from schwab.stream import Stream


async def init(stream_info,token:str):
    async with websockets.connect(stream_info['streamerSocketUrl']) as websocket:
        stream = Stream(websocket, stream_info['schwabClientCustomerId'], stream_info['schwabClientCorrelId'])
        await stream.login(stream_info['schwabClientChannel'], stream_info['schwabClientFunctionId'], token)
        await stream.euqity_subscription(["QQQ","SPY","AAPL","MSFT","TSLA"])
        await stream.logout()
        return stream
if __name__ == '__main__':
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
    # token = "I0.b2F1dGgyLmNkYy5zY2h3YWIuY29t.SIR3RgzNFRx1-t5Ot2ZnESVJAbhJomSOGdOjQuqtHh4@"

    print(token)
    user_pref = Accounts.user_preferences(token)
    stream_info=user_pref['streamerInfo'][0]
    
    asyncio.run(init(stream_info,token))
    # Streams.stream