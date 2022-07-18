import unittest

from blockchain.account import Account
from blockchain.auction.digital_product import DigitalProduct


class DigitalProductTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        account_gen = Account()
        cls.first = account_gen.get_account()
        cls.second = account_gen.get_account()
        cls.gen = account_gen

    def test_initialization(self):
        dp = DigitalProduct("Some data!")
        self.assertEqual(dp.get_data, "Some data!")

    def test_ownership(self):
        dp = DigitalProduct("Some data!")
        self.assertTrue(dp.become_owner(self.first))
        self.assertTrue(dp.verify_owner(self.first))
        self.assertFalse(dp.verify_owner(self.second))



if __name__ == '__main__':
    unittest.main()
