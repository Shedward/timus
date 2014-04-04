
from optparse import OptionParser, Values
from os import path

from timus.Conf import Conf
from timus.Exceptions import WrongParams
from timus.Logger import Log

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
    cmdopts = {}
    defopts = {}
    fileopts = {}
    opts = {}
    action = None

    def _init_parser(self):
        HELP_MESSAGE = """
            timus [OPTIONS] <action> <filename>
            Use one of the action:
                run     - Run program using by default pattern "$TERM -e {bin}"
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
            help="Specify pattern for 'run' action.")

        self.parser.add_option("-f", "--force", action="store_true",
            dest="force", help="Force recompile.")

        self.parser.add_option("--ll","--log-lvl", action="store",
            dest="log_lvl",
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
            dest="run_count", type="int"
            )

        self.parser.add_option("-l", "--lang", action="store",
            help="Specify compiler/language dialect.",
            dest="lang")

        self.parser.add_option('-i', "--id", action="store",
            help="Specify JudjeID.", dest="id")

        self.parser.add_option('-p', "--problem", action="store",
            help="Problem num.", dest="problem")

        self.parser.add_option('-d', "--diff", action="store_true",
            help="Show diff between expected and recived for failed tests.",
            dest="diff_out")

    def __init__(self, argv):
        # Append user defined.
        self.defopts = Conf().read('defopts')

        self._init_parser()
        (opts, args) = self.parser.parse_args(argv)

        self.cmdopts = vars(opts)

        self._update()

        # Define action
        if len(args) > 0:
            self.action = args[0]
            self.args = args[1:]
        else:
            raise WrongParams("Action not defined.")

        # Parce special options
        if 'mem_limit' in self.opts and isinstance(self.opts['mem_limit'], str):
            self.opts['mem_limit'] = _str2bytes(self.opts['mem_limit'])

        if 'log_lvl' in self.opts and isinstance(self.opts['log_lvl'], str):
                LOG_LVL_OPTS = {
                    "err": Log.Err,
                    "msg": Log.Msg,
                    "vrb": Log.Vrb
                    }
                if self.opts['log_lvl'] in LOG_LVL_OPTS:
                    self.opts['log_lvl']  = LOG_LVL_OPTS[self.opts['log_lvl']]
                else:
                    raise WrongParams("Wrong log level: {0}.".format(self.opts['log_lvl']))

    def __call__(self, name):
        if name not in self.opts:
            self._try_define(name)
        return self.opts[name]

    def _update(self):
        def upd(d1, d2):
            """ Apply d2 to d1, rewrite if elem of dic2 is not None """
            for k, v in d2.items():
                if v is not None:
                    d1[k] = v

        self.opts = {}
        upd(self.opts, self.defopts)
        upd(self.opts, self.fileopts)
        upd(self.opts, self.cmdopts)

    def update_file_opts(self, dic):
        # Infile opts must overwrite def opts
        # but be overwriten by command line opts
        self.fileopts.update(dic)
        self._update()


    def need_args(self, *arg_names):
        if len(self.args) < len(arg_names):
            raise WrongParams("Not enough args.")
        elif len(self.args) > len(arg_names):
            raise WrongParams("Too much args.")
        else:
            for name, val in zip(arg_names, self.args):
                self.cmdopts[name] = val
            self._update()          

    def _try_define(self, name):
        DEFS = {
            'cmd': '{bin}',
            'log_lvl': Log.Msg,
            'run_count': 1,
            'force': False,
            'lang': None,
            'time_limit': None,
            'mem_limit': None,
            'diff_out': False
        }
        if name == 'tests':
            self.need_args('filename')
            self.opts['tests'] = path.splitext(self.opts['filename'])[0] + ".tests"
        elif name in DEFS:
            self.opts[name] = DEFS[name]
        else:
            raise WrongParams("Option '{0}' is not defined.".format(name))

    def save_as_grobal(self):
        Conf().write('defopts', self.opts)