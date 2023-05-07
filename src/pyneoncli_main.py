import argparse
import os
from neon_api import NeonAPI
import pprint
NEON_API_KEY = None
PGHOST= 5432
PGHOST="localhost"
PGUSER=os.getenv("USERNAME", "postgres")
PGPASSWORD=""
PGDATABASE="postgres"

def get_default_from_env(env_var, default):
    return os.getenv(env_var, default
                     )
def detect_defaults():
    apikey = os.getenv('APIKEY', 'defaultapikey')
    pghost = os.getenv('PGHOST', 'localhost')
    pgport = os.getenv('PGPORT', '5432')
    pgurl = os.getenv('PGURL', 'postgresql://user:password@localhost:5432/dbname')
    return apikey, pghost, pgport, pgurl

def main(apikey, pghost, pgport, pgurl):
    print(f"API Key: {apikey}")
    print(f"PostgreSQL Host: {pghost}")
    print(f"PostgreSQL Port: {pgport}")
    print(f"PostgreSQL URL: {pgurl}")
    api = NeonAPI(key=apikey)
    r = api.validate_key()
    print(r.status_code)
    print(r.url)
    pprint.pprint(r.json())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('--apikey', type=str, help='API Key')
    parser.add_argument('--pghost', type=str, help='PostgreSQL Host', default=os.getenv( "PGHOST", "localhost"))
    parser.add_argument('--pgport', type=str, help='PostgreSQL Port', default=os.getenv( "PGPORT", "5432"))
    parser.add_argument('--pgurl', type=str, help='PostgreSQL URL', default=os.getenv( "PGURL", "postgresql://localhost:5432"))

    args = parser.parse_args()

    main(args.apikey, args.pghost, args.pgport, args.pgurl)
