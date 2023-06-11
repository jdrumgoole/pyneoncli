import os
import random
import string
from datetime import datetime
import unittest
from argparse import Namespace

from pyneoncli.clibranch import CLIBranch
from pyneoncli.cliproject import CLIProject
from pyneoncli.clilist import CLIList
from pyneoncli.configfile import NeonConfigFile
from pyneoncli.neon import NeonProject, NeonBranch
from pyneoncli.neonapi import NeonAPI
from pyneoncli.neonapiexceptions import NeonAPIException
from tests.utils import generate_random_name


class TestCLICommands(unittest.TestCase):

    def setUp(self):
        self._cfg = NeonConfigFile()
        self._api = NeonAPI(api_key=self._cfg.api_key)
        self._projects = []

    def tearDown(self):
        for project in self._projects:
            self._api.delete_project(project.id)

    def xtest_timing(self):
        start = datetime.utcnow()
        p = self._api.create_project(generate_random_name(prefix="test_timing", length=3))
        end = datetime.utcnow()
        print(f"\ncreate_project took: {(end - start)}")
        start = datetime.utcnow()
        self._api.delete_project(p.id)
        end = datetime.utcnow()
        print(f"delete_project took: {(end - start)}")

    def test_list_all(self):
        cl = CLIList(Namespace(apikey=self._cfg.api_key, nocolor=False, fieldfilter=None, verbose=False))
        cl.list_all()

    def test_project(self):
        project_name = generate_random_name(prefix="test_project", length=3)
        cp = CLIProject(Namespace(apikey=self._cfg.api_key, nocolor=False, fieldfilter=None, verbose=False))
        cp = cp.create_one_project(project_name)
        cl = CLIList(Namespace(apikey=self._cfg.api_key, nocolor=False, fieldfilter=None, verbose=False))
        cl.list_projects([cp.id])
        self.assertTrue(type(cp) == NeonProject)
        self.assertEqual(cp.name, project_name)
        dp = self._api.delete_project(cp.id)
        self.assertEqual( dp.id, cp.id)

    def test_delete_project(self):
        cp = CLIProject(Namespace(apikey=self._cfg.api_key, nocolor=False, fieldfilter=None, verbose=False))
        p1=cp.create_one_project(generate_random_name(prefix="test_delete_project", length=3))
        p2=cp.create_one_project(generate_random_name(prefix="test_delete_project", length=3))
        p3=cp.create_one_project(generate_random_name(prefix="test_delete_project", length=3))
        cp.delete_projects([p1.id, p2.id, p3.id], check=False)
        self.assertRaises(NeonAPIException, self._api.get_project, p1.id)
        self.assertRaises(NeonAPIException, self._api.get_project, p3.id)

    def test_branch(self):
        project_name = generate_random_name(prefix="test_branch", length=3)
        cp = CLIProject(Namespace(apikey=self._cfg.api_key, nocolor=False, fieldfilter=None, verbose=False))
        cp = cp.create_one_project(project_name)
        cb = CLIBranch(Namespace(apikey=self._cfg.api_key, nocolor=False, fieldfilter=None, verbose=False))
        branch = cb.create_one_branch(cp.id)
        self.assertTrue(type(cp) == NeonProject)
        self.assertTrue(type(branch) == NeonBranch)
        self.assertEqual(cp.name, project_name)
        self.assertEqual(branch.project_id, cp.id)
        dp = self._api.delete_project(cp.id)
        self.assertEqual(dp.id, cp.id)


if __name__ == '__main__':
    unittest.main()
