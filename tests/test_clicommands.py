import os
import random
import string
import unittest
from argparse import Namespace

from pyneoncli.clicommands import CLIProject, CLIBranch
from pyneoncli.neon import NeonProject, NeonBranch
from pyneoncli.neonapi import NeonAPI, NeonAPIException


def generate_random_name(length):
    characters = string.ascii_letters + string.digits + '_'
    return ''.join(random.choice(characters) for _ in range(length))

class TestCLICommands(unittest.TestCase):

    def setUp(self):
        self._apikey = os.getenv("NEON_API_KEY")
        self._api = NeonAPI(api_key=self._apikey)

    def test_namespace(self):
        apikey = os.getenv("NEON_API_KEY")
        self.assertTrue(apikey)
        ns = Namespace(apikey=apikey)
        self.assertTrue(ns.apikey == apikey)

    def test_project(self):
        project_name = generate_random_name(10)
        self.assertTrue(self._apikey)
        cp = CLIProject(Namespace(apikey=self._apikey, nocolor=False, fieldfilter=None, verbose=False))
        cp = cp.create_one_project(project_name)
        self.assertTrue(type(cp) == NeonProject)
        self.assertEqual(cp.name, project_name)
        dp = self._api.delete_project(cp.id)
        self.assertEqual( dp.id, cp.id)

    def test_delete_project(self):
        cp = CLIProject(Namespace(apikey=self._apikey, nocolor=False, fieldfilter=None, verbose=False))
        p1=cp.create_one_project(generate_random_name(10))
        p2=cp.create_one_project(generate_random_name(10))
        p3=cp.create_one_project(generate_random_name(10))
        cp.delete_projects([p1.id, p2.id, p3.id], check=False)
        self.assertRaises(NeonAPIException, self._api.get_project_by_id, p1.id)
        self.assertRaises(NeonAPIException, self._api.get_project_by_id, p3.id)

    def test_branch(self):
        project_name = generate_random_name(10)
        apikey = os.getenv("NEON_API_KEY")
        self.assertTrue(apikey)
        cp = CLIProject(Namespace(apikey=apikey, nocolor=False, fieldfilter=None, verbose=False))
        cp = cp.create_one_project(project_name)
        cb = CLIBranch(Namespace(apikey=apikey, nocolor=False, fieldfilter=None, verbose=False))
        branch = cb.create_one_branch(cp.id)
        self.assertTrue(type(cp) == NeonProject)
        self.assertTrue(type(branch) == NeonBranch)
        self.assertEqual(cp.name, project_name)
        self.assertEqual(branch.project_id, cp.project_id)
        dp = self._api.delete_project(cp.id)
        self.assertEqual(dp.id, cp.id)

if __name__ == '__main__':
    unittest.main()
