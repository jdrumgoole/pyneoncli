import argparse
import sys

from pyneoncli.clicommands import CLICommands
from pyneoncli.neonapiexceptions import NeonAPIException


class CLIProject(CLICommands):

    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__(args)

    def create_one_project(self, project_name: str):
        project = self._api.create_project(project_name)
        self._p.print(project.obj_data)
        return project

    def create_project(self, project_names: list[str]) -> list[str]:
        project_ids = []
        if project_names is not None and type(project_names) is list:
            for project_name in project_names:
                try:
                    p = self.create_one_project(project_name)
                    project_ids.append(p.id)
                except NeonAPIException as e:
                    self.report_exception(e, "create project", project_name)
                    sys.exit(1)

        if len(project_ids) == 0:
            raise NeonAPIException("No projects created")
        return project_ids

    def delete_one_project(self, project_id: str, check=True):
        if check:
            resp = self._msg.prompter(msg=f"Are you sure you want to delete project {project_id}? (y/n): ",
                                      expected=["y", "Y", "yes", "Yes", "YES"],
                                      yes=self._args.yes)
            if resp:
                project = self._api.delete_project(project_id)
                self._p.print(project.obj_data)
                return project
            else:
                self._msg.warning("Aborted project deletion")
                return None
        else:
            project = self._api.delete_project(project_id)
            self._p.print(project.obj_data)
            return project

    def delete_projects(self, project_ids: list[str], check=True) -> list[str]:
        deleted_project_ids = []
        if project_ids is not None and type(project_ids) is list:
            for project_id in project_ids:
                try:
                    p = self.delete_one_project(project_id, check=check)
                    if p is not None:
                        deleted_project_ids.append(p.id)
                except NeonAPIException as e:
                    self.report_exception(e, "delete project", project_id)
        else:
            self._msg.error("You must specify a project id with --project_id for delete project")
            sys.exit(1)
        return deleted_project_ids

    def delete_all_projects(self):
        project_ids = []
        any_ids = False
        resp = self._msg.prompter(msg=f"Are you sure you want to delete all projects? (y/n): ",
                                  expected=["y", "Y", "yes", "Yes", "YES"],
                                  yes=self._args.yes)
        if resp is not None:
            for project in self._api.get_projects():
                self._api.delete_project(project.id)
                project_ids.append(project.id)
                self.print_obj_id("", project, sep="", end="")
                self._msg.green(f" deleted")
                any_ids = True
            if not any_ids:
                self._msg.info("No projects to delete")
            return project_ids
        else:
            self._msg.warning("Aborting delete all projects")
            return None
