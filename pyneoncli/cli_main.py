import argparse
import os

import pprint
from typing import Any
import json

from pygments import highlight
from pygments.formatters import TerminalTrueColorFormatter
from pygments.lexers import JsonLexer

from pyneoncli.neon_api import  NeonBranch, NeonProject
from pyneoncli.version import __VERSION__


NEON_API_KEY = None

def pprint_color(obj: Any, nocolor: bool) -> None:
    """Pretty-print in color."""
    json_str = json.dumps(obj, indent=4, sort_keys=True)
    if nocolor:
        print(json_str)
    else:
        print(highlight(json_str, JsonLexer(), TerminalTrueColorFormatter()), end="")



class CLI_Commands:

    def __init__(self) -> None:
        pass

    @staticmethod
    def print_list(l:list, nocolor: bool= False, fields:list=None):
        for i in l:
            d = CLI_Commands.filter_dict(i, fields)
            pprint_color(d, nocolor)

    @staticmethod
    def filter_dict(input_dict, fieldfilter):
        if fieldfilter is None or len(fieldfilter) == 0:
            return input_dict
        output_dict = {}
        for field in fieldfilter:
            if field in input_dict:
                output_dict[field] = input_dict[field]
        return output_dict
    
    @staticmethod
    def project(args:argparse.Namespace):
        projects =NeonProject(api_key=args.apikey)

        if args.create:
            p = projects.create_project(args.create)
            pprint_color(p, args.nocolor)
        if args.id:
            p = projects.get(args.id)
            pprint_color(p, args)
        if args.list:
                projects = projects.get_projects()
                CLI_Commands.print_list(projects, args.nocolor, args.fieldfilter)
        if args.delete:
            p = projects.delete_project(args.delete)
            pprint_color(p, args.nocolor)

    @staticmethod
    def branch(args:argparse):
        branches = NeonBranch(api_key=args.apikey, project_id=args.project_id)
        if args.list:
            branches = branches.get_list()
            CLI_Commands.print_list(branches, args.nocolor, args.fieldfilter)

def main():
    parser = argparse.ArgumentParser(description='neoncli - python neon api client', 
                                     epilog=f"Version : {__VERSION__}")
    parser.add_argument('--apikey', type=str, help='Specify NEON API Key (env NEON_API_KEY)', default=os.getenv( "NEON_API_KEY"))
    parser.add_argument("--version", action="version", version=f"neoncli {__VERSION__}")
    parser.add_argument("--nocolor", action="store_true", default=False, help="Turn off Color output")
    parser.add_argument( '-f', '--fieldfilter', action="append", type=str, help='Enter field values to filter results on')


    subparsers = parser.add_subparsers(dest='command', help='Neon commands')

    # Projects
    project_parser = subparsers.add_parser('project', help='maninpulate Neon projects')
    project_parser.add_argument('-c', '--create', type=str,  help='create project')
    project_parser.add_argument('-i', '-id', type=str, dest="id",  help='project details')
    project_parser.add_argument('-l', '--list', help='List projects', action='store_true')
    project_parser.add_argument('-d', '--delete', type=str,  help='delete project')


    project_parser.set_defaults(func=CLI_Commands.project)

    # Branches
    branch_parser = subparsers.add_parser('branch', help='manuinplate Neon branches')
    branch_parser.add_argument('-p', '--project_id', type=str, dest="project_id",  
                               help='specify project id', required=True)
    branch_parser.add_argument('-l', '--list', help='List branches', action='store_true')
    branch_parser.add_argument('-c', '--create', type=str, dest="name",  help='create branch')
    branch_parser.add_argument('-d', '--delete', type=str, dest="id",  help='delete branch')
    branch_parser.set_defaults(func=CLI_Commands.branch)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
