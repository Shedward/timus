
from optparse import OptionParser
from os import path

from timus.Exceptions import WrongParams
from timus.Logger import Log
from timus.TimusCompilers import DESC

HELP_MESSAGE = """
	timus [OPTIONS] <action> <filename>
	Use one of the action:
	    run	    - Run program using by default pattern "$TERM -e {bin}"
	              where {bin} is name of executable file.
	              Use -c to change patern.
	    compile - Compile source file. With interpret languages do nothing.
	              Use -f to force recompile.
	    test    - Test program. Searching for <source>.tests by default.
	              Use -t to specify tests file.
"""

def parser():
	parser = OptionParser(usage=HELP_MESSAGE)

	parser.add_option("-t", "--tests", action="store",
		type="string", dest="tests",
		help="Specify tests filename. By default "
		"searching for <source_file>.tests.")

	parser.add_option("-r", "--run", action="store",
		type="string", dest="cmd",
		help="Specify pattern for 'run' action.",
		default="$TERM -e {bin}")

	parser.add_option("-f", "--force", action="store_true",
		dest="force", help="Force recompile.")

	parser.add_option("--ll","--log-lvl", action="store",
		dest="log_lvl", default="msg",
		help="Set logging level:\n err - show "
		"only error messages,\n msg - show "
		"basic messages (default),\n"
		" vrb - show every execute command.")

	parser.add_option("--tl","--time-limit", action="store",
		help="Specify time limit in seconds. "
		"If program running longer "
		"it will be terminated with "
		"'Time limit exceeded' error. "
		"Using in test action.",
		dest="time_limit", type="float")

	parser.add_option("--ml","--mem-limit", action="store",
		help="Specify maximum memory usage in kbytes"
		"also you can use notation like 1K, 5.5M, "
		"0.1g. If program exceed the limit "
		"it will be terminated with "
		"'Memory limit exceeded' error. "
		"Using in test action.",
		dest="mem_limit", type="string")

	parser.add_option("-c", "--run-count", action="store",
		help="Specify amount of runing. "
		"More runs, more accurate "
		"the measurements.",
		dest="run_count", type="int",
		default=1
		)

	parser.add_option("-l", "--lang", action="store",
		help="Specify compiler/language dialect.",
		dest="lang")

	parser.add_option('-i', "--id", action="store",
		help="Specify JudjeID.", dest="id")

	parser.add_option('-p', "--problem", action="store",
		help="Problem num.", dest="problem")

	return parser

def str2bytes(val):
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

def parse_args(argv):
	(opts, args) = parser().parse_args(argv)

	# Convers special params to sutable type
	if opts.mem_limit is not None:
		opts.mem_limit = str2bytes(opts.mem_limit)

	if opts.log_lvl is not None:
			LOG_LVL_OPTS = {
				"err": Log.Err,
				"msg": Log.Msg,
				"vrb": Log.Vrb
				}
			if opts.log_lvl in LOG_LVL_OPTS:
				opts.log_lvl  = LOG_LVL_OPTS[opts.log_lvl]
			else:
				raise WrongParams("Wrong log level: {0}.".format(opts.log_lvl))

	# Check arguments
	if len(args) == 0:
		raise WrongParams("Action not defined.")
	if len(args) > 0:
		setattr(opts, 'action', args[0])

	if len(args) == 2:
		setattr(opts, 'filename', args[1])
	elif opts.action == 'list':
		pass
	else:
		raise WrongParams("Too much args.")

	# Define undefined opts with standard values
	testsfn = path.splitext(opts.filename)[0] + ".tests"
	if opts.tests is None:
		opts.tests = testsfn

	return opts

def show_lang_list():
	LANGS_LIST = '\n\t'.join([lang + " - " + desc for lang, desc in DESC.items()])
	MSG = """
		List of compilers/interpreters for -l option:

	""" + LANGS_LIST
	print(MSG)


def need(var, name):
	if var is None:
		raise WrongParams(name, 'not defined.')