
from os import path

from timus.Conf import Conf
from timus.Exceptions import CompilationError, SourceFileNotFound, TestFileNotFound, WrongParams
from timus.Logger import Log
from timus.OnlineJudje import submit, init
from timus.Options import Options
from timus.RetCodes import RetCode
from timus.TimusCompilers import TimusProgram, show_lang_list


def main(argv):
	opts = Options(argv)

	Log(opts.opt.log_lvl)

	ret = RetCode.UnknownError

	# Do action
	if opts.action == 'list':
		show_lang_list()

	elif opts.action == 'init':
		opts.need_args('problem')
		opts.need_opts('id')
		init(opts.opt.problem, opts.opt.id, opts.opt.lang)

	elif opts.action == 'setdef':
		opts.save_as_grobal()

	elif opts.action == 'reset':
		Conf().reset()

	else:
		opts.need_args('filename')

		# Check sourcefile existance and type
		if not path.exists(opts.opt.filename):
			raise SourceFileNotFound(opts.opt.filename)

		# Detect language if not defined
		prog = TimusProgram(opts.opt.filename, opts.opt.lang)
		opts.opt.lang = prog.lang # :C

		if opts.action == "run":
			ret = prog.run(cmd=opts.opt.cmd.split(' '))

		elif opts.action == "build":
			ret = prog.compile(force=True)

		elif opts.action == "test":
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

		elif opts.action == "submit":
			opts.need_opts('id', 'problem')
			submit(opts.opt.id, opts.opt.problem, opts.opt.filename, opts.opt.lang)

		else:
			raise WrongParams("Wrong action: '{0}".format(opts.opt.action))

	return ret
