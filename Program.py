#!/usr/bin/env python

from os import path
import yaml
from subprocess import PIPE
from io import IOBase

from Observed import ObservedCmd, TimeLimitExceeded, MemoryLimitExceeded
from Logger import Log


class WrongOutput(Exception):
    pass


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
        if source_fn:
            self.filename = path.abspath(source_fn)
        else:
            raise Exception("Source filename not defined.")

    def run(self, cmd="{bin}", inp="", time_limit=None, mem_limit=None):
        """ Run custom cmd in shell with {bin} as program file name

        Return: programs output
            If the timeout expires, the child process will be killed
        and then waited for again. The TimeoutExpired exception
        will be re-raised after the child process has terminated
        """
        LOG = Log()
        LOG(Log.Msg, ":: Runing")
        cmd = cmd.format(bin=self.exec_file())
        LOG(Log.Vrb, "\trun", cmd)

        cmd = ObservedCmd(cmd)
        cmd.run(inp=inp, time_limit=time_limit, mem_limit=mem_limit)
        LOG(Log.Msg, "[{0}s, {1}K]".format(cmd.max_time, cmd.max_mem))

    def test(self, tests, run_count=1, mem_limit=None,
             time_limit=None):
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

            if "in" in tst:
                inp = str(tst["in"]).encode()
                stdin = PIPE
            elif "in file" in tst:
                inp = None
                stdin = open(tst["in file"])
            else:
                LOG(Log.Err, "No input in test", descr)

            out = str(tst["out"]).rstrip().encode()

            max_time = 0
            max_mem = 0

            cmd = ObservedCmd(self.exec_file())
            try:
                for _ in range(run_count):
                    if isinstance(stdin, IOBase):
                        stdin.seek(0)
                    cmd.run(inp=inp, time_limit=time_limit,
                            mem_limit=mem_limit, stdin=stdin)
                    recived = cmd.output[0].rstrip()
                    if cmd.max_rss > max_mem:
                        max_mem = cmd.max_rss
                    if cmd.time > max_time:
                        max_time = cmd.time

                if recived != out:
                    raise WrongOutput()

            except WrongOutput:
                LOG(Log.Msg, "  {0}: fail: {1}".format(i, descr))
                LOG(Log.Err, "{0}: error: Test {1} failed."
                             .format(self.source(), descr))
                LOG(Log.Err, "Expected:\n"
                             "'{0}'\n"
                             "Recived:\n"
                             "'{1}'"
                             .format(out.decode(), recived.decode()))

            except TimeLimitExceeded:
                LOG(Log.Msg, "  {0}: fail: {1}".format(i, descr))
                LOG(Log.Err, "{0}: error: Time limit {1}s exceeded."
                    .format(self.source(), time_limit))

            except MemoryLimitExceeded:
                LOG(Log.Msg, "  {0}: fail: {1}".format(i, descr))
                LOG(Log.Err, "{0}: error: Memory limit {1:0.1f}K exceeded."
                    .format(self.source(), mem_limit / 1024))

            else:
                LOG(Log.Msg, "  {0}: pass: {1} [{2}s, {3:0.1f}K]"
                    .format(i, descr, max_time, max_mem / 1024))

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

    def test(self, tests, run_count=1, mem_limit=None,
             time_limit=None):
        if self.is_compiled or self.compile():
            super(CompilingProgram, self).test(tests, run_count, mem_limit,
                                               time_limit)


class InterprentingProgram(Program):
    """docstring for InterprentProgram"""
    def __init__(self, arg):
        super(InterprentingProgram, self).__init__()
        self.arg = arg
