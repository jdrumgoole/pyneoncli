import os
import pprint
import unittest
import time

from pyneoncli.rawneonapi import RawNeonAPI
from pyneoncli.printer import dict_filter

NEON_API_KEY = os.getenv("NEON_API_KEY")
assert NEON_API_KEY is not None, "NEON_API_KEY environment variable must be set"


class TestNeonAPI(unittest.TestCase):
    def setUp(self):
        self._api = RawNeonAPI(NEON_API_KEY)

    def test_create_project(self):
        project = self._api.create_project("test_project")
        self.assertEqual(self._api.is_complete(project.id), True)
        self._api.delete_project(project.id)

    def test_create_delete_list_project(self):
        project_name = "test_project"
        project = self._api.create_project(project_name)
        self.assertEqual(self._api.is_complete(project.id), True)
        project_id = project.id
        self.assertTrue(any((p.id == project_id) for p in self._api.get_projects()))
        project = self._api.delete_project(project_id)
        self.assertEqual(project.name, project_name)
        self.assertTrue(any((p.id != project_id) for p in self._api.get_projects()))

    def test_create_delete_branch(self):
        project_name = "branch_test_project"
        project = self._api.create_project(project_name)
        self.assertEqual(self._api.is_complete(project.id), True)
        self.assertEqual(project.name, project_name)
        project = self._api.get_project_by_id(project.id)
        self.assertEqual(self._api.is_complete(project.id), True)
        self.assertEqual(project.name, project_name)
        branch = self._api.create_branch(project.id)
        self.assertEqual(self._api.is_complete(project.id), True)
        self.assertEqual(branch.project_id, project.id)
        self._api.delete_branch(project.id, branch.id)
        self.assertEqual(self._api.is_complete(project.id), True)
        self._api.delete_project(project.id)

    def test_dict_filter(self):
        d = {
            "branch": {
                "active_time_seconds": 0,
                "compute_time_seconds": 0,
                "cpu_used_sec": 0,
                "created_at": "2023-05-11T09:25:02Z",
                "creation_source": "console",
                "current_state": "ready",
                "data_transfer_bytes": 0,
                "id": "br-lingering-resonance-821551",
                "name": "br-lingering-resonance-821551",
                "parent_id": "br-muddy-wildflower-293772",
                "parent_lsn": "0/2825F40",
                "primary": False,
                "project_id": "red-sea-544606",
                "updated_at": "2023-05-11T09:26:27Z",
                "written_data_bytes": 0
            },
            "operations": [
                {
                    "action": "delete_timeline",
                    "branch_id": "br-lingering-resonance-821551",
                    "created_at": "2023-05-11T09:26:27Z",
                    "failures_count": 0,
                    "id": "b7fbecf4-3275-4b7e-a96f-da65fd5a8933",
                    "project_id": "red-sea-544606",
                    "status": "running",
                    "updated_at": "2023-05-11T09:26:27Z"
                }
            ]
        }
        assert dict_filter(d, ["branch.id"]) == {"branch.id": "br-lingering-resonance-821551"}


if __name__ == '__main__':
    unittest.main()
