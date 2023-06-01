import json
import os
import subprocess
from time import sleep
import unittest

from pyneoncli.neon import NeonProject
from pyneoncli.printer import Printer


class CommandExecutionTestCase(unittest.TestCase):

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
        self.assertEqual(lines[0], "usage: neoncli [-h] [--apikey APIKEY] [--version] [--nocolor] [-f FIELDFILTER]",
                         lines[0])

    def test_neon_command_project(self, project_id=None):

        output = self._test_command_execution(f"neoncli list")
        starting_line_count = len(output.splitlines())
        project_name = "test_project"
        apiKey = os.getenv("NEON_API_KEY")
        self.assertTrue(apiKey is not None, "NEON_API_KEY environment variable must be set")
        output = self._test_command_execution(f"neoncli project --create {project_name}")
        create_doc = json.loads(output)
        self.assertEqual(create_doc["name"], project_name)

        project_id = create_doc["id"]
        output = self._test_command_execution(f"neoncli list --project_id {project_id}")
        ids = [x for x in Printer.parse_name_id_list(output.splitlines()) if (project_name, project_id) == x]

        self.assertTrue((project_id, project_name) in ids, ids)

        output = self._test_command_execution(f"neoncli project --delete {project_id}")
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
        project_id = branch_test_project_doc["project"]["id"]

        output = self._test_command_execution(f"neoncli list --branches {project_id}")
        starting_line_count = len(output.splitlines())

        sleep(5)

        output = self._test_command_execution(f"neoncli branch --create {project_id}")
        branch_doc = json.loads(output)
        self.assertEqual(branch_doc["branch"]["project_id"], project_id)

        branch_id = branch_doc["branch"]["id"]
        output = self._test_command_execution(f"neoncli list --branch_id {project_id}:{branch_id}")

        output = self._test_command_execution(f"neoncli branch --delete {project_id}:{branch_id}")
        delete_doc = json.loads(output)
        self.assertEqual(delete_doc["id"], branch_id)

        output = self._test_command_execution(f"neoncli project --list")

        ending_line_count = len(output.splitlines())

        self.assertEqual(starting_line_count, ending_line_count)


if __name__ == '__main__':
    unittest.main()
