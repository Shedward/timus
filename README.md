timus
=====

Little timus client with simple input/output testing tool.
Lines commented with '//' is not realize yet.

Installation
------------
It's now in alpha state but if you want to try:

    git clone https://github.com/Shedward/timus.git #(or download archive and unpack)
    cd ./timus
    python3 setup.py test

if it's OK, you can install it:

    python3 setup.py install

then you can try testing examples in dir:

    cd ./examples/
    timus test example.cpp

Troubleshooting.
----------------
If you see error 'Compillation error' it may mean that you don't have installed gcc, used in test, timus won't need gcc to work, it's only mean than you can't compile and test your cpp program local with gcc.

If you see error 'Python.h not found' it may mean that you don't have installed `pyhon3-dev` package for compiling psutil, also you can install psutil manualy using your package manager.

If you see error in lxml compiling - install `libxml2-dev libxslt-dev` packages, or install python3-lxml manualy using your package manager.

Requirements
------------

- Python 3.3
- python3-psutil >= 0.6.1 - python package using for benchmark measurements.
- python3-yaml >= 3.10 - python package using for parsing tests files.
- python3-requests >= 1.1.0-1 - using for operation with acm.timus.ru.
- python3-lxml >= 3.1.0-1 - using for parsing answers from requests.
- Any timus supported compiler/interpreter:
	- Visual C 2010
	- Visual C++ 2010
	- GCC 4.7.2
	- G++ 4.7.2
	- FreePascal 2.0.4
	- Visual C# 2012
	- Java 1.7
	- Go 1.1
	- Python 2.7.3
	- Python 3.3.0
	- GHC 7.6.1
	- Ruby 1.9.3

Usage
-----

    Usage: 
    timus [OPTIONS] <action> <filename>
    Use one of the action:
        run     - Run program using by default pattern "$TERM -e {bin}"
                  where {bin} is name of executable file.
                  Use -c to change patern.
        build - Compile source file. For interpret languages do nothing.
                  Use -f to force recompile.
        test    - Test program. Searching for <source>.tests by default.
                  Use -t to specify tests file.
        submit  - Send solution to acm.timus.ru server. Need defined -i and -p opts.



    List of compilers/interpreters for -l option:
        c# - Visual C#
        cl    - Visual C 2010
        cl - Visual C 2010
        cl++ - Visual C 2010
        g++ - G++ 4.7.2
        g++11 - G++ 4.7.2 with C++11
        gcc - GCC 4.7.2
        gcc11 - GCC 4.7.2 with C11
        ghc - Haskell 7.6.1
        go - Go 1.7
        java - Java 1.7
        mono - Mono 3.0.7
        pas - FreePascal 2.4.0
        py2 - Python 2.7
        py3 - Python 3.3
        rb - Ruby 1.9.3
        vb - VB.NET 2010



    Options:
      -h, --help            show this help message and exit
      -t TESTS, --tests=TESTS
                            Specify tests filename. By default searching for
                            <source_file>.tests.
      -r CMD, --run=CMD     Specify pattern for 'run' action
      -f, --force           Force recompile.
      --log-lvl=LOG_LVL     Set logging level:  err - show only error messages,
                            msg - show basic messages (default),  vrb - show every
                            execute command
      --time-limit=TIME_LIMIT
                            Specify time limit in seconds. If program running
                            longer it will be terminated with 'Time limit
                            exceeded' error. Using in test action
      --mem-limit=MEM_LIMIT
                            Specify maximum memory usage in kbytesalso you can use
                            notation like 1K, 5.5M, 0.1g. If program exceed the
                            limit it will be terminated with 'Memory limit
                            exceeded' error. Using in test action.
      -c RUN_COUNT, --run-count=RUN_COUNT
                            Specify amount of runing. More runs, the more accurate
                            the measurements
      -l LANG, --lang=LANG  Specify compiler/language dialect.

###Examples:
####Local:
`timus build source.cpp` - run gcc compiler (chosen by extension of sourcefile).

`timus build source.cpp -lcl++` - recompile using cl instead of gcc.

`timus run -c'gnome-terminal -e {bin}' source.cpp` - run program in gnome-terminal, recompile if needed.

`timus test source.cpp` - test program using tests from source.cpp.tests file.

`timus test source.cpp --run-count 3 --time-lim 2 --mem-lim 5M` - run program 3 times at every test (its let get more accurate result of benchmark) if program will runing longer that 2 seconds or use more than 5Mb of memory it will be terminated.

####Timus:
`timus submit example.scala -i86286AA -p1000`  - send solution of '1000. A+B Problem' from example.scala to acm.timus.ru with JudjeID 86286AA

// `timus init 1000 -l=GCC` - create template for solving 1000s task with GCC, it will create 1000.cpp and files with basic settings and 1000.cpp.tests with tests parsed from condition of the problem.

// `timus sumbit 1000.cpp` - send solution from 1000.cpp to acm.timus.ru using global setting or setting from 1000.cpp

// `timus set id 89542` - global set 89542 as default user id

// `timus set lang G++11` - global set G++11 as default compiler

Tests file format:
------------------
Tests file using yaml format:

Simple tests set writing like this

    - Basics:
        in: 2 2
        out: 4

    - Common things:
        in: 2 5     4 5
        out: 16

Set your editor to keep indentation.
For multiline use |:

    - Multiline:
        in: |
            1 2     5
            5 2 1
        out: 16

    - Negative number:
        in: |
            -1 1 -1 1 -1 1 -11 
            11
        out: |
            0

Also you can use external file if input is too big for tests file:

    - Many numbers:
        in file: 1 to 10.txt
        out: 55
