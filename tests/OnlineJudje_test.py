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

if __name__ == '__main__':
    unittest.main()