import json
import websockets
import asyncio


class Stream:
    def __init__(self, websocket, customer_id: str, correl_id: str) -> None:
        self.websocket = websocket
        self.customer_id = customer_id
        self.correl_id = correl_id
        self.__request_id = 0

    def request_id(self):
        self.__request_id += 1
        return self.__request_id

    def _resp_handler(self, response):
        print(response)
        return json.loads(response)

    async def euqity_subscription(self,keys=list[str]):
        data = {
            "requestid": self.request_id(),
            "service": "LEVELONE_EQUITIES",
            "command": "SUBS",
            "SchwabClientCustomerId": self.customer_id,
            "SchwabClientCorrelId": self.correl_id,
            "parameters": {
                "keys": ','.join(keys),
                "fields": "0,3,10,11,12,13,17"
            }
        }
        await self.websocket.send(json.dumps(data))
        while True:
            response = await self.websocket.recv()
            print(response)

    async def login(self, channel: str, func_id: str, token: str):
        data = {
            "requestid": self.request_id(),
            "service": "ADMIN",
            "command": "LOGIN",
            "SchwabClientCustomerId": self.customer_id,
            "SchwabClientCorrelId": self.correl_id,
            "parameters": {
                "Authorization": token,
                "SchwabClientChannel": channel,
                "SchwabClientFunctionId": func_id
            }
        }

        await self.websocket.send(json.dumps(data))
        response = await self.websocket.recv()
        return self._resp_handler(response)

    async def logout(self):
        data = {
            "requestid": self.request_id(),
            "service": "ADMIN",
            "command": "LOGOUT",
            "SchwabClientCustomerId": self.customer_id,
            "SchwabClientCorrelId": self.correl_id,
            "parameters": {}
        }
        await self.websocket.send(json.dumps(data))
        response = await self.websocket.recv()
        return self._resp_handler(response)
