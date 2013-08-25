#!/usr/bin/env python

from os import path
from subprocess import call

from Logger import Log


def apply_template(str, filename):
    """ Replace {base}, {ext}, {dir} to data. """
    (base, ext) = path.basename(filename).split('.')
    cur_dir = path.abspath(filename)
    return str.format(base=base, ext=ext, dir=cur_dir)


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
        args = apply_template(args, filename)
        LOG = Log()
        LOG(Log.Vrb, "\trun", args)
        return call(args, shell=True)

    def add_args(self, args):
        self.args += " " + args

    def bin_file_name(self, src_filename=""):
        return apply_template(self.bin_fn, path.abspath(src_filename))
