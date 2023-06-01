import unittest
from pyneoncli.printer import Printer


class TestPrinter(unittest.TestCase):

    def setUp(self) -> None:
        self._p = Printer()

    def test_parse(self):
        s = self._p.name_id({'name': 'foo', 'id': 'bar'}, name_label="name: ", id_label="id: ")
        n, i = self._p.parse_name_id(s)
        self.assertEqual(n, 'foo')
        self.assertEqual(i, 'bar')

        s = self._p.name_id({'name': 'foo', 'id': 'bar'}, name_label="Project name: ", id_label="Project id: ")
        n, i = self._p.parse_name_id(s)
        self.assertEqual(n, 'foo')
        self.assertEqual(i, 'bar')

    def test_multiline_parse(self):
        s = self._p.name_id_list([{'name': 'foo', 'id': 'bar'}, {'name': 'baz', 'id': 'qux'}],
                                 name_label="name: ", id_label="id: ")
        l = self._p.parse_name_id_list(s)
        self.assertTrue(("foo", "bar") in l)
        self.assertTrue(("baz", "qux") in l)

        s = self._p.name_id_list([{'name': 'foo', 'id': 'bar'}, {'name': 'baz', 'id': 'qux'}],
                                 name_label="Project name: ", id_label="Project id: ")
        l = self._p.parse_name_id_list(s)
        self.assertTrue(("foo", "bar") in l)
        self.assertTrue(("baz", "qux") in l)


if __name__ == '__main__':
    unittest.main()
