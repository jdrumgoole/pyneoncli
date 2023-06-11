import json
import os
import subprocess
import unittest

from pyneoncli.configfile import NeonConfigFile
from pyneoncli.neonapi import NeonAPI
from .utils import generate_random_name


class CommandExecutionTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self._cfg = NeonConfigFile()
        self._api = NeonAPI(self._cfg.api_key)

    def _test_command_execution(self, command):
        try:
            # Execute the command and capture the output
            output = subprocess.check_output(command, shell=True, universal_newlines=True).strip()
            return output
        except subprocess.CalledProcessError as e:
            # The command execution failed
            self.fail(f"Command '{command}' failed with error code {e.returncode}")

    def test_neon_command_help(self):
        output = self._test_command_execution("neoncli --help")
        lines = output.splitlines()
        self.assertEqual(lines[0], "usage: neoncli [-h] [--apikey APIKEY] [--version] [--nocolor] [--yes]",
                         lines[0])

    def test_neon_command_project(self, project_id=None):

        output = self._test_command_execution(f"neoncli list")
        starting_line_count = len(output.splitlines())
        project_name = generate_random_name(prefix="test_neon_command_project", length=3)
        self.assertTrue(self._cfg.api_key, "neoncli.conf: api key not set")
        output = self._test_command_execution(f"neoncli project --create {project_name}")
        create_doc = json.loads(output)
        self.assertEqual(create_doc["name"], project_name)

        project_id = create_doc["id"]
        output = self._test_command_execution(f"neoncli list --project_id {project_id}")
        list_doc = json.loads(output)
        self.assertEqual(list_doc["name"], project_name)
        self.assertEqual(list_doc["id"], project_id)

        output = self._test_command_execution(f"neoncli --yes project --delete {project_id}")
        delete_doc = json.loads(output)
        self.assertEqual(delete_doc["name"], project_name)

        output = self._test_command_execution(f"neoncli list")

        ending_line_count = len(output.splitlines())

        self.assertEqual(starting_line_count, ending_line_count)

    def test_neon_command_branch(self):

        # create a project to test branches
        project_name = generate_random_name(prefix="test_neon_command_branch", length=3)

        output = self._test_command_execution(f"neoncli project --create {project_name}")
        branch_test_project_doc = json.loads(output)
        self.assertEqual(branch_test_project_doc["name"], project_name)
        project_id = branch_test_project_doc["id"]

        output = self._test_command_execution(f"neoncli list --branches {project_id}")
        starting_line_count = len(output.splitlines())

        output = self._test_command_execution(f"neoncli branch --create {project_id}")
        branch_doc = json.loads(output)
        self.assertEqual(branch_doc["project_id"], project_id)

        branch_id = branch_doc["id"]
        output = self._test_command_execution(f"neoncli list --branch_id {project_id}:{branch_id}")

        output = self._test_command_execution(f"neoncli --yes branch --delete {project_id}:{branch_id}")
        delete_doc = json.loads(output)
        self.assertEqual(delete_doc["id"], branch_id)

        output = self._test_command_execution(f"neoncli list --branches {project_id}")
        ending_line_count = len(output.splitlines())
        self.assertEqual(starting_line_count, ending_line_count)

        delete_output = self._test_command_execution(f"neoncli --yes project --delete {project_id}")
        delete_doc = json.loads(delete_output)
        self.assertEqual(delete_doc["name"], project_name)

    def test_neon_operations(self):

        project = self._api.create_project(generate_random_name(prefix="test_neon_operations", length=3))
        ops = self._api.get_operations(project.id)
        op = next(ops)
        detail = self._api.get_operation(project.id, op.id)
        output = self._test_command_execution(f"neoncli list  --operations {project.id}")
        self.assertTrue(len(output.splitlines()) > 0)
        output = self._test_command_execution(f"neoncli --nocolor list  --operation_detail {project.id}:{op.id}")
        op_doc = json.loads(output)
        self.assertEqual(op_doc["id"], op.id)
        self._api.delete_project(project.id)

    def test_list_by_name(self):
        project1 = self._api.create_project(generate_random_name(prefix="test_list_by_name", length=3))
        project2 = self._api.create_project(generate_random_name(prefix="test_list_by_name", length=3))
        output = self._test_command_execution(f"neoncli list --project_name {project1.name}")
        self._api.delete_project(project1.id)
        self._api.delete_project(project2.id)

if __name__ == '__main__':
    unittest.main()
