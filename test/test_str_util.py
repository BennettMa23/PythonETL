import unittest
from util import strutil

class TestStrUtil(unittest.TestCase):
    def setUp(self) -> None:
        pass
    def tearDown(self) -> None:
        pass

    def test_check_null(self):
        data = ''
        result = strutil.check_null(data)
        self.assertEqual(True, result)

        data = None
        result = strutil.check_null(data)
        self.assertEqual(True, result)

    def test_check_str_null_and_transform_to_sql_null(self):
        data = 'Tom'
        result = strutil.check_str_null_and_transform_to_sql_null(data)
        self.assertEqual("'Tom'", result)  # "'Tom'"

        data = ''
        result = strutil.check_str_null_and_transform_to_sql_null(data)
        self.assertEqual('null', result)

    def test_clear_str(self):
        data = 'abc"de"fg'
        result = strutil.clear_str(data)
        self.assertEqual('abcdefg', result)