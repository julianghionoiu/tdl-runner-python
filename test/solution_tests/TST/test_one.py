import pytest

from solutions.TST import one


class TestSum(pytest.TestCase):
    def test_sum(self):
        assert one.get() == 1


if __name__ == '__main__':
    pytest.main()
