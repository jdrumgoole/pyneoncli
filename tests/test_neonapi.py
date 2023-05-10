import os
import pprint
import pytest

from pyneoncli.neon_api import NeonAPI, Requester, NeonProject

NEON_API_KEY=os.getenv( "NEON_API_KEY")
assert NEON_API_KEY is not None

@pytest.fixture
def neonapi():
    return NeonAPI(key=NEON_API_KEY)

@pytest.fixture
def neonproject():
    return NeonProject(api_key=NEON_API_KEY)    

@pytest.fixture
def requester():
    return Requester(key=NEON_API_KEY)   

def test_validate(neonapi):
    neonapi.validate_key()


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
