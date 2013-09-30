
import json
from os import path, makedirs

from appdirs import user_data_dir

class Conf(object):
	""" Config file wraper """
	def __init__(self):
		self.filename = path.join(user_data_dir("timus","shed"), 'timus.conf')
		if not path.exists(self.filename):
			self.reset()

	def reset(self):
		conf_dir = path.dirname(self.filename)
		if not path.exists(conf_dir):
			makedirs(conf_dir)
		with open(self.filename, 'w') as conf:
			conf.write('{"defopts": {}}')

	def write(self, name, val):
		with open(self.filename, 'r+') as conf:
			data = json.load(conf)
			data[name] = val
			conf.seek(0)
			json.dump(data, conf, sort_keys=True,
				indent=4, separators=(',', ': '))

	def read(self, name):
		with open(self.filename, 'r') as conf:
			data = json.load(conf)
			return data[name]