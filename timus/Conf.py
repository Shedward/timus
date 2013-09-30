
import json
from os import path
from pkg_resources import Requirement, resource_filename

class Conf(object):
	""" Config file wraper """
	def __init__(self):
		self.filename = resource_filename(Requirement.parse('timus'), 'timus.conf')
		if not path.exists(self.filename):
			self.reset()

	def reset(self):
		with open(self.filename, 'w') as conf:
			conf.write("{}")

	def write(self, name, val):
		with open(self.filename, 'r+') as conf:
			data = json.load(conf)
			data[name] = val
			conf.seek(0)
			json.dump(data, conf)

	def read(self, name):
		with open(self.filename, 'r') as conf:
			data = json.load(conf)
			return data[name]