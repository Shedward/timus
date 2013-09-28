
from os import path

from timus.Exceptions import CompilationError, SourceFileNotFound, TestFileNotFound, WrongParams
from timus.Logger import Log
from timus.OnlineJudje import submit
from timus.Options import Options, show_lang_list
from timus.RetCodes import RetCode
from timus.TimusCompilers import TimusProgram


def main(argv):
	opts = Options(argv)

	Log(opts.opt.log_lvl)

	ret = RetCode.UnknownError

	# Do action
	if opts.opt.action == 'list':
		show_lang_list()
	else:
		opts.need_args('filename')

		# Check sourcefile existance and type
		if not path.exists(opts.opt.filename):
			raise SourceFileNotFound(opts.opt.filename)

		# Detect language if not defined
		prog = TimusProgram(opts.opt.filename, opts.opt.lang)
		opts.opt.lang = prog.lang # :C

		if opts.opt.action == "run":
			ret = prog.run(cmd=opts.opt.cmd.split(' '))

		elif opts.opt.action == "build":
			ret = prog.compile(force=True)

		elif opts.opt.action == "test":
			opts.need_opts('tests')
			if path.exists(opts.opt.tests):
				if (prog.compile(force=opts.opt.force)):
					ret = prog.test(opts.opt.tests, run_count=opts.opt.run_count,
					                time_limit=opts.opt.time_limit,
					                mem_limit=opts.opt.mem_limit)
				else:
					raise CompilationError(ret)
			else:
				raise TestFileNotFound(opts.opt.tests)

		elif opts.opt.action == "submit":
			opts.need(['filename'], 'id', 'problem')
			submit(opts.opt.id, opts.opt.problem, opts.opt.filename, opts.opt.lang)

		else:
			raise WrongParams("Wrong action: '{0}".format(opts.opt.action))

	return ret
