import unittest

from auction.digital_product import DigitalProduct


class DigitalProductTestCase(unittest.TestCase):
    def test_initialization(self):
        dp = DigitalProduct("Some data!")
        self.assertEqual(dp.get_data, "Some data!")


if __name__ == '__main__':
    unittest.main()
