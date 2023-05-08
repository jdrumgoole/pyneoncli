import requests


class Requester:

    def __init__(self, base_url:str, key=None):
        self._key = key
        self._base_url = base_url
        self._headers = {}
        self._headers['Authorization'] = f"Bearer {self._key}"
        self._headers['Content-Type'] = "application/json"

    def request(self, method:str,  operation:str,  **kwargs):

        return requests.request(method, f"{self._base_url}{operation}", headers=self._headers, **kwargs)

    def GET(self, operation:str, **kwargs):
        return self.request("GET", operation, **kwargs)

    def POST(self, operation:str, **kwargs):
        return self.request("POST", operation, **kwargs)

    def PUT(self, operation:str, **kwargs):
        return self.request("PUT", operation, **kwargs)

    def PATCH(self, operation:str, **kwargs):
        return self.request("PATCH", operation, **kwargs)
class NeonAPI:

    BASE_URL_V2="https://console.neon.tech/api/v2/" 

    def __init__(self, base_url:str= BASE_URL_V2, key=None):
        self.key = key
        self.base_url = base_url
        self._requester = Requester(self.base_url, self.key)
    
    def validate_key(self):
        if not self.key:
            return False    
        else:
            for i in self._requester.GET("projects"):
                return True
        
    def get_projects(self):
        projects = self._requester.GET("projects")["projects"]
        for project in projects:
            yield project
    
