import unittest
from pyneoncli.printer import dict_filter, flatten
from pyneoncli.neonliterals import NeonAPIPaths, NeonFunction as nf


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


class TestDict(unittest.TestCase):
    def test_dict_walk(self):
        data = {
            'person': {
                'name': 'John Doe',
                'age': 30,
                'address': {
                    'street': '123 Main St',
                    'city': 'New York',
                    'country': 'USA'
                }
            }
        }
        for k,v in flatten(data):
            print(f"{k} : {v}")

    def test_dict_filter(self):
        x = { "a": 1, 
             "b": 2, 
             "c": 3 }
        f = dict_filter(x, ["a", "b"])
        # f = dict_filter(d, ["branch_id"])
        # print(f)
        x = { "a": 1,
              "b": 2,
              "c": {"d": 3,
                    "e": 4,
                    "f": 5 }}
        f = dict_filter(x, ["a", "b", "c.d"])
        print(f)

    def test_literals(self):
        self.assertTrue("project_id" in NeonAPIPaths.GET_BRANCHES.value)
        s = NeonAPIPaths.GET_BRANCHES(project_id="1234")
        self.assertEqual(s, "https://console.neon.tech/api/v2/projects/1234/branches")
        s = NeonAPIPaths.GET_BRANCH( project_id="1234", branch_id="5678")
        self.assertEqual(s, "https://console.neon.tech/api/v2/projects/1234/branches/5678")
        s = NeonAPIPaths.GET_PROJECTS()
        self.assertEqual(s, "https://console.neon.tech/api/v2/projects")

        x = nf.project()
        self.assertEqual(x, "project")


if __name__ == '__main__':
    unittest.main()