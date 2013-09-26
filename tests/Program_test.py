import unittest
from os import remove
from time import sleep

import pkg_resources

from timus import Program

class TestFirstModifiedLatter(unittest.TestCase):
	def setUp(self):
		self.fn1 = 'file1'
		self.fn2 = 'file2'
		open(self.fn1, 'w').close()
		sleep(0.2)
		open(self.fn2, 'w').close()

	def test_first_modified_latter(self):
		self.assertTrue(Program.first_modified_latter(self.fn2, self.fn1))

	def tearDown(self):
		remove(self.fn1)
		remove(self.fn2)


class TestFormatList(unittest.TestCase):
	def test_format_list(self):
		l = ["{two}",
			 "{one}",
			 "None",
			 "{one}.{two}"]
		res = Program.format_list(l, one='1', two='2')
		self.assertEqual(res, ["2","1","None","1.2"])

class TestTestSet(unittest.TestCase):
	def test_testset(self):
		examplefn = pkg_resources.resource_filename('examples','example.tests')
		testset = Program.TestSet(examplefn)
		self.assertEqual(testset[0][1]['in'], '2 2')
		self.assertEqual(testset[4][0], 'Bignum')
		self.assertEqual(testset[-1][1]['out'], 55)

if __name__ == '__main__':
    unittest.main()