import os
import pprint
import unittest

from pyneoncli.configfile import NeonConfigFile
from pyneoncli.neon import NeonProject
from pyneoncli.neonapi import NeonAPI
from pyneoncli.rawneonapi import RawNeonAPI
from pyneoncli.printer import dict_filter
from tests.utils import generate_random_name


class TestRawNeonAPI(unittest.TestCase):
    def setUp(self):
        self._cfg = NeonConfigFile()
        self._rawapi = RawNeonAPI(self._cfg.api_key)
        self._api = NeonAPI(self._cfg.api_key)
        self._projects = []

    def tearDown(self):
        for project in self._projects:
            self._rawapi.delete_project(project.id)

    def test_create_raw_project(self):
        project_name = generate_random_name(prefix="test_create_raw_project", length=3)
        project = self._rawapi.create_project(project_name)
        self._projects.append(project)
        self.assertEqual(self._rawapi.is_complete(project.id), True)
        self.assertEqual(project.name, project_name)
        self.assertGreater(len(project.id), 0)

    def test_paginate(self):
        project_count = self._rawapi.count_projects()
        project1 = self._rawapi.create_project(generate_random_name(prefix="test_paginate", length=3))
        project2 = self._rawapi.create_project(generate_random_name(prefix="test_paginate", length=3))
        project3 = self._rawapi.create_project(generate_random_name(prefix="test_paginate", length=3))
        self._projects.extend([project1, project2, project3])

        projects = list(self._rawapi.get_projects())
        self.assertEqual(len(projects), project_count + 3)

        self.assertTrue(all((isinstance(p, NeonProject) for p in projects)))

    def test_create_delete_list_project(self):
        project_name = generate_random_name(prefix="test_create_delete_list_project", length=3)
        project = self._rawapi.create_project(project_name)
        self.assertEqual(self._rawapi.is_complete(project.id), True)
        project_id = project.id
        self.assertTrue(any((p.id == project_id) for p in self._rawapi.get_projects(batch_size=2)))
        project = self._rawapi.delete_project(project_id)
        self.assertEqual(project.name, project_name)
        for p in self._rawapi.get_projects():
            self.assertTrue(p.id != project_id)

    def test_create_delete_branch(self):
        project_name = generate_random_name(prefix="test_create_delete_branch", length=3)
        project = self._rawapi.create_project(project_name)
        self._projects.append(project)
        self.assertEqual(self._rawapi.is_complete(project.id), True)
        self.assertEqual(project.name, project_name)
        project = self._rawapi.get_project(project.id)
        self.assertEqual(self._rawapi.is_complete(project.id), True)
        self.assertEqual(project.name, project_name)
        branch = self._rawapi.create_branch(project.id)
        self.assertEqual(self._rawapi.is_complete(project.id), True)
        self.assertEqual(branch.project_id, project.id)
        self._rawapi.delete_branch(project.id, branch.id)
        self.assertEqual(self._rawapi.is_complete(project.id), True)

    def test_operations(self):
        project_name = generate_random_name(prefix="test_operations", length=3)
        project = self._api.create_project(project_name)
        self._projects.append(project)
        self.assertEqual(self._rawapi.is_complete(project.id), True)
        for op in self._api.get_operations(project.id):
            self.assertEqual(op.project_id, project.id)
            op_inner = self._api.get_operation(project.id, op.id)
            self.assertEqual(op_inner, op)


class TestNeonAPI(unittest.TestCase):
    def setUp(self):
        self._cfg = NeonConfigFile()
        self._api = NeonAPI(self._cfg.api_key)
        self._projects = []

    def tearDown(self):
        for project in self._projects:
            self._api.delete_project(project.id)

    def test_get_operations(self):
        pass

    def test_create_project(self):
        project_name = generate_random_name(prefix="test_create_project", length=10)
        project = self._api.create_project(project_name)
        self._projects.append(project)
        self.assertTrue(type(project), NeonProject)
        self.assertEqual(project.name, project_name)

    def test_create_delete_list_project(self):
        project_name = generate_random_name(prefix="test_create_delete_list_project", length=3)
        project = self._api.create_project(project_name)
        self.assertEqual(self._api.is_complete(project.id), True)
        self._api.delete_project(project.id)

        for p in self._api.get_projects():
            self.assertTrue(p.id != project.id)

    def test_create_delete_branch(self):
        project_name = generate_random_name(prefix="test_create_delete_branch", length=3)
        project = self._api.create_project(project_name)
        self._api.is_complete(project.id)
        self._projects.append(project)
        self.assertEqual(project.name, project_name)
        branch = self._api.create_branch(project.id)
        self.assertEqual(project.name, project_name)
        self.assertEqual(branch.project_id, project.id)
        self._api.delete_branch(project.id, branch.id)


class TestDictFilter(unittest.TestCase):

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
