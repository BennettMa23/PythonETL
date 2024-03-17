import unittest
from util import timeutil

class TestTimeUtil(unittest.TestCase):
    def setUp(self) -> None:
        pass
    def tearDown(self) -> None:
        pass

    def test_ts13_to_ts10(self):
        ts = 1645539742000  # Java => 时间戳 => 13位 => 写入到JSON文件 => 2022-02-22 22:22:22
        result = timeutil.ts13_to_ts10(ts)
        self.assertEqual(1645539742, result)

    def test_ts10_to_date_str(self):
        ts = 1645539742
        result = timeutil.ts10_to_date_str(ts)
        self.assertEqual('2022-02-22 22:22:22', result)