import argparse
import os
import sys
from dotenv import load_dotenv

from pyneoncli.clicommands import CLIDispatcher
from pyneoncli.version import __VERSION__

NEON_API_KEY = None

epilog = f'''
use neoncli list  -h for more information on the list command
use neoncli branch  -h for more information on the branch command
use neoncli project -h for more information on the project command

Version : {__VERSION__}

'''

def main():

    load_dotenv()
    dispatcher = CLIDispatcher()
    parser = argparse.ArgumentParser(description='neoncli - python neon api client (Python 3.8+))',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=epilog)
    parser.add_argument('--apikey', type=str, help='Specify NEON API Key (env NEON_API_KEY)', default=os.getenv( "NEON_API_KEY"))
    parser.add_argument("--version", action="version", version=f"neoncli {__VERSION__}")
    parser.add_argument("--nocolor", action="store_true", default=False, help="Turn off Color output")
    parser.add_argument( '-f', '--fieldfilter', action="append", type=str, help='Enter field values to filter results on')

    subparsers = parser.add_subparsers(dest='command', help='Neon commands')

    # List
    list_parser = subparsers.add_parser('list', help='List Neon objects')
    list_parser.add_argument('-a', '--all', action="store_true", default=False, help='List all objects')
    list_parser.add_argument('-p', '--projects', action='store_true', default=False, help='list projects')
    list_parser.add_argument('-b', '--branches', action="append", dest="project_ids", help='List branches associated with project_id(s)')
    list_parser.add_argument('-pi', '--project_id', action="append", dest="project_ids",  type=str, help='List projects specificed by project_id')
    list_parser.add_argument('-bi', '--branch_id', action="append", dest="branch_ids",  type=str, help='List branches specificed by project_id:branch_id')
    list_parser.set_defaults(func=dispatcher.dispatch_list)

    # Projects
    project_parser = subparsers.add_parser('project', help='Create and delete Neon projects')
    project_parser.add_argument('-c', '--create', action="append", dest="create_names", type=str,  help='create project')
    project_parser.add_argument('-d', '--delete', action="append", dest="delete_ids",  type=str, help='delete project')
    project_parser.add_argument('--delete_all', action="store_true", default=False,  help='delete all projects')

    project_parser.set_defaults(func=dispatcher.dispatch_project)

    # Branches
    branch_parser = subparsers.add_parser('branch', help='create and delete Neon branches')
    branch_parser.add_argument('-c', '--create', action="append",  dest="project_ids", type=str, help='create branch on the project specified by project id')
    branch_parser.add_argument('-d', '--delete', action="append", dest="delete_ids", type=str,  help='delete branches specified by project_id:branch_id')
    branch_parser.add_argument('--delete_all', action="store_true", default=False,  help='delete all branches')

    branch_parser.set_defaults(func=dispatcher.dispatch_branch)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting : Ctrl-C detected")
        sys.exit(1)