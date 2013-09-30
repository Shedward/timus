import unittest

from timus.Options import Options
from timus.Logger import Log
from timus.Exceptions import WrongParams

class TestOptions(unittest.TestCase):
	def test_basic_options(self):
		opts = Options(["run","source.cpp",
						   "-f", 
						   "--run-count","5", 
						   "--tl", "2.5",
						   "-t", "test.file",
						   "-l", "gcc",
						   "-r", "run_cmd"])
		opts.need_args('filename') 
		opts.need_opts('run_count', 'tests', 'lang')
		self.assertEqual(opts.action, "run")
		self.assertEqual(opts.opt.filename, "source.cpp")
		self.assertEqual(opts.opt.force, True)
		self.assertEqual(opts.opt.run_count, 5)
		self.assertEqual(opts.opt.time_limit, 2.5)
		self.assertEqual(opts.opt.tests, "test.file")
		self.assertEqual(opts.opt.lang, "gcc")
		self.assertEqual(opts.opt.cmd, "run_cmd")

	def test_log_lvl_option(self):
		opts = Options(["run", "source.cpp", "--ll", "vrb"])
		self.assertEqual(opts.opt.log_lvl, Log.Vrb)
		opts = Options(["run","source.cpp", "--ll", "err"])
		self.assertEqual(opts.opt.log_lvl, Log.Err)
		opts = Options(["run","source.cpp", "--ll", "msg"])
		self.assertEqual(opts.opt.log_lvl, Log.Msg)

	def test_mem_limit_option(self):
		opts = Options(["run","source.cpp", "--ml", "50"])
		self.assertEqual(opts.opt.mem_limit, 51200)
		opts = Options(["run","source.cpp", "--ml", "50."])
		self.assertEqual(opts.opt.mem_limit, 51200)
		opts = Options(["run","source.cpp", "--ml", "1G"])
		self.assertEqual(opts.opt.mem_limit, 1073741824)
		opts = Options(["run","source.cpp", "--ml", "1M"])
		self.assertEqual(opts.opt.mem_limit, 1048576)
		opts = Options(["run","source.cpp", "--ml", "50.k"])
		self.assertEqual(opts.opt.mem_limit, 51200)

	def test_wrong_param_rise(self):
		self.assertRaises(WrongParams, 
			lambda : Options(["--ml", "12h"]))

if __name__ == '__main__':
    unittest.main()
