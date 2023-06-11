import unittest

from pyneoncli.configfile import NeonConfigFile
from pyneoncli.neonapi import NeonAPI
from pyneoncli.threadedcreate import ThreadedCreate
from pyneoncli.threadedneonapi import ThreadedNeonAPI

from tests.utils import generate_random_name


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self._cfg = NeonConfigFile()
        self._api = ThreadedNeonAPI(self._cfg.api_key)

    def _test_create_many(self, n=2):
        project_names = []
        for _ in range(n):
            project_names.append( generate_random_name(prefix="test_create_two", length=3))
        projects = self._api.create_projects(project_names)
        self.assertEqual(len(projects), n)
        for project in projects:
            self._api.delete_project(project.id)

    def test_create_one(self):
        self._test_create_many(1)

    def test_create_two(self):
        self._test_create_many(2)

    def test_create_three(self):
        self._test_create_many(2)

    def test_create_four(self):
        self._test_create_many(4)

    def test_create_ten(self):
        self._test_create_many(10)


if __name__ == '__main__':
    unittest.main()
