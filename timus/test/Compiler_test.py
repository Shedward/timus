from unittest import TestCase

import timus.Compiler

class TestSubstitude(TestCase):
	def test_substitude(self):
		s = "{dir}/{base}.{ext}"
		filename = __file__
		substituted = timus.Compiler.substitute(s, filename)
		self.assertEqual(filename, substituted)

	def test_separated_sub(self):
		fn= "/long/dir/file.name.ext"
		sub = timus.Compiler.substitute
		self.assertEqual(sub("{dir}", fn), "/long/dir")
		self.assertEqual(sub("{base}", fn), "file.name")
		self.assertEqual(sub("{ext}", fn), "ext")



class TestCompiler(TestCase):

	def setUp(self):
		pass		