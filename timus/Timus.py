
from os import path

from timus.Exceptions import CompilationError, SourceFileNotFound, TestFileNotFound, WrongParams
from timus.Logger import Log
from timus.OnlineJudje import submit
from timus.Options import parse_args, need, show_lang_list
from timus.RetCodes import RetCode
from timus.TimusCompilers import TimusProgram


def main(argv):
	opts = parse_args(argv)

	Log(opts.log_lvl)

	ret = RetCode.UnknownError

	# Check sourcefile existance and type
	if not path.exists(opts.filename):
		raise SourceFileNotFound(opts.filename)

	# Detect language if not defined
	prog = TimusProgram(opts.filename, opts.lang)
	opts.lang = prog.lang # :C

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
		need(opts.id, 'JudjeID')
		need(opts.problem, 'problem')
		submit(opts.id, opts.problem, opts.filename, opts.lang)
	
	elif opts.action == "list":
		show_lang_list()

	else:
		raise WrongParams("Wrong action: '{0}".format(opts.action))

	return ret
