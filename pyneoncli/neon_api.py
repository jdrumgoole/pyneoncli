import json
import sys
import requests

BASE_URL_V2="https://console.neon.tech/api/v2/"
class Requester:

    def __init__(self, base_url:str=BASE_URL_V2, key=None):
        self._key = key
        self._base_url = base_url
        self._headers = {}
        self._headers['Authorization'] = f"Bearer {self._key}"
        self._headers['Content-Type'] = "application/json"

    def request(self, method:str,  operation:str,  **kwargs):

        try:
            # print(self._headers)
            # print(kwargs)
            path = f"{self._base_url}{operation}"
            print(path)
            r = requests.request(method, path, headers=self._headers, **kwargs)
            r.raise_for_status()
            return r.json()
        
        except requests.exceptions.HTTPError as err:
            print("HTTP Error")
            print(r.url)
            print(r.status_code)
            print(r.headers)
            print(err)
            sys.exit(1)

        return r.json()

    def GET(self, operation:str, **kwargs):
        return self.request("GET", operation)

    def POST(self, operation:str, data:dict={}):
        self._headers["Accept"] = "application/json"
        return self.request("POST", operation, data=json.dumps(data))

    def PUT(self, operation:str, **kwargs):
        return self.request("PUT", operation, **kwargs)

    def DELETE(self, operation:str, **kwargs):
        return self.request("DELETE", operation, **kwargs)
    
    def PATCH(self, operation:str, **kwargs):
        return self.request("PATCH", operation, **kwargs)

# class NeonAPI:

#     BASE_URL_V2="https://console.neon.tech/api/v2/" 

#     def __init__(self, base_url:str= BASE_URL_V2, key=None):
#         self._key = key
#         self._base_url = base_url
#         self._requester = Requester(self.base_url, self._key)
    
#     @property
#     def base_url(self):
#         return self._base_url
    
#     @base_url.setter
#     def base_url(self, value):
#         self._base_url = value
    
#     def validate_key(self):
#         if not self._key:
#             return False    
#         else:
#             for i in self._requester.GET("projects"):
#                 return True
        
#     # Projects

#     def get_projects(self):
#         projects = self._requester.GET("projects")["projects"]
#         for project in projects:
#             yield project

#     def create_project(self, name:str):
#         payload = {"project": {"name": name}}
#         self._requester.POST(f"projects", data=payload)



#     # Branches
#     def get_branches(self, branch_id:str):
#         b = self._requester.GET(f"projects/{branch_id}/branches")
        return b
    
# red-sea-544606

def dict_filter(d:dict, keys:list[str]):
    retValue = {}
    if keys is None or len(keys) == 0:
        return d
    for k,v in flatten(d):
        if k in keys:
            retValue[k] = v
    return retValue


def flatten(d:dict, root:str=None):
    for k, v in d.items():
        if type(v) == dict:
            yield from flatten(v, k)
        else:
            yield f"{root}.{k}", v

def dict_filter_key(d:dict, key:str):

    if key is None or len(key) == 0:
        return d
    if type(d) != dict:
        raise TypeError("d must be a dict")
    key_path = key.split(".")
    for k in d.keys():
        if k == key_path[0]:
            if len(key_path) > 1:
                return dict_filter(d[k], ".".join(key_path[1:]))
            else:
                return k, d[k]

class NeonObject:
    
        def __init__(self, api_key:str, operation=None) -> None:
            self._api_key = api_key
            self._operation = operation
            self._requester = Requester(key=self._api_key)
            self._obj = {}

        @property
        def operation(self):
            return self._operation
    
        def __str__(self) -> str:
            return f"api_key={self._api_key}\noperation={self._operation}"
        
        def __repr__(self) -> str:
            return f"NeonObject(api_key={self._api_key}, operation={self._operation})"
        
        def get(self, id:str):
            return self._requester.GET(f"{self._operation}/{id}")

        def delete(self,id:str):
            pass

        def name(self):
            self._obj["name"]

        def id(self):
            self._obj["id"]

class NeonProject(NeonObject):

    def __init__(self, api_key:str) -> None:
        NeonObject.__init__(self, api_key, "projects")

    def get_list(self):
            l = self._requester.GET(self._operation)[self._operation]
            for item  in l:
                yield item

    def get_projects(self):
        yield from self.get_list()

    def create_project(self, name:str):
        payload = {"project": {"name": name}}
        return self._requester.POST(f"projects", data=payload)
    
    def delete_project(self, id:str):
        return self._requester.DELETE(f"projects/{id}")

    def __str__(self) -> str:
        return f"api_key={self._api_key}\noperation={self._operation}"

class NeonBranch(NeonObject):

    def __init__(self, api_key:str, project_id) -> None:
        NeonObject.__init__(self, api_key, "branches")
        self._project_id = project_id
                                   
    def get_list(self):
        path = f"projects/{self._project_id}/branches"
        l = self._requester.GET(path)[self._operation]
        for i in l:
            yield i

    def get(self, project_id:str, branch_id:str):
        path = f"projects/{project_id}/branches/{branch_id}"
        return self._requester.GET(path)
    
    def create_branch(self, project_id:str):
        return self._requester.POST(f"projects/{project_id}/{self.operation}")
    
    def delete_branch(self, project_id:str, branch_id:str):
        return self._requester.DELETE(f"projects/{project_id}/{self.operation}/{branch_id}")

    def __str__(self) -> str:
        return f"api_key={self._api_key}\noperation={self._operation}"

