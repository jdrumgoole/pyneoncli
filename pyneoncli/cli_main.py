import argparse
import os
from pyneoncli.neon_api import NeonAPI
import pprint
from typing import Any
import json

from pygments import highlight
from pygments.formatters import TerminalTrueColorFormatter
from pygments.lexers import JsonLexer

NEON_API_KEY = None

def pprint_color(obj: Any) -> None:
    """Pretty-print in color."""
    json_str = json.dumps(obj, indent=4, sort_keys=True)
    print(highlight(json_str, JsonLexer(), TerminalTrueColorFormatter()))
class CLI_Commands:

    def __init__(self, api:NeonAPI) -> None:
        self._api = api

    def validate(self):
        if self._api.validate_key():
            print("key is valid")
        else:
            print("key is not valid")

    def list(self):
        for p in self._api.get_projects():
            print(f"name: {p['name']}")
            pprint_color(p)

def get_default_from_env(env_var, default):
    return os.getenv(env_var, default
                     )

def main():
    # print(f"API Key: {apikey}")
    # print(f"PostgreSQL Host: {pghost}")
    # print(f"PostgreSQL Port: {pgport}")
    # print(f"PostgreSQL URL: {pgurl}")
    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('--apikey', type=str, help='Specify NEON API Key (env NEON_API_KEY)', default=os.getenv( "NEON_API_KEY"))
    # parser.add_argument('--pghost', type=str, help='PostgreSQL Host', default=os.getenv( "PGHOST", "localhost"))
    # parser.add_argument('--pgport', type=str, help='PostgreSQL Port', default=os.getenv( "PGPORT", "5432"))
    # parser.add_argument('--pgurl', type=str, help='PostgreSQL URL', default=os.getenv( "PGURL", "postgresql://localhost:5432"))
    parser.add_argument("cmd", nargs="*", choices=["validate", "list"],  help="List projects")
    args = parser.parse_args()
    api = NeonAPI(key=args.apikey)
    cmds = CLI_Commands(api)

    if args.cmd:
        print(f"Command: {args.cmd}")
        if "list" in args.cmd:
            cmds.list()
        if "validate" in args.cmd:
            cmds.validate()

if __name__ == '__main__':
    main()
