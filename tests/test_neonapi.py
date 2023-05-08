import os
import pytest

from neon_api import NeonAPI

PGHOST=os.getenv( "PGHOST", "localhost")
PGPORT=os.getenv( "PGPORT", "5432")
PGURL=os.getenv( "PGURL", "postgresql://localhost:5432")
NEON_API_KEY=os.getenv( "NEON_API_KEY")

assert NEON_API_KEY is not None

@pytest.fixture
def neonapi():
    return NeonAPI(key=NEON_API_KEY, pghost=PGHOST, pgport=PGPORT, pgurl=PGURL)


def test_validate(neonapi):
    neonapi.validate_key()