import sys
import json
import argparse

from pyneoncli.neon import NeonBranch, NeonProject
from pyneoncli.rawneonapi import NeonAPI, NeonAPIException, NeonTimeoutException
from pyneoncli.printer import ColorText, Printer


class CLICommands:

    def __init__(self, args: argparse.Namespace) -> None:
        self._args = args
        self._api_key = args.apikey
        self._api = NeonAPI(args.apikey)
        if args is None:
            self._p = Printer()
            self._c = ColorText()
        else:
            self._p = Printer(nocolor=args.nocolor, filters=args.fieldfilter)
            self._c = ColorText(nocolor=args.nocolor)

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value
        self._p = Printer(nocolor=self._args.nocolor, filters=self._args.fieldfilter)
        self._c = ColorText(nocolor=self._args.nocolor)


class CLIList(CLICommands):

    def __init__(self, args: argparse.Namespace = None) -> None:
        super().__init__(args)

    def list_all(self):
        for p in self._api.get_projects():

            print(f"{self._p.project_id(p)}")
            for branch in self._api.get_branches(p.id):
                print(f"  {self._p.branch_id(branch)}")

    def list_projects(self, project_ids: list[str] = None):
        if project_ids is None:
            for p in self._api.get_projects():
                print(f"{self._p.project_id(p)}")
        elif type(project_ids) is list:
            if len(project_ids) == 0:
                for p in self._api.get_projects():
                    print(f"{self._p.project_id(p)}")
            else:
                for project_id in project_ids:
                    p = self._api.get_project_by_id(project_id)
                    print(f"{self._p.project_id(p)}")
        else:
            print(f"Wrong argument type for list_projects: {type(project_ids)}")
            sys.exit(1)

    def list_branches_for_project(self, p: NeonProject):
        for b in self._api.get_branches(p.id):
            print(f"  {self._p.branch_id(b)}")

    def list_branches_for_projects(self, project_ids: list[str]):
        for i in project_ids:
            project = self._api.get_project_by_id(i)
            self.list_branches_for_project(project)

    def list_branches_for_branch_ids(self, branch_ids: list[str]):
        for i in branch_ids:
            this_pid, this_bid = i.strip().split(":")
            p = self._api.get_project_by_id(this_pid)
            print(f"{self._p.project_id(p)}")
            for b in self._api.get_branches(p.id):
                if this_bid == b.id:
                    print(f"  {self._p.branch_id(b)}")


class CLIProject(CLICommands):

    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__(args)

    def create_project(self, project_names: list[str]) -> list[str]:
        project_ids = []
        if project_names is not None and type(project_names) is list:
            for project_name in project_names:
                project = self._api.create_project(project_name)
                project_ids.append(project.id)
                self._p.print(project.data)
        return project_ids

    def delete_project(self, project_ids: list[str]):
        ids = []
        if project_ids is not None and type(project_ids) is list:
            for project_id in project_ids:
                project = self._api.delete_project(project_id)
                self._p.print(project.data)
                ids.append(project.id)
        else:
            print("You must specify a project id with --project_id for delete project")
            sys.exit(1)
        return ids

    def delete_all_projects(self):
        project_ids = []
        any_ids = False
        for project in self._api.get_projects():
            self._api.delete_project(project.id)
            project_ids.append(project.id)
            print(f"{project.id} deleted")
            any_ids = True
        if not any_ids:
            print("No projects to delete")
        return project_ids


class CLIBranch(CLICommands):

    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__(args)

    def create_branch(self, project_ids: list[str]):
        branches = []
        for project_id in project_ids:
            np = NeonProject()
            project = self._api.get_project_by_id(project_id)
            branch = self._api.create_branch(project_id)
            self._p.print(branch.data)
            branches.append(branch)
        return branches

    def delete_branch(self, branch_ids: list[str]):
        if branch_ids is not None and type(branch_ids) is list:
            for id in branch_ids:
                pid, bid = id.strip().split(":")
                b = self._api.delete_branch(pid.bid)
                self._p.print(b)
        else:
            print("You must specify a branch id with --branch_id for delete branch")
            sys.exit(1)
        return b


class CLIDispatcher:

    def __init__(self) -> None:
        self._printer = Printer()

    def dispatch_list(self, args: argparse.Namespace):

        try:
            any_args = False
            l = CLIList(args)
            if args.all:
                l.list_all()
                any_args = True
            elif args.branch_ids:
                l.list_branches_for_branch_ids(args.branch_ids)
                any_args = True
            elif args.project_ids:
                l.list_projects(args.project_ids)
                any_args = True
            elif args.projects:
                l.list_projects()
                any_args = True

            elif args.branch_ids:
                l.list_branches_for_branch_ids(args.branch_ids)
                any_args = True

            if not any_args:
                l.list_all()

        except NeonAPIException as api_error:
            print(api_error)
            sys.exit(1)

        except NeonTimeoutException as timeout_error:
            print(timeout_error)
            sys.exit(1)


    @staticmethod
    def dispatch_project(args: argparse.Namespace):
        p = CLIProject(args)
        if args.create_names:
            p.create_project(args.create_names)
        if args.delete_ids:
            p.delete_project(args.delete_ids)
        if args.delete_all:
            p.delete_all_projects()

    @staticmethod
    def dispatch_branch(args: argparse.Namespace):
        b = CLIBranch(args=args)
        if args.project_ids:
            b.create_branch(args.project_ids)
        if args.delete_ids:
            b.delete_branch(args.delete_ids)
