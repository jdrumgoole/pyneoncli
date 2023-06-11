import pprint
import unittest

from requests import HTTPError

from pyneoncli.configfile import NeonConfigFile
from pyneoncli.neon import NeonProject
from pyneoncli.neonapi import NeonAPI
from pyneoncli.neonapiexceptions import NeonAPIException
from pyneoncli.neonliterals import NeonAPIPaths as np, NeonFunction as nf
from pyneoncli.requester import Requester
from pyneoncli.threadedneonapi import ThreadedNeonAPI
from tests.utils import generate_random_name


class TestPaginator(unittest.TestCase):

    def setUp(self):
        self._cfg = NeonConfigFile()
        self._requester = Requester(api_key=self._cfg.api_key)
        self._api = ThreadedNeonAPI(api_key=self._cfg.api_key, thread_count=10)

    def tearDown(self):
        pass

    def test_get_operation(self):
        self._project = self._api.create_project(generate_random_name(prefix="TestPaginator"))
        self._branch = self._api.create_branch(self._project.id)
        op = self._api.get_first_operation(project_id=self._project.id)
        self.assertEqual(op.project_id, self._project.id)
        self._api.delete_project(self._project.id)

    def test_get_paginate(self):
        projects1 = list(self._requester.paginate(np.GET_PROJECTS(), selector=nf.projects()))
        tester = self._api.create_project(generate_random_name(prefix="test_paginate"))
        projects2 = list(self._requester.paginate(np.GET_PROJECTS(), selector=nf.projects()))
        self.assertEqual(len(projects1)+1, len(projects2))
        self._api.delete_project(tester.id)

    async def async_create_project(self, prefix="test") -> NeonProject:
        project_name = generate_random_name(prefix=prefix, length=3)
        return self._api.create_project(project_name)

    def test_get_batch(self):
        all_projects = list(self._requester.paginate(np.GET_PROJECTS(), selector="projects"))
        total = len(all_projects)
        required = 13
        new_projects = []
        project_names = []
        if total < required:
            for _ in range(required-total):
                project_names.append(generate_random_name(prefix="test_get_batch", length=4))
            new_projects = self._api.create_projects(project_names)

        total = self._requester.count(np.GET_PROJECTS(), selector="projects")
        data = self._requester.get_batch(np.GET_PROJECTS(), how_many=1, selector="projects")
        self.assertEqual(len(data), 1)
        data = self._requester.get_batch(np.GET_PROJECTS(), how_many=2, selector="projects")
        self.assertEqual(len(data), 2)
        data = self._requester.get_batch(np.GET_PROJECTS(), how_many=10, selector="projects")
        self.assertEqual(len(data), 10)
        data = self._requester.get_batch(np.GET_PROJECTS(), how_many=12, selector="projects")
        self.assertEqual(len(data), 12)
        data = self._requester.get_batch(np.GET_PROJECTS(), how_many=0, limit=100, selector="projects")
        self.assertEqual(len(data), total)

        for i in new_projects:
            self._api.delete_project(i.id)

    def test_limit(self):
        with self.assertRaises(NeonAPIException):
            self._requester.get_batch(np.GET_PROJECTS(), limit=101, selector="projects")

    def test_cursor(self):
        p = self._api.create_project(generate_random_name(prefix="test_cursor", length=3))
        cursor = self._requester.get_cursor(np.GET_PROJECTS())
        self.assertIsNotNone(cursor)
        self._api.delete_project(p.id)


if __name__ == '__main__':
    unittest.main()
