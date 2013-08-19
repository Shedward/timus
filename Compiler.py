#!/usr/bin/env python

from os import path
from subprocess import call

from Logger import Log

#######################################################
#
#	Base realisation.
#
#######################################################


def apply_mask(str, filename):
    """ Replace {base}, {ext}, {dir} to data. """
    (base, ext) = path.basename(filename).split('.')
    cur_dir = path.abspath(filename)
    return str.format(base=base, ext=ext, dir=cur_dir)


class Compiler(object):
    """ Define how to compile file """
    def __init__(self, cmd, args, bin_fn):
        super(Compiler, self).__init__()
        self.cmd = cmd
        self.args = args
        self.bin_fn = path.abspath(bin_fn)

    def run(self, filename):
        """ Compile file. Result filename can be obitain by bin_file_name() """
        args = self.cmd + " " + ' '.join(self.args)\
            + " " + path.abspath(filename)
        args = apply_mask(args, filename)
        LOG = Log()
        LOG(Log.Vrb, "\trun", args)
        return call(args, shell=True)

    def add_args(self, *args):
        self.args += args

    def bin_file_name(self, src_filename=""):
        return apply_mask(self.bin_fn, path.abspath(src_filename))

#######################################################
#
#	Custom compilers.
#
#######################################################


class GCC(Compiler):
    """ Default gcc compiler """
    def __init__(self, args=None):
        super(GCC, self).__init__("gcc", ["-o{base}"], "{base}")
        if args is not None:
            self.add_args(args)


class Clang(Compiler):
    """ Default clang compiler """
    def __init__(self, args=None):
        super(GCC, self).__init__("clang", ["-o{base}"], "{base}")
        if args is not None:
            self.add_args(args)


class GPP(Compiler):
    """ Default g++ compiler """
    def __init__(self, args=None):
        super(GPP, self).__init__("g++", ["-o{base}"], "{base}")
        if args is not None:
            self.add_args(args)
