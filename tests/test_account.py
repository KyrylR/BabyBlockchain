import unittest

from blockchain.account import Account


class AccountTestCase(unittest.TestCase):
    def test_unique_accounts(self):
        account_gen = Account()
        first = account_gen.get_account()
        second = account_gen.get_account()
        self.assertNotEqual(first, second)


if __name__ == '__main__':
    unittest.main()
