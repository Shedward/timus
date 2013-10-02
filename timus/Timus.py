
from os import path

from timus.Conf import Conf
from timus.Exceptions import CompilationError, SourceFileNotFound, TestFileNotFound, WrongParams
from timus.Logger import Log
from timus.OnlineJudje import submit, init
from timus.Options import Options
from timus.RetCodes import RetCode
from timus.Templating import extract
from timus.TimusCompilers import TimusProgram, show_lang_list


def main(argv):
    opts = Options(argv)

    Log(opts('log_lvl'))

    ret = RetCode.UnknownError

    # Do action
    if opts.action == 'list':
        show_lang_list()

    elif opts.action == 'init':
        opts.need_args('problem')
        init(opts('problem'), opts('id'), opts('lang'))

    elif opts.action == 'setdef':
        opts.save_as_grobal()

    elif opts.action == 'reset':
        Conf().reset()

    else:
        opts.need_args('filename')

        # Check sourcefile existance and type
        if not path.exists(opts('filename')):
            raise SourceFileNotFound(opts('filename'))

        # Get opts stored in sourcefile.
        opts.update_file_opts(extract(opts('filename')))

        # Detect language if not defined
        prog = TimusProgram(opts('filename'), opts('lang'))
        opts.update_file_opts({'lang': prog.lang})

        # Do program's action.
        if opts.action == "run":
            ret = prog.run(cmd=opts('cmd').split(' '))

        elif opts.action == "build":
            ret = prog.compile(force=True)

        elif opts.action == "test":
            if path.exists(opts('tests')):
                if (prog.compile(force=opts('force'))):
                    ret = prog.test(opts('tests'), run_count=opts('run_count'),
                                    time_limit=opts('time_limit'),
                                    mem_limit=opts('mem_limit'))
                else:
                    raise CompilationError(ret)
            else:
                raise TestFileNotFound(opts('tests'))

        elif opts.action == "submit":
            submit(opts('id'), opts('problem'), opts('filename'), opts('lang'))

        else:
            raise WrongParams("Wrong action: '{0}".format(opts('action')))

    return ret
