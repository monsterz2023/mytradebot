import os

class Config:
    def __init__(self, client_id, client_secret, refresh_token) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token

    @classmethod
    def create_from_env(cls):
        client_id=os.environ.get("SCHWAB_CLIENT_ID")
        client_secret=os.environ.get("SCHWAB_CLIENT_SECRET")
        refresh_token=os.environ.get("SCHWAB_REFRESH_TOKEN")
        return cls(client_id,client_secret,refresh_token)