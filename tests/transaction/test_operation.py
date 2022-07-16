import unittest

from blockchain.account import Account
from blockchain.transaction.operation import Operation


class OperationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        account_gen = Account()
        cls.first = account_gen.get_account()
        cls.second = account_gen.get_account()
        cls.gen = account_gen
        cls.op_gen = Operation()

    def test_payment_operation_gen(self):
        self.first.update_balance(20)
        # Ok operation
        _, correct = self.op_gen.create_payment_operation(self.first, self.second, 5, self.first.wallet[0])
        self.assertTrue(correct)

        # Ok operation to same account
        _, correct = self.op_gen.create_payment_operation(self.first, self.first, 5, self.first.wallet[0])
        self.assertTrue(correct)

        # Balance error
        _, correct = self.op_gen.create_payment_operation(self.first, self.second, 25, self.first.wallet[0])
        self.assertFalse(correct)

        # Invalid keys
        _, correct = self.op_gen.create_payment_operation(self.first, self.second, 25, self.second.wallet[0])
        self.assertFalse(correct)

        # Balance error (10 spent in previous operations)
        _, correct = self.op_gen.create_payment_operation(self.first, self.second, 11, self.first.wallet[0])
        self.assertFalse(correct)

    def test_coinbase_operation(self):
        # Ok operation
        op = self.op_gen.create_coinbase_op(self.first, 10)
        self.assertIsNotNone(op)


if __name__ == '__main__':
    unittest.main()
