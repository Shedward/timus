
from os import path

from timus.TimusCompilers import autodetect_program, LANG
from timus.Logger import Log
from timus.RetCodes import RetCode
from timus.Options import parse_args, WrongParams

class CompilationError(Exception):
	pass

class SourceFileNotFound(Exception):
	pass

class TestFileNotFound(Exception):
	pass

def main(argv):
	(opts, args) = parse_args(argv)

	Log(opts.log_lvl)

	ret = RetCode.UnknownError # Unknown error

	# Action
	if len(args) == 2:
		(action, srcfile) = args

		if not path.exists(srcfile):
			raise SourceFileNotFound(srcfile)

		# Define language
		if opts.lang is None:
			prog = autodetect_program(srcfile)
		else:
			prog = LANG[opts.lang](srcfile)

		if action == "run":
			ret = prog.run(cmd=opts.cmd.split(' '))

		elif action == "compile":
			ret = prog.compile(force=opts.force)

		elif action == "test":
			testsfn = path.splitext(srcfile)[0] + ".tests"
			if opts.tests is not None:
				testsfn = opts.tests
			if path.exists(testsfn):
				if (prog.compile(force=opts.force)):
					ret = prog.test(testsfn, run_count=opts.run_count,
					                time_limit=opts.time_limit,
					                mem_limit=opts.mem_limit)
				else:
					raise CompilationError(ret)
			else:
				raise TestFileNotFound(testsfn)
		else:
			raise WrongParams("Wrong action: "+action)
	else:
		raise WrongParams("Wrong args count:",len(args))

	return ret
