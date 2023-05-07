import requests

class NeonAPI:

    BASE_URL_V2="https://console.neon.tech/api/v2/" 

    def __init__(self, base_url:str= BASE_URL_V2, key=None):
        self.key = key
        self.base_url = base_url


    def _request(self, method:str, url:str, func:str,  **kwargs):
        headers = kwargs.pop('headers', {})
        headers['Authorization'] = f"Bearer {self.key}"
        headers['Content-Type'] = "application/json"
        return requests.request(method, f"{url}{func}", headers=headers, **kwargs)
    
    def validate_key(self):
        if not self.key:
            return False    
        else:
            return self._request("GET", self.base_url, "projects")
