import unittest

from blockchain.account import Account
from signature_algorithms.key_pair import KeyPair


class AccountTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        account_gen = Account()
        cls.first = account_gen.get_account()
        cls.second = account_gen.get_account()
        cls.gen = account_gen

    def test_unique_accounts(self):
        self.assertNotEqual(self.first, self.second)

    def test_signing_data_with_new_keys(self):
        new_key_pair = KeyPair()
        self.first.add_key_pair_to_wallet(new_key_pair)

        data = "Some data"
        sig, correct = self.first.sign_data(new_key_pair.private_key, data)
        self.assertTrue(correct)

        correct = self.first.verify_data(data, sig)
        self.assertTrue(correct)

        correct = self.second.verify_data(data, sig)
        self.assertFalse(correct)

    def test_update_balance(self):
        self.assertTrue(self.first.update_balance(10))
        self.assertFalse(self.first.update_balance(-20))
        self.assertTrue(self.first.update_balance(-2))


if __name__ == '__main__':
    unittest.main()
