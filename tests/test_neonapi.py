import os
import pprint
import pytest

from pyneoncli.neon_api import Requester, NeonProject, dict_filter


NEON_API_KEY=os.getenv( "NEON_API_KEY")
assert NEON_API_KEY is not None

@pytest.fixture
def neonproject():
    return NeonProject(api_key=NEON_API_KEY)    

@pytest.fixture
def requester():
    return Requester(key=NEON_API_KEY)   

def test_requester(requester):
    assert requester is not None
    p = requester.GET("projects")
    assert p is not None

def test_neonproject(neonproject):
    assert neonproject is not None
    p = neonproject.get_projects()
    assert p is not None
    plist = list(p)
    assert type(plist) == list

d = {
    "branch": {
        "active_time_seconds": 0,
        "compute_time_seconds": 0,
        "cpu_used_sec": 0,
        "created_at": "2023-05-11T09:25:02Z",
        "creation_source": "console",
        "current_state": "ready",
        "data_transfer_bytes": 0,
        "id": "br-lingering-resonance-821551",
        "name": "br-lingering-resonance-821551",
        "parent_id": "br-muddy-wildflower-293772",
        "parent_lsn": "0/2825F40",
        "primary": False,
        "project_id": "red-sea-544606",
        "updated_at": "2023-05-11T09:26:27Z",
        "written_data_bytes": 0
    },
    "operations": [
        {
            "action": "delete_timeline",
            "branch_id": "br-lingering-resonance-821551",
            "created_at": "2023-05-11T09:26:27Z",
            "failures_count": 0,
            "id": "b7fbecf4-3275-4b7e-a96f-da65fd5a8933",
            "project_id": "red-sea-544606",
            "status": "running",
            "updated_at": "2023-05-11T09:26:27Z"
        }
    ]
}

def test_dict_filter():
    assert dict_filter(d, "branch.id") == {"branch.id": "br-lingering-resonance-821551"}
