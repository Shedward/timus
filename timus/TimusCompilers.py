from os import path

from timus.Compiler import Compiler, substitute
from timus.Exceptions import WrongLang, NotSupportedExt
from timus.Logger import Log
from timus.Program import Program, CompilingProgram

class CL(Compiler):
    """Visual C 2010"""
    def __init__(self):
        super(CL, self).__init__("cl", "{base}.exe")
        self.add_args(r"/TC /MT /EHsc /GL /O2 /W3 /Za "
                      r"/D \"_CRT_SECURE_NO_WARNINGS\" "
                      r"/D \"_CRT_SECURE_NO_DEPRECATE\" "
                      r"/D \"ONLINE_JUDGE\" "
                      r"{file}")


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
                      r"{file}")


class clppProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(clppProgram, self).__init__(source_fn=sourcefn, compiler=CLPP())


class GCC(Compiler):
    """GCC 4.7.2"""
    def __init__(self):
        super(GCC, self).__init__("gcc", "{base}")
        self.add_args(r"-static -fno-strict-aliasing "
                      r"-DONLINE_JUDGE -lm -s "
                      r"-o {base} {file}")


class gccProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(gccProgram, self).__init__(source_fn=sourcefn, compiler=GCC())


class GCC11(Compiler):
    """GCC 4.7.2 C11"""
    def __init__(self):
        super(GCC11, self).__init__("gcc", "{base}")
        self.add_args(r"-static -fno-strict-aliasing "
                      r"-DONLINE_JUDGE -lm -s -std=c11 -O2 "
                      r"-o {base} {file}")


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
                      r"-o {base} {file}")


class gppProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(gppProgram, self).__init__(source_fn=sourcefn, compiler=GPP())


class GPP11(Compiler):
    """G++ 4.7.2 C++11"""
    def __init__(self):
        super(GPP11, self).__init__("g++", "{base}")
        self.add_args(r"-static -fno-strict-aliasing "
                      r"-DONLINE_JUDGE -lm -s -x c++ -std=c++0x -O2 "
                      r"-o {base} {file}")


class gpp11Program(CompilingProgram):
    def __init__(self, sourcefn):
        super(gpp11Program, self).__init__(source_fn=sourcefn,
                                           compiler=GPP11())


class FreePascal(Compiler):
    """FreePascal 2.0.4"""
    def __init__(self):
        super(FreePascal, self).__init__("ppc386", "{base}")
        self.add_args(r"{file} -Ci-o-r-t- -Xs "
                      r"-Sdgich -Se10 -l- -vwnh -dONLINE_JUDGE")


class pasProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(pasProgram, self).__init__(source_fn=sourcefn,
                                         compiler=FreePascal())


class GHC(Compiler):
    """GHC 7.6.1"""
    def __init__(self):
        super(GHC, self).__init__("ghc", "{base}")
        self.add_args(r"-v0 -O {file}")


class hsProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(hsProgram, self).__init__(source_fn=sourcefn,
                                        compiler=GHC())


class GO(Compiler):
    """Go 1.1"""
    def __init__(self):
        super(GO, self).__init__("go", "{base}")
        self.add_args(r"build {file}")


class goProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(goProgram, self).__init__(source_fn=sourcefn,
                                        compiler=GO())


class DMCS(Compiler):
    """Mono"""
    def __init__(self):
        super(DMCS, self).__init__("dmcs", "{base}.exe")
        self.add_args(r"/o+ /d:ONLINE_JUDGE "
                      r"/r:System.Numerics.dll "
                      r"{file}")


class monoProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(monoProgram, self).__init__(source_fn=sourcefn,
                                          compiler=DMCS(),
                                          run_cmd=["mono", "{bin}"])


class CSC(Compiler):
    """Visual C# 2010"""
    def __init__(self):
        super(CSC, self).__init__("csc", "{base}.exe")
        self.add_args(r"/o+ /d:ONLINE_JUDGE "
                      r"/r:System.Numerics.dll "
                      r"{file}")


class cscProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(cscProgram, self).__init__(source_fn=sourcefn,
                                         compiler=CSC())


