import unittest

from timus.Conf import Conf

class TestConf(unittest.TestCase):
	def test_conf(self):
		c = Conf()
		c.write('test', 15)
		self.assertEqual(c.read('test'), 15)

	def test_dict(self):
		data = {
			'one': 1,
			'two': 2,
			'three': 3
			}
		Conf().write('data', data)
		res = Conf().read('data')
		self.assertEqual(data, res)