import argparse
import sys

from pyneoncli.clicommands import CLICommands


class CLIBranch(CLICommands):

    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__(args)

    def create_one_branch(self, project_id: str):
        project = self._api.get_project(project_id)
        branch = self._api.create_branch(project.id)
        self._p.print(branch.obj_data)
        return branch

    def create_branch(self, project_ids: list[str]):
        branches = []
        for project_id in project_ids:
            branch = self.create_one_branch(project_id)
            branches.append(branch)
        return branches

    def delete_branch(self, branch_ids: list[str]):
        if branch_ids is not None and type(branch_ids) is list:
            for id in branch_ids:
                pid, bid = id.strip().split(":")
                b = self._api.delete_branch(pid, bid)
                self._p.print(b.obj_data)
        else:
            self._msg.error("You must specify a branch id with --branch_id for delete branch")
            sys.exit(1)
