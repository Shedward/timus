import unittest
import pkg_resources

from timus import Timus
from timus.RetCodes import RetCode
from timus import Options
from timus.Conf import Conf


class TestTimus(unittest.TestCase):
    def setUp(self):
        Conf().reset()

    def test_timus(self):
        fn = pkg_resources.resource_filename('examples', 'example.cpp')
        self.assertEqual(Timus.main(['test', fn, '-f']), RetCode.WrongOutput)

    def test_timus_wrong_params(self):
        self.assertRaises(Options.WrongParams,
                          lambda: Timus.main([""]))
        self.assertRaises(Timus.SourceFileNotFound,
                          lambda: Timus.main(["test", "no_file"]))

if __name__ == '__main__':
    unittest.main()
