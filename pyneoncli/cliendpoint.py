import argparse

from pyneoncli.clicommands import CLICommands


class CLIEndPoint(CLICommands):
    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__(args)

    def create_endpoint(self, create_id: str):
        project_id, branch_id = create_id.strip().split(":")
        endpoint = self._api.create_endpoint(project_id, branch_id)
        self._p.print(endpoint.obj_data)
        return endpoint

    def delete_endpoint(self, delete_id: str):
        project_id, endpoint_id = delete_id.strip().split(":")
        endpoint = self._api.delete_endpoint(project_id, endpoint_id)
        self._p.print(endpoint.obj_data)
        return endpoint
