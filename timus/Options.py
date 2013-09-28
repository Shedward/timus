
from optparse import OptionParser
from os import path

from timus.Exceptions import WrongParams
from timus.Logger import Log
from timus.TimusCompilers import DESC

def _str2bytes(val):
	p = val[-1].upper()
	m = float(val[0:-1])
	if p == 'G':
		res = m * 1024 ** 2
	elif p == 'M':
		res = m * 1024
	elif p == 'K':
		res = m
	elif p.isdigit() or p == '.':
		try:
			res = float(val)
		except ValueError:
			raise WrongParams("Wrong mem limit: {0}.".format(val))
	else:
		raise WrongParams("Wrong mem limit: {0}.".format(val))

	res = int(round(res * 1024))  # to bytes
	return res

class Options:
	opt = None

	def _init_parser(self):
		HELP_MESSAGE = """
			timus [OPTIONS] <action> <filename>
			Use one of the action:
			    run	    - Run program using by default pattern "$TERM -e {bin}"
			              where {bin} is name of executable file.
			              Use -c to change patern.
			    build - Compile source file. With interpret languages do nothing.
			              Use -f to force recompile.
			    test    - Test program. Searching for <source>.tests by default.
			              Use -t to specify tests file.
			    list    - Show list of all languages for -l option.
			    submit  - Send solution to acm.timus.ru server. Need defined -i and -p opts.
		"""

		self.parser = OptionParser(usage=HELP_MESSAGE)

		self.parser.add_option("-t", "--tests", action="store",
			type="string", dest="tests",
			help="Specify tests filename. By default "
			"searching for <source_file>.tests.")

		self.parser.add_option("-r", "--run", action="store",
			type="string", dest="cmd",
			help="Specify pattern for 'run' action.",
			default="$TERM -e {bin}")

		self.parser.add_option("-f", "--force", action="store_true",
			dest="force", help="Force recompile.")

		self.parser.add_option("--ll","--log-lvl", action="store",
			dest="log_lvl", default="msg",
			help="Set logging level:\n err - show "
			"only error messages,\n msg - show "
			"basic messages (default),\n"
			" vrb - show every execute command.")

		self.parser.add_option("--tl","--time-limit", action="store",
			help="Specify time limit in seconds. "
			"If program running longer "
			"it will be terminated with "
			"'Time limit exceeded' error. "
			"Using in test action.",
			dest="time_limit", type="float")

		self.parser.add_option("--ml","--mem-limit", action="store",
			help="Specify maximum memory usage in kbytes"
			"also you can use notation like 1K, 5.5M, "
			"0.1g. If program exceed the limit "
			"it will be terminated with "
			"'Memory limit exceeded' error. "
			"Using in test action.",
			dest="mem_limit", type="string")

		self.parser.add_option("-c", "--run-count", action="store",
			help="Specify amount of runing. "
			"More runs, more accurate "
			"the measurements.",
			dest="run_count", type="int",
			default=1
			)

		self.parser.add_option("-l", "--lang", action="store",
			help="Specify compiler/language dialect.",
			dest="lang")

		self.parser.add_option('-i', "--id", action="store",
			help="Specify JudjeID.", dest="id")

		self.parser.add_option('-p', "--problem", action="store",
			help="Problem num.", dest="problem")

	def __init__(self, argv):
		self._init_parser()
		(self.opt, self.args) = self.parser.parse_args(argv)

		# Define action
		if len(self.args) > 0:
			setattr(self.opt, 'action', self.args[0])
			self.args = self.args[1:]
		else:
			raise WrongParams("Action not defined.")

		# Parce special options
		if self.opt.mem_limit is not None:
			self.opt.mem_limit = _str2bytes(self.opt.mem_limit)

		if self.opt.log_lvl is not None:
				LOG_LVL_OPTS = {
					"err": Log.Err,
					"msg": Log.Msg,
					"vrb": Log.Vrb
					}
				if self.opt.log_lvl in LOG_LVL_OPTS:
					self.opt.log_lvl  = LOG_LVL_OPTS[self.opt.log_lvl]
				else:
					raise WrongParams("Wrong log level: {0}.".format(self.opt.log_lvl))

	def need_args(self, *arg_names):
		if len(self.args) < len(arg_names):
			raise WrongParams("Not enough args.")
		elif len(self.args) > len(arg_names):
			raise WrongParams("Too much args.")
		else:
			for name, val in zip(arg_names, self.args):
				setattr(self.opt, name, val)

	def need_opts(self, *opts_names):
		for name in opts_names:
			if not hasattr(self.opt, name):
				raise Exception("Option '{0}' is not exist.".format(name))

			if getattr(self.opt, name) is None:
				self._try_define(name)

	def _try_define(self, name):
		if name == 'tests' and self.opt.tests is None:
			self.need_args('filename')
			self.opt.tests = path.splitext(self.opt.filename)[0] + ".tests"
		else:
			raise WrongParams("Option '{0}' is not defined.".format(name))

def show_lang_list():
	LANGS_LIST = '\n\t'.join([lang + " - " + desc for lang, desc in DESC.items()])
	MSG = """
		List of compilers/interpreters for -l option:

	""" + LANGS_LIST
	print(MSG)