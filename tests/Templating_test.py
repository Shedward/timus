import unittest

from timus import Templating

class TestTemplating(unittest.TestCase):

	def test_add_intend(self):
		sample = "\n1\n2\n3\n\n4"
		self.assertEqual(Templating._add_to_each_line(sample, '_'), "_\n_1\n_2\n_3\n_\n_4")

if __name__ == '__main__':
	unittest.main()