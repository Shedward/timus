import unittest
import pkg_resources
from os import path, chdir

import timus.TimusCompilers as TimusCmp 


class TestAutodetect(unittest.TestCase):
	def setUp(self):
		filename = pkg_resources.resource_filename('examples', 'example.cpp')
		file_dir = path.dirname(path.abspath(filename))
		chdir(file_dir)

	def test_autodetect_lang(self):
		self.assertEqual(TimusCmp.autodetect_lang("example.cpp"), "g++")
		self.assertEqual(TimusCmp.autodetect_lang("example.c"), "gcc")
		self.assertEqual(TimusCmp.autodetect_lang("example.pas"), "pas")
		self.assertEqual(TimusCmp.autodetect_lang("example.py"), "py3")
		self.assertEqual(TimusCmp.autodetect_lang("example.java"), "java")
		self.assertEqual(TimusCmp.autodetect_lang("example.go"), "go")
		self.assertEqual(TimusCmp.autodetect_lang("example.hs"), "ghc")
		self.assertEqual(TimusCmp.autodetect_lang("example.rb"), "rb")
		self.assertEqual(TimusCmp.autodetect_lang("example.cs"), "mono")
		self.assertEqual(TimusCmp.autodetect_lang("example.scala"), "scala")

	def test_with_dot(self):
		self.assertEqual(TimusCmp.autodetect_lang("example.py.go.cpp"), "g++")

	def test_without_ext(self):
		self.assertRaises(TimusCmp.NotSupportedExt, 
			lambda : TimusCmp.autodetect_lang("example"))

	def test_wrong_ext(self):
		self.assertRaises(TimusCmp.NotSupportedExt, 
			lambda : TimusCmp.autodetect_lang("example.txt"))

	def test_autodetect_program(self):
		self.assertTrue(isinstance(TimusCmp.autodetect_program("example.go"),
								   TimusCmp.goProgram))