class JAVAC(Compiler):
    """Javac"""
    def __init__(self):
        super(JAVAC, self).__init__("javac", "{base}")
        self.add_args(r"{file}")

    def bin_file_name(self, src_filename=""):
        return substitute("{base}", src_filename)


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

class scalac(Compiler):
    """Javac"""
    def __init__(self):
        super(scalac, self).__init__("scalac", "{base}")
        self.add_args(r"-optimise -feature {file}")

    def bin_file_name(self, src_filename=""):
        return substitute("{base}", src_filename)


class scalaProgram(CompilingProgram):
    def __init__(self, sourcefn):
        super(scalaProgram, self).__init__(source_fn=sourcefn,
                                           compiler=scalac(),
                                           run_cmd=["scala", "-DONLINE_JUDGE",
                                                    "{bin}"])

def program(lang):
    LANG = {
        "cl"   : clProgram,
        "cl++" : clppProgram,
        "gcc"  : gccProgram,
        "gcc11": gcc11Program,
        "g++"  : gppProgram,
        "g++11": gpp11Program,
        "pas"  : pasProgram,
        "ghc"  : hsProgram,
        "go"   : goProgram,
        "c#"   : cscProgram,
        "mono" : monoProgram,
        "java" : javaProgram,
        "py2"  : py2Program,
        "py3"  : py3Program,
        "rb"   : rubyProgram,
        "scala": scalaProgram
    }
    if lang in LANG:
        return LANG[lang]
    else:
        raise WrongLang(lang)

_DESC = {
        'cl'   : "Visual C 2010",
        'cl++' : "Visual C 2010",
        'gcc'  : "GCC 4.7.2",
        'gcc11': "GCC 4.7.2 with C11",
        'g++'  : "G++ 4.7.2",
        'g++11': "G++ 4.7.2 with C++11",
        'pas'  : "FreePascal 2.4.0",
        'ghc'  : "Haskell 7.6.1",
        'go'   : "Go 1.7",
        'c#'   : "Visual C#",
        'mono' : "Mono 3.0.7",
        'java' : "Java 1.7",
        'py2'  : "Python 2.7",
        'py3'  : "Python 3.3",
        'rb'   : "Ruby 1.9.3",
        'vb'   : "VB.NET 2010",
        'scala': "Scala 2.10.1"
    }
def lang_description(lang):

    if lang in _DESC:
        return _DESC[lang]
    else:
        raise WrongLang(lang)

_EXT = {
    "cpp"  : ("g++", "cl++","g++11"),
    "c"    : ("gcc", "cl", "gcc11"),
    "pas"  : ("pas",),
    "py"   : ("py3", "py2"),
    "java" : ("java",),
    "go"   : ("go",),
    "hs"   : ("ghc",),
    "rb"   : ("rb",),
    "cs"   : ("mono", "c#"),
    "scala": ("scala",)
    }

def lang_by_ext(ext):
    if ext in _EXT:
        return _EXT[ext]
    else:
        raise NotSupportedExt(ext)

def ext_by_lang(lang):
    rev_EXT = {}
    for k, i in _EXT.items():
        rev_EXT.update(dict.fromkeys(i, k))
    if lang in rev_EXT:
        return rev_EXT[lang]
    else:
        WrongLang(lang)

def show_lang_list():
    LANGS_LIST = '\n\t'.join([lang + " - " + desc for lang, desc in _DESC.items()])
    MSG = """
        List of compilers/interpreters for -l option:

    """ + LANGS_LIST
    print(MSG)

def autodetect_lang(filename):
    base, ext = path.splitext(filename)
    if ext != '':
        ext = ext[1:] # remove leading dot
    LOG = Log()
    lang = lang_by_ext(ext)
    if len(lang) > 1:
        LOG(Log.Msg, "Warning: Suported '{0}', used '{1}' by default."
                      .format(lang, lang[0]))
    return lang[0]

def TimusProgram(source, lang=None):
    if lang is None:
        lang = autodetect_lang(source)

    prog = program(lang)(source)
    prog.lang = lang
    return prog
