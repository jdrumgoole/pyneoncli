import json
import pprint
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
            #print(path)
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
            if root is None:
                yield k, v
            else:
                yield f"{root}.{k}", v

class NeonObject:
    
        def __init__(self, api_key:str, operation=None, id=None) -> None:
            self._api_key = api_key
            self._operation = operation
            self._id = id
            self._requester = Requester(key=self._api_key)
            self._obj = {}

        @property
        def data(self):
            return self._data
        
        @property
        def id(self):
            return self._id
        
        @property
        def name(self):
            return self._data[self._operation]["name"]
        
        @property
        def operation(self):
            return self._operation
    
        def __str__(self) -> str:
            return pprint.pformat(self._data)
        
        def __repr__(self) -> str:
            return f"NeonObject(api_key={self._api_key}, operation={self._operation}, id={self._id})"
        
        def get(self, id:str):
            self._data = self._requester.GET(f"{self._operation}/{id}")
            return self._data

        def delete(self,id:str):
            pass




class NeonProject(NeonObject):

    def __init__(self, api_key:str, id=None) -> None:
        NeonObject.__init__(self, api_key, "projects", id)
        self.get_project(self._id)

    @property
    def project(self):
        return self._data
    
    def get_projects(self):
        l = self._requester.GET(self._operation)[self._operation]
        for item  in l:
            yield item

    def get_project(self, id:str):
         self._data = self.get(id)
         return self._data
    
    def create_project(self, name:str):
        # Project name must be unique
        payload = {"project": {"name": name}}
        self._data = self._requester.POST(f"projects", data=payload)
        self._id = self._data["project"]["id"]
        return self._data
    
    
    def delete_project(self, id:str=None):
        return self._requester.DELETE(f"projects/{id}")

class NeonBranch(NeonObject):

    def __init__(self, api_key:str, id:str, project_id) -> None:
        NeonObject.__init__(self, api_key=api_key, operation="branches", id=id)
        self._project_id = project_id
        self._data = self.get(self._id)
                                   
    def get_list(self):
        path = f"projects/{self._project_id}/branches"
        l = self._requester.GET(path)[self._operation]
        for i in l:
            yield i

    def get(self, id:str):
        path = f"projects/{self._project_id}/branches/{branch_id}"
        self._data = self._requester.GET(path)
        return self._data
    
    def create_branch(self):
        self._data = self._requester.POST(f"projects/{self._project_id}/{self.operation}")
        return self._data
    
    def delete_branch(self, branch_id:str):
        return self._requester.DELETE(f"projects/{self._project_id}/{self.operation}/{branch_id}")

    def __str__(self) -> str:
        return f"api_key={self._api_key}\noperation={self._operation}\nproject_id={self._project_id}"

