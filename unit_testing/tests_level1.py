import unittest

from calculator import Calculator

class TestOperations(unittest.TestCase):
    def setUp(self):
        self.c = Calculator(12,3)

    def test_sum(self):
        self.assertEqual(self.c.do_sum(), 15, "The sum is wrong")

    def test_product(self):
        self.assertEqual(self.c.do_product(), 36, "The product is wrong")

    def test_subtract(self):
        self.assertEqual(self.c.do_subtract(), 9, "The subtraction is wrong")

    def test_divide(self):
        self.assertEqual(self.c.do_divide(), 4, "The division is wrong")


if __name__ == "__main__":
    unittest.main()
