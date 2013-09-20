from subprocess import PIPE, STDOUT

import psutil
import threading
from time import sleep

SLEEP = 0.2

class TimeLimitExceeded(Exception):
	"""Rises when observed process exceed said time limit"""
	pass


class MemoryLimitExceeded(Exception):
	"""Rises when observed process exceed said memory limit"""
	pass


class ObservedCmd(object):
	"""Limited external process"""

	def __init__(self, cmd):
		self.cmd = cmd
		self.process = None

	def run(self, inp=None, time_limit=None, mem_limit=None,
			stdin=PIPE, stdout=PIPE, stderr=STDOUT):
		self.max_rss = 0
		self.time = 0

		self.process = psutil.Popen(self.cmd, stdin=stdin, stdout=stdout,
									stderr=stderr)

		def do():
			sleep(SLEEP)
			self.output = self.process.communicate(input=inp)

		thread = threading.Thread(target=do)

		thread.start()
		while self.process.is_running():
			try:
				mem = self.process.get_memory_info().rss
				self.time = self.process.get_cpu_times().user

				if mem > self.max_rss:
					self.max_rss = mem

				if mem_limit is not None and mem > mem_limit:
					self.process.terminate()
					raise MemoryLimitExceeded()

				if time_limit is not None and self.time - SLEEP > time_limit:
					self.process.terminate()
					raise TimeLimitExceeded

			except psutil.NoSuchProcess:
				break
		thread.join()
