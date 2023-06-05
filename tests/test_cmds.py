import json
import os
import subprocess
from time import sleep
import unittest

from pyneoncli.neon import NeonProject
from pyneoncli.printer import Printer


class CommandExecutionTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self._apiKey = os.getenv("NEON_API_KEY")
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
        project_name = "test_project"
        self.assertTrue(self._apiKey is not None, "NEON_API_KEY environment variable must be set")
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
        project_name = "branch_test_project"

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


if __name__ == '__main__':
    unittest.main()
