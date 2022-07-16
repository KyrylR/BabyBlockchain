import unittest

from blockchain.account import Account
from blockchain.transaction.operation import Operation
from blockchain.transaction.transaction import Transaction


class TransactionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        account_gen = Account()
        cls.first = account_gen.get_account()
        cls.second = account_gen.get_account()
        cls.gen = account_gen
        cls.op_gen = Operation()
        cls.tx_gen = Transaction()

    def test_payment_transactions(self):
        self.first.update_balance(20)
        self.second.update_balance(13)
        # Ok operations
        op1, _ = self.op_gen.create_payment_operation(self.first, self.second, 5, self.first.wallet[0])
        # first: 15, second: 13
        op2, _ = self.op_gen.create_payment_operation(self.first, self.second, 8, self.first.wallet[0])
        # first: 7, second: 13
        op3, _ = self.op_gen.create_payment_operation(self.second, self.second, 8, self.first.wallet[0])
        # first: 7, second: 5
        # bad operation
        op4, _ = self.op_gen.create_payment_operation(self.second, self.first, 8, self.first.wallet[0])
        # first: 7, second: 5

        # Ok transaction
        self.assertIsNotNone(self.tx_gen.crete_transaction([op1, op2, op3], 255))

        # Bad sequence
        self.assertIsNone(self.tx_gen.crete_transaction([op1, op2, op3], 300))

        # With bad operation
        self.assertIsNone(self.tx_gen.crete_transaction([op1, op2, op3, op4], 120))

    def test_coinbase_transactions(self):
        # Ok coinbase transaction
        self.assertIsNotNone(self.tx_gen.crete_coinbase_transaction(self.first, 10))


if __name__ == '__main__':
    unittest.main()
