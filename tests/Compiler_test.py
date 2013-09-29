import unittest

from os.path import abspath

import timus.Compiler


class TestSubstitude(unittest.TestCase):
    def test_substitude(self):
        s = "{dir}/{base}.{ext}"
        filename = __file__
        substituted = timus.Compiler.substitute(s, filename)
        self.assertEqual(filename, substituted)

    def test_separated_sub(self):
        fn = "/long/dir/file.name.ext"
        sub = timus.Compiler.substitute
        self.assertEqual(sub("{dir}", fn), "/long/dir")
        self.assertEqual(sub("{base}", fn), "file.name")
        self.assertEqual(sub("{ext}", fn), "ext")


class TestCompiler(unittest.TestCase):
    def setUp(self):
        self.comp = timus.Compiler.Compiler("dir {dir}", "{base}")

    def test_compile(self):
        fn = "file.ext"
        self.assertEqual(self.comp.compile(fn), 0)
        self.assertEqual(self.comp.bin_file_name(fn), abspath("file"))

    def test_add_args(self):
        self.comp.add_args("-wrong /opt")
        self.assertEqual(self.comp.args, " -wrong /opt")
        self.assertNotEqual(self.comp.compile("file.ext"), 0)


if __name__ == '__main__':
    unittest.main()

