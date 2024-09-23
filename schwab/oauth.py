import base64
import webbrowser
import requests
from urllib.parse import unquote

class OAuth:
    def __init__(self,cli_id:str, cli_sec:str, redirect_uri="https://127.0.0.1/mytradebot") -> None:
        self.cli_id=cli_id
        self.cli_sec=cli_sec
        self.redirect_uri=redirect_uri

    def get_code(self):
        '''
        open browser to get auth code
        '''
        url=f"https://api.schwabapi.com/v1/oauth/authorize?client_id={self.cli_id}&redirect_uri={self.redirect_uri}"
        webbrowser.open(url)

    def get_token(self, code):
        '''
        once code is copied from the redirect url as query parameter `code`, use it here to exchange for tokens
        '''
        url = "https://api.schwabapi.com/v1/oauth/token"
        headers = {
            "Authorization": f"Basic {self.__auth_header()}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "authorization_code",
            "code": unquote(code),
            "redirect_uri": "https://127.0.0.1/mytradebot",
        }
        response = requests.post(url, headers=headers, data=data)
        data = response.json()
        return data
    
    def refresh_token(self, refresh_token):
        '''
        refresh token with existing refresh token
        '''
        url = "https://api.schwabapi.com/v1/oauth/token"
        headers = {
            "Authorization": f"Basic {self.__auth_header()}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        response = requests.post(url, headers=headers, data=data)
        data = response.json()
        return data
    
    def __auth_header(self):
        return base64.b64encode(f"{self.cli_id}:{self.cli_sec}".encode()).decode()
