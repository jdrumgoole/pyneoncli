import json
import pprint
import sys
import requests

from pyneoncli.printer import Printer

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
            Printer.error(err)
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

    def HEAD(self, operation:str, **kwargs):
        return self.request("HEAD", operation, **kwargs)

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
            self._data = self._requester.GET(f"{self._operation}/{id}")["project"]
            return self._data

        def delete(self,id:str):
            pass




class NeonProject(NeonObject):

    def __init__(self, api_key:str, id=None) -> None:
        NeonObject.__init__(self, api_key, "projects", id)
        if self.id  is not None:
            self._data = self.get_project(self._id)

    @property
    def project(self):
        return self._data
    
    def get_projects(self):
        l = self._requester.GET(self._operation)[self._operation]
        for item  in l:
            yield item

    def get_project_ids(self):
        l = self._requester.GET(self._operation)[self._operation]
        for item  in l:
            yield item["id"]

    def get_project_names(self):
        l = self._requester.GET(self._operation)[self._operation]
        for item  in l:
            yield item["id"]

    def get_project_name_id(self):
        l = self._requester.GET(self._operation)[self._operation]
        for item  in l:
            yield item["name"], item["id"]


    def get_project(self, id:str):
         self._data = self.get(id)
         self._id = self._data["id"]
         return self._data
    
    def create_project(self, project_name:str) -> dict:
        # Project name must be unique
        payload = {"project": {"name": project_name}}
        self._data = self._requester.POST(f"projects", data=payload)
        self._id = self._data["project"]["id"]
        return self._data
    
    
    def delete_project(self, id:str=None):
        return self._requester.DELETE(f"projects/{id}")

class NeonBranch(NeonObject):

    def __init__(self, api_key:str, project_id:str=None, id:str=None) -> None:
        NeonObject.__init__(self, api_key=api_key, operation="branches", id=id)
        self._project_id = project_id
        self._id = id
        self._data = None
        if id is not None and project_id is not None:
            self._data = self.get_branch(self._id)
                                   
    def get_branches(self):
        path = f"projects/{self._project_id}/branches"
        l = self._requester.GET(path)[self._operation]
        for i in l:
            yield i

    def get_branch(self, id:str):
        path = f"projects/{self._project_id}/branches/{id}"
        self._data = self._requester.GET(path)["branch"]
        self._id = self._data["id"]
        #print(type(self._data))
        return self._data
    
    def create_branch(self):
        self._data = self._requester.POST(f"projects/{self._project_id}/{self.operation}")
        return self._data
    
    def delete_branch(self, branch_id:str):
        return self._requester.DELETE(f"projects/{self._project_id}/{self.operation}/{branch_id}")

    def __str__(self) -> str:
        return f"api_key={self._api_key}\noperation={self._operation}\nproject_id={self._project_id}"

