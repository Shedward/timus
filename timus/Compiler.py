
from os import path
from subprocess import call

from timus.Logger import Log


def substitute(str, filename):
    """ Replace {base}, {ext}, {dir}, {file} to basename, extension, dir
    and filename of file """
    filename = path.abspath(filename)
    (base, ext) = path.splitext(path.basename(filename))
    if ext != '':
        ext = ext[1:]  # remove dot
    cur_dir = path.dirname(filename)
    return str.format(base=base, ext=ext, dir=cur_dir, file=filename)


class Compiler(object):
    """ Define how to compile file """
    def __init__(self, cmd, bin_fn):
        super(Compiler, self).__init__()
        self.cmd = cmd
        self.bin_fn = path.abspath(bin_fn)
        self.args = []

    def compile(self, filename):
        """ Compile file. Result filename can be obitain by bin_file_name() """
        cmd = [self.cmd] + self.args
        cmd = list(map(lambda c: substitute(c, filename), cmd))
        LOG = Log()
        LOG(Log.Vrb, "\trun", ' '.join(cmd))
        return call(cmd)

    def add_args(self, args):
        self.args += args.split(' ')

    def bin_file_name(self, src_filename):
        return substitute(self.bin_fn, path.abspath(src_filename))
