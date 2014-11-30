import unittest
import pkg_resources
from os import chdir, path, getcwd, remove

from timus import OnlineJudje


class TestOnlineJudje(unittest.TestCase):
    def setUp(self):
        filename = pkg_resources.resource_filename('examples', 'example.py')
        file_dir = path.dirname(path.abspath(filename))
        self.defdir = getcwd()
        chdir(file_dir)

    def test_get_name(self):
        self.assertEqual(OnlineJudje.get_name('86286AA'), "Shed")

    def test_result_table(self):
        # In table shoud be 9 cols.
        self.assertEqual(len(OnlineJudje.result_table('86286AA')[0]), 9)

    def test_send(self):
        r = OnlineJudje.send('86286AA', '1000', 'example.c', 'gcc')
        print(r)
        print(r.url)
        self.assertTrue(r.url.find('status.aspx') != -1)

    def test_get_problem_data(self):
        data = OnlineJudje.get_problem_data('1201')
        self.assertEqual(data['problem_id'], '1201')
        self.assertEqual(data['problem_desc'], 'Which Day Is It?')
        tests = list(data['tests'])
        self.assertEqual(tests[0][0], '16 3 2002\r\n')
        self.assertEqual(tests[1][0], '1 3 2002\r\n')

    def test_init(self):
        OnlineJudje.init('1000', '86286AA', 'scala')
        self.assertTrue(path.exists('1000.A+B_Problem.scala'))
        self.assertTrue(path.exists('1000.A+B_Problem.tests'))
        remove('1000.A+B_Problem.scala')
        remove('1000.A+B_Problem.tests')

    def tearDown(self):
        chdir(self.defdir)

if __name__ == '__main__':
    unittest.main()
