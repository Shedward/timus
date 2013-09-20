import unittest
import pkg_resources

from timus import Timus
from timus.RetCodes import RetCode

class TestTimus(unittest.TestCase):
	def test_timus(self):
		fn = pkg_resources.resource_filename('examples','example.cpp')
		self.assertEqual(Timus.main(['test', fn, '-f']), RetCode.WrongOutput)

	def test_timus_wrong_params(self):
		self.assertRaises(Timus.WrongParams, 
						  lambda : Timus.main([""]))
		self.assertRaises(Timus.SourceFileNotFound, 
				  		  lambda : Timus.main(["test", "no_file"]))