
from os import path
from subprocess import call

from timus.Logger import Log


def substitute(str, filename):
    """ Replace {base}, {ext}, {dir}, {file} to basename, extension, dir 
        and filename of file """
    (base, ext) = path.splitext(path.basename(filename))
    if ext != '':
        ext = ext[1:] # remove dot
    cur_dir = path.dirname(filename)
    return str.format(base=base, ext=ext, dir=cur_dir, file=filename)


class Compiler(object):
    """ Define how to compile file """
    def __init__(self, cmd, bin_fn):
        super(Compiler, self).__init__()
        self.cmd = cmd
        self.bin_fn = path.abspath(bin_fn)
        self.args = ""

    def compile(self, filename):
        """ Compile file. Result filename can be obitain by bin_file_name() """
        args = self.cmd + " " + self.args
        args = substitute(args, filename)
        LOG = Log()
        LOG(Log.Vrb, "\trun", args)
        return call(args, shell=True)

    def add_args(self, args):
        self.args += " " + args

    def bin_file_name(self, src_filename):
        return substitute(self.bin_fn, path.abspath(src_filename))
