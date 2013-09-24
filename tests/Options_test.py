import unittest

from timus import Options
from timus.Logger import Log

class TestOptions(unittest.TestCase):
	def test_basic_options(self):
		opts = Options.parse_args(["run","source.cpp",
										   "-f", 
									   	   "--run-count","5", 
										   "--tl", "2.5",
										   "-t", "test.file",
										   "-l", "gcc",
										   "-r", "run_cmd"])
		self.assertEqual(opts.action, "run")
		self.assertEqual(opts.filename, "source.cpp")
		self.assertEqual(opts.force, True)
		self.assertEqual(opts.run_count, 5)
		self.assertEqual(opts.time_limit, 2.5)
		self.assertEqual(opts.tests, "test.file")
		self.assertEqual(opts.lang, "gcc")
		self.assertEqual(opts.cmd, "run_cmd")

	def test_log_lvl_option(self):
		opts = Options.parse_args(["run", "source.cpp", "--ll", "vrb"])
		self.assertEqual(opts.log_lvl, Log.Vrb)
		opts = Options.parse_args(["run","source.cpp", "--ll", "err"])
		self.assertEqual(opts.log_lvl, Log.Err)
		opts = Options.parse_args(["run","source.cpp", "--ll", "msg"])
		self.assertEqual(opts.log_lvl, Log.Msg)

	def test_mem_limit_option(self):
		opts = Options.parse_args(["run","source.cpp", "--ml", "50"])
		self.assertEqual(opts.mem_limit, 51200)
		opts = Options.parse_args(["run","source.cpp", "--ml", "50."])
		self.assertEqual(opts.mem_limit, 51200)
		opts = Options.parse_args(["run","source.cpp", "--ml", "1G"])
		self.assertEqual(opts.mem_limit, 1073741824)
		opts = Options.parse_args(["run","source.cpp", "--ml", "1M"])
		self.assertEqual(opts.mem_limit, 1048576)
		opts = Options.parse_args(["run","source.cpp", "--ml", "50.k"])
		self.assertEqual(opts.mem_limit, 51200)

	def test_wrong_param_rise(self):
		self.assertRaises(Options.WrongParams, 
			lambda : Options.parse_args(["--ml", "12h"]))