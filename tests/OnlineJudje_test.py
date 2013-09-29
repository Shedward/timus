import unittest
import pkg_resources
from os import chdir, path

from timus import OnlineJudje

class TestOnlineJudje(unittest.TestCase):
	def setUp(self):
		filename = pkg_resources.resource_filename('examples', 'example.py')
		file_dir = path.dirname(path.abspath(filename))
		chdir(file_dir)

	def test_get_name(self):
		self.assertEqual(OnlineJudje.get_name('86286AA'), "Shed")

	def test_result_table(self):
		self.assertEqual(len(OnlineJudje.result_table('86286AA')[0]), 9) # In table shoud be 9 cols.

	def test_send(self):
		r = OnlineJudje.send('86286AA', '1000', 'example.c', 'gcc')
		self.assertTrue(r.url.find('status.aspx') != -1)

	def test_get_problem_data(self):
		data = OnlineJudje.get_problem_data('1000')
		self.assertEqual(data['problem_id'], '1000')
		self.assertEqual(data['problem_desc'], 'A+B Problem')
		self.assertEqual(data['test_input'], '1 5')
		self.assertEqual(data['test_output'], '6')

	def test_init(self):
		OnlineJudje.init('1000', '86286AA', 'scala')

if __name__ == '__main__':
    unittest.main()
