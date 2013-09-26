
from os import path

from timus.Exceptions import CompilationError, SourceFileNotFound, TestFileNotFound, WrongParams
from timus.Logger import Log
from timus.OnlineJudje import submit
from timus.Options import parse_args
from timus.RetCodes import RetCode
from timus.TimusCompilers import autodetect_program, LANG


def main(argv):
	opts = parse_args(argv)

	Log(opts.log_lvl)

	ret = RetCode.UnknownError

	# Check sourcefile existance and type
	if not path.exists(opts.filename):
		raise SourceFileNotFound(opts.filename)

	# Detect language if not defined
	if opts.lang is None:
		prog = autodetect_program(opts.filename)
		opts.lang = prog.lang # :C
	else:
		prog = LANG[opts.lang](opts.filename)

	# Do action
	if opts.action == "run":
		ret = prog.run(cmd=opts.cmd.split(' '))

	elif opts.action == "compile":
		ret = prog.compile(force=opts.force)

	elif opts.action == "test":
		if path.exists(opts.tests):
			if (prog.compile(force=opts.force)):
				ret = prog.test(opts.tests, run_count=opts.run_count,
				                time_limit=opts.time_limit,
				                mem_limit=opts.mem_limit)
			else:
				raise CompilationError(ret)
		else:
			raise TestFileNotFound(opts.tests)

	elif opts.action == "submit":
		submit(opts.id, opts.problem, opts.filename, opts.lang)
	else:
		raise WrongParams("Wrong action: '{0}".format(opts.action))

	return ret
