import os
import random
import string
import unittest

from pyneoncli.clicommands import CLIProject

def generate_random_name(length):
    characters = string.ascii_letters + string.digits + '_'
    return ''.join(random.choice(characters) for _ in range(length))

class TestCLICommands(unittest.TestCase):

    def test_project(self):
        pass
        # project_name  = generate_random_name(10)
        # apikey = os.getenv("NEON_API_KEY")
        # self.assertTrue(apikey)
        # project = CLIProject(args=["--apikey", apikey, ])
        # p = project.create_project(project_name=project_name)
        # self.assertTrue(type(p) == dict)
        # self.assertEqual(p["name"], project_name)
        # ids = project.delete_project([p[id]])
        # self.assertTrue( id in ids)

if __name__ == '__main__':
    unittest.main()
