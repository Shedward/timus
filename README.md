timus
=====

Little timus client with simple input/output testing tool.

Now it's just cpp programs testing tool.
Lines commented with '//' is not realize yet.

To try just clone or download and extract and type `./timus test example.cpp`

Requirements
------------

- Python 3.3
- psutil - python package using for benchmark measurements.
- yaml - python package using for parsing tests files.
- Any timus supported compiler/interpreter:
	- // Visual C 2010
	- // Visual C++ 2010
	- // GCC 4.7.2
	- G++ 4.7.2
	- // FreePascal 2.0.4
	- // Visual C# 2012
	- // Java 1.7
	- // Go 1.1
	- // Python 2.7.3
	- // Python 3.3.0
	- // GHC 7.6.1
	- // Ruby 1.9.3

Usage
-----

    timus [OPTIONS] <action> <filename>
    Use one of the action:
        run     - Run program using by default pattern "konsole --hold -e {bin}"
                  where {bin} is name of executable file.
                  Use -c to change pattern.
        compile - Compile source file.
                  Use -f to force recompile.
        test    - Test program. Searching for <source>.tests by default.
                  Use -t to specify tests file.



    Options:
      -h, --help            show this help message and exit
      -t TESTS, --tests=TESTS
                            Specify tests filename. By default searching for
                            <source_file>.tests.
      -r CMD, --run=CMD     Specify pattern for 'run' action
      -f, --force           Force recompile.
      -l LOG_LVL, --log-lvl=LOG_LVL
                            Set logging level:  err - show only error messages,
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
                            Specify amount of running. More runs, the more accurate
                            the measurements

###Examples:
####Local:
`timus compile source.cpp` - run gcc compiler (chosen by extension of sourcefile). [it's suport gcc only yet]

// `timus compile source.cpp -lCL++` - compile using cl instead of gcc.

`timus run -c'gnome-terminal -e {bin}' source` - run program in gnome-terminal, recompile if needed.

`timus test source.cpp` - test program using tests from source.cpp.tests file.

`timus test source.cpp --run-count 3 --time-lim 2 --mem-lim 5M` - run program 3 times at every test (its let get more accurate result of benchmark) if program will runing longer that 2 seconds or use more than 5Mb of memory it will be terminated.

####Timus:
// `timus set id 89542` - global set 89542 as default user id

// `timus set lang G++11` - global set G++11 as default compiler

// `timus init 1000 -l=GCC` - create template for solving 1000s task with GCC, it will create 1000.cpp and files with basic settings and 1000.cpp.tests with tests parsed from condition of the problem.

// `timus sumbit 1000.cpp` - send solution from 1000.cpp to acm.timus.ru using global setting or setting from 1000.cpp

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

    - Many numers:
        in file: tests
        out: 1783293664
