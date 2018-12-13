import pytest

from solutions.SUM import sum_solution


class TestSum(pytest.TestCase):
    def test_sum(self):
        assert sum_solution.compute(1, 2) == 3


if __name__ == '__main__':
    pytest.main()
