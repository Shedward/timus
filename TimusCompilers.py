from Compiler import Compiler, apply_template
from Program import Program, CompilingProgram
from Logger import Log


class CL(Compiler):
    """Visual C 2010"""
    def __init__(self):
        super(CL, self).__init__("cl", "{base}.exe")
        self.add_args(r"/TC /MT /EHsc /GL /O2 /W3 /Za "
                      r"/D \"_CRT_SECURE_NO_WARNINGS\" "
                      r"/D \"_CRT_SECURE_NO_DEPRECATE\" "
                      r"/D \"ONLINE_JUDGE\" "
                      r"{base}.{ext}")


class clProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(clProgram, self).__init__(source_fn=sourcefn, compiler=CL())


class CLPP(Compiler):
    """Visual C++ 2010"""
    def __init__(self):
        super(CLPP, self).__init__("cl", "{base}.exe")
        self.add_args(r"/TP /MT /EHsc /GL /O2 /W3 /Za "
                      r"/D \"_CRT_SECURE_NO_WARNINGS\" "
                      r"/D \"_CRT_SECURE_NO_DEPRECATE\" "
                      r"/D \"ONLINE_JUDGE\" "
                      r"{base}.{ext}")


class clppProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(clProgram, self).__init__(source_fn=sourcefn, compiler=CLPP())


class GCC(Compiler):
    """GCC 4.7.2"""
    def __init__(self):
        super(GCC, self).__init__("gcc", "{base}")
        self.add_args(r"-static -fno-strict-aliasing "
                      r"-DONLINE_JUDGE -lm -s "
                      r"-o {base} {base}.{ext}")


class gccProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(gccProgram, self).__init__(source_fn=sourcefn, compiler=GCC())


class GCC11(Compiler):
    """GCC 4.7.2 C11"""
    def __init__(self):
        super(GCC11, self).__init__("gcc", "{base}")
        self.add_args(r"-static -fno-strict-aliasing "
                      r"-DONLINE_JUDGE -lm -s -std=c11 -O2 "
                      r"-o {base} {base}.{ext}")


class gcc11Program(CompilingProgram):
    def __init__(self, sourcefn):
        super(gcc11Program, self).__init__(source_fn=sourcefn,
                                           compiler=GCC11())


class GPP(Compiler):
    """G++ 4.7.2"""
    def __init__(self):
        super(GPP, self).__init__("g++", "{base}")
        self.add_args(r"-static -fno-strict-aliasing "
                      r"-DONLINE_JUDGE -lm -s -x c++ -O2 "
                      r"-o {base} {base}.{ext}")


class gppProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(gppProgram, self).__init__(source_fn=sourcefn, compiler=GPP())


class GPP11(Compiler):
    """G++ 4.7.2 C++11"""
    def __init__(self):
        super(GPP11, self).__init__("g++", "{base}")
        self.add_args(r"-static -fno-strict-aliasing "
                      r"-DONLINE_JUDGE -lm -s -x c++ -std=c11 -O2 "
                      r"-o {base} {base}.{ext}")


class gpp11Program(CompilingProgram):
    def __init__(self, sourcefn):
        super(gpp11Program, self).__init__(source_fn=sourcefn,
                                           compiler=GPP11())


class FreePascal(Compiler):
    """FreePascal 2.0.4"""
    def __init__(self):
        super(FreePascal, self).__init__("ppc386", "{base}")
        self.add_args(r"{base}.{ext} -Ci-o-r-t- -Xs "
                      r"-Sdgich -Se10 -l- -vwnh -dONLINE_JUDGE")


class pasProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(pasProgram, self).__init__(source_fn=sourcefn,
                                         compiler=FreePascal())


class GHC(Compiler):
    """GHC 7.6.1"""
    def __init__(self):
        super(GHC, self).__init__("ghc", "{base}")
        self.add_args(r"-v0 -O {base}.{ext}")


class hsProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(hsProgram, self).__init__(source_fn=sourcefn,
                                        compiler=GHC())


class GO(Compiler):
    """Go 1.1"""
    def __init__(self):
        super(GO, self).__init__("go", "{base}")
        self.add_args(r"build {base}.{ext}")


class goProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(goProgram, self).__init__(source_fn=sourcefn,
                                        compiler=GO())


class MCS(Compiler):
    """Mono"""
    def __init__(self):
        super(MCS, self).__init__("mcs", "{base}.exe")
        self.add_args(r"/o+ /d:ONLINE_JUDGE "
                      r"/r:System.Numerics.dll "
                      r"{base}.{ext}")


class monoProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(monoProgram, self).__init__(source_fn=sourcefn,
                                          compiler=MCS(),
                                          run_cmd=["mono", "{bin}"])


class CSC(Compiler):
    """Visual C# 2010"""
    def __init__(self):
        super(CSC, self).__init__("csc", "{base}.exe")
        self.add_args(r"/o+ /d:ONLINE_JUDGE "
                      r"/r:System.Numerics.dll "
                      r"{base}.{ext}")


class cscProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(cscProgram, self).__init__(source_fn=sourcefn,
                                         compiler=CSC())


class JAVAC(Compiler):
    """Javac"""
    def __init__(self):
        super(JAVAC, self).__init__("javac", "{base}")
        self.add_args(r"{base}.{ext}")

    def bin_file_name(self, src_filename=""):
        return apply_template("{base}", src_filename)


class javaProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(javaProgram, self).__init__(source_fn=sourcefn,
                                          compiler=JAVAC(),
                                          run_cmd=["java", "-Xmx544m",
                                                   "-Xss64m", "-DONLINE_JUDGE",
                                                   "{bin}"])


class py2Program(Program):
    def __init__(self, sourcefn):
        super(py2Program, self).__init__(source_fn=sourcefn,
                                         run_cmd=["python2", "{bin}"])


class py3Program(Program):
    def __init__(self, sourcefn):
        super(py3Program, self).__init__(source_fn=sourcefn,
                                         run_cmd=["python3", "{bin}"])


class rubyProgram(Program):
    def __init__(self, sourcefn):
        super(rubyProgram, self).__init__(source_fn=sourcefn,
                                          run_cmd=["ruby", "{bin}"])
LANG = {
    "cl": clProgram,
    "cl++": clppProgram,
    "gcc": gccProgram,
    "gcc11": gcc11Program,
    "g++": gppProgram,
    "g++11": gpp11Program,
    "pas": pasProgram,
    "ghc": hsProgram,
    "go": goProgram,
    "c#": cscProgram,
    "mono": monoProgram,
    "java": javaProgram,
    "py2": py2Program,
    "py3": py3Program,
    "rb": rubyProgram
}

EXT = {
    "cpp": ("g++", "cl++"),
    "c": ("gcc", "cl"),
    "pas": "pas",
    "py": ("py3", "py2"),
    "java": "java",
    "go": "go",
    "hs": "ghc",
    "rb": "rb",
    "cs": ("mono", "c#")
}


def autodetect_program(filename):
    base, ext = filename.split('.')
    if ext in EXT:
        lang = EXT[ext]
        program = None
        if isinstance(lang, str):
            program = LANG[lang]
        elif isinstance(lang, tuple):
            LOG = Log()
            LOG(Log.Msg, "Warning: Suported {0}, used {1} by default."
                         .format(lang, lang[0]))
            program = LANG[lang[0]]
        else:
            LOG(Log.Msg, "Wrong program type {0}".format(type(lang)))
        return program(filename)

    else:
        LOG(Log.Err, "Filetype {0} not suported.".format(ext))
        exit()
