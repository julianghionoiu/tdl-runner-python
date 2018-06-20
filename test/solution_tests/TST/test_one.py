import unittest

from solutions.TST import one


class TestSum(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(one.get(), 1)


if __name__ == '__main__':
    unittest.main()
