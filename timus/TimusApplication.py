
from optparse import OptionParser
from os import path

from timus.Program import TestSet
from timus.TimusCompilers import autodetect_program, LANG
from timus.Logger import Log

HELP_MESSAGE = """
timus [OPTIONS] <action> <filename>
Use one of the action:
    run	    - Run program using by default pattern "konsole --hold -e {bin}"
              where {bin} is name of executable file.
              Use -c to change patern.
    compile - Compile source file. With interpret languages do nothing.
              Use -f to force recompile.
    test    - Test program. Searching for <source>.tests by default.
              Use -t to specify tests file.

List of compilers/interpreters for -l option:
    cl    - Visual C 2010
    cl++  - Visual C 2010
    gcc   - GCC 4.7.2
    gcc11 - GCC 4.7.2 with C11
    g++   - G++ 4.7.2
    g++11 - G++ 4.7.2 with C++11
    pas   - FreePascal 2.4.0
    ghc   - Haskell 7.6.1
    go    - Go 1.7
    c#    - Visual C#
    mono  - Mono 3.0.7
    java  - Java 1.7
    py2   - Python 2.7
    py3   - Python 3.3
    rb    - Ruby 1.9.3

"""

class SourceFileNotFound(Exception):
	pass

class TestFileNotFound(Exception):
	pass

class WrongMemLimit(Exception):
	pass

class WrongParams(Exception):
	pass

def main(argv):
	# Init option parser
	parser = OptionParser(usage=HELP_MESSAGE)

	parser.add_option("-t", "--tests", action="store",
		type="string", dest="tests",
		help="Specify tests filename. By default "
		"searching for <source_file>.tests.")

	parser.add_option("-r", "--run", action="store",
		type="string", dest="cmd",
		help="Specify pattern for 'run' action",
		default="konsole --hold -e {bin}")

	parser.add_option("-f", "--force", action="store_true",
		dest="force", help="Force recompile.")

	parser.add_option("--ll","--log-lvl", action="store",
		dest="log_lvl", default="msg",
		help="Set logging level:\n err - show "
		"only error messages,\n msg - show "
		"basic messages (default),\n"
		" vrb - show every execute command")

	parser.add_option("--tl","--time-limit", action="store",
		help="Specify time limit in seconds. "
		"If program running longer "
		"it will be terminated with "
		"'Time limit exceeded' error. "
		"Using in test action",
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
		"More runs, the more accurate "
		"the measurements",
		dest="run_count", type="int",
		default=1
		)

	parser.add_option("-l", "--lang", action="store",
		help="Specify compiler/language dialect.",
		dest="lang")

	(opts, args) = parser.parse_args()

	# Convert mem limit to KB if needed.
	if opts.mem_limit is not None:
		p = opts.mem_limit[-1].upper()
		m = float(opts.mem_limit[0:-1])
		if p == 'G':
			opts.mem_limit = m * 1024 ** 2
		elif p == 'M':
			opts.mem_limit = m * 1024
		elif p == 'K':
			opts.mem_limit = m
		elif p.isdigit():
			opts.mem_limit = float(opts.mem_limit)
		else:
			raise WrongMemLimit(opts.mem_limit)

		opts.mem_limit = int(round(opts.mem_limit * 1024))  # to bytes

	# Init logger
	LOG_LVL_OPTS = {
	"err": Log.Err,
	"msg": Log.Msg,
	"vrb": Log.Vrb
	}
	Log(LOG_LVL_OPTS[opts.log_lvl])

	# Action
	if len(args) == 2:
		(action, srcfile) = args

		if not path.exists(srcfile):
			raise SourceFileNotFound(format(srcfile))

		# Define language
		if opts.lang is None:
			prog = autodetect_program(srcfile)
		else:
			prog = LANG[opts.lang](srcfile)

		if action == "run":
			prog.run(cmd=opts.cmd.split(' '))

		elif action == "compile":
			prog.compile(force=opts.force)

		elif action == "test":
			testsfn = path.splitext(srcfile)[0] + ".tests"
			if opts.tests is not None:
				testsfn = opts.tests
				if path.exists(testsfn):
					tests = TestSet(testsfn)
					prog.compile(force=opts.force)
					prog.test(tests, run_count=opts.run_count,
							  time_limit=opts.time_limit,
							  mem_limit=opts.mem_limit)
				else:
					raise TestFileNotFound(testsfn)
		else:
			raise WrongParams("Wrong action: "+action)
	else:
		raise WrongParams("Wrong args count.")
