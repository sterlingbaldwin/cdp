import unittest
import os
import cdp.cdp_parameter
import cdp.cdp_parser


class TestCDPParser(unittest.TestCase):

    class MyCDPParameter(cdp.cdp_parameter.CDPParameter):
        def check_values(self):
            pass

    class MyCDPParser(cdp.cdp_parser.CDPParser):
        def __init__(self, *args, **kwargs):
            super(TestCDPParser.MyCDPParser, self).__init__(
                TestCDPParser.MyCDPParameter, *args, **kwargs)

        def load_default_args(self):
            super(TestCDPParser.MyCDPParser, self).load_default_args()
            self.add_argument(
                '-v', '--vars',
                type=str,
                nargs='+',
                dest='vars',
                help='Variables to use',
                required=False)

    def write_file(self, file_name, contents):
        f = open(file_name, 'w')
        f.write(contents)
        f.close()

    def setUp(self):
        self.cdp_parser = self.MyCDPParser()

    def test_load_default_args(self):
        self.write_file('param_file.py', 'vars=["v1", "v2"]\n')
        try:
            self.cdp_parser.add_args_and_values(['-p', 'param_file.py'])
            self.cdp_parser.get_parameter()
        except:
            self.fail('Failed to load a parameter with -p.')
        os.remove('param_file.py')

    def test_load_custom_args(self):
        try:
            self.cdp_parser.add_args_and_values(['-v', 'v1', 'v2'])
        except:
            self.fail('Failed to load variables with -v.')

    def test_get_parameter(self):
        self.cdp_parser.add_args_and_values(['-v', 'v1', 'v2'])
        para = self.cdp_parser.get_parameter()
        self.assertTrue(para.vars, ['v1', 'v2'])

if __name__ == '__main__':
    unittest.main()
