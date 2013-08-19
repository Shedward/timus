#!/usr/bin/env python

from subprocess import Popen, PIPE, STDOUT
from os import path
import yaml

from Logger import Log

#######################################################
#
#   Base realisation.
#
#######################################################


def first_modified_latter(first, second):
    """ Return True if first file modified later than second """
    return path.getmtime(first) > path.getmtime(second)


class TestSet(object):
    """ Iterable and indexable wraper for tests file """
    def __init__(self, filename):
        super(TestSet, self).__init__()
        bare_tests = yaml.load(open(filename))
        tests = []
        for bare_test in bare_tests:
            tests += bare_test.items()
        self.data = tests

    def __iter__(self):
        return self.data.__iter__()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]


class Program(object):
    """ Abstract program object """
    def __init__(self, source_fn):
        super(Program, self).__init__()
        if source_fn:
            self.filename = path.abspath(source_fn)
        else:
            raise Exception("Source filename not defined.")

    def run(self, cmd="{bin}", inp="", timeout=None, verbose=True):
        """ Run custom cmd in shell with {bin} as program file name

        Return: programs output
            If the timeout expires, the child process will be killed
        and then waited for again. The TimeoutExpired exception
        will be re-raised after the child process has terminated
        """
        LOG = Log()
        if verbose:
            LOG(Log.Msg, ":: Runing")
        cmd = cmd.format(bin=self.exec_file())
        LOG(Log.Vrb, "\trun", cmd)
        p = Popen([cmd], stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=True)
        return p.communicate(inp, timeout)[0]

    def test(self, tests):
        """ Run program with tests.

        Tests should be list of [(<descr>, {in:"<in>", out:"<out>"})]
        Program will be runed with <in> in input pipe, and output
        will be compared with expected <out>
        """
        LOG = Log()
        LOG(Log.Msg, ":: Testing")
        i = 0
        for descr, tst in tests:
            i += 1
            inp = str(tst["in"]).encode()
            out = str(tst["out"]).encode()

            recived = self.run(inp=inp, verbose=False)

            if recived == out:
                LOG(Log.Msg, "  {0}: pass: {1},".format(i, descr))
            else:
                LOG(Log.Msg, "  {0}: FAIL: {1},".format(i, descr))
                LOG(Log.Err, "{0}: error: Test {1} failed."
                             .format(self.source(), descr))
                LOG(Log.Err, "Expected:\n"
                             "'{0}'\n"
                             "Recived:\n"
                             "'{1}'"
                             .format(out, recived))

    def source(self):
        """ Return source filename """
        return self.filename

    def exec_file(self):
        return self.filename


class CompilingProgram(Program):
    """ Compiling program object.
    Using as base for compiling languages programs.
    """
    def __init__(self, source_fn, compiler=None):
        super(CompilingProgram, self).__init__(source_fn)
        self.compiler = None
        self.bin_fn = ""
        if compiler:
            self.compiler = compiler
            self.bin_fn = compiler.bin_file_name(source_fn)
            self.is_compiled = path.exists(self.bin_fn) and \
                first_modified_latter(self.bin_fn, self.source())

    def exec_file(self):
        return self.bin_fn

    def compile(self, force=False, compiler=None):
        """ Compile program from source file if it modified """
        if compiler is None:
                compiler = self.compiler
        LOG = Log()
        LOG(Log.Msg, ":: Compiling")
        if not force and path.exists(self.bin_fn)\
           and first_modified_latter(self.bin_fn, self.source()):
            LOG(Log.Msg, "\tAlready compiled.")
            self.is_compiled = True
        else:
            if compiler is None:
                raise Exception("Compiler not defined")
            else:
                res = compiler.run(self.source())
                self.is_compiled = res == 0
                if self.is_compiled:
                    LOG(Log.Msg, "\tOK.")
                    self.bin_fn = compiler.bin_file_name(self.source())
                else:
                    LOG(Log.Msg, "\tFailed.")
                    exit()
        return self.is_compiled

    def run(self, cmd="{bin}", inp="", timeout=None, verbose=True):
        """ Run custom cmd in shell with {bin} as program file name

        Return: programs output
            If the timeout expires, the child process will be killed
        and then waited for again. The TimeoutExpired exception
        will be re-raised after the child process has terminated
        """
        if self.is_compiled or self.compile():
            return super(CompilingProgram, self) \
                .run(cmd, inp, timeout, verbose)

    def test(self, tests):
        if self.is_compiled or self.compile():
            super(CompilingProgram, self).test(tests)


class InterprentingProgram(Program):
    """docstring for InterprentProgram"""
    def __init__(self, arg):
        super(InterprentingProgram, self).__init__()
        self.arg = arg
