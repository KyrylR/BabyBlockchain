import unittest
from time import time

from blockchain.account import Account
from blockchain.block import Block
from blockchain.transaction.operation import Operation
from blockchain.transaction.transaction import Transaction


class BlockTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        account_gen = Account()
        cls.first = account_gen.get_account()
        cls.second = account_gen.get_account()
        cls.gen = account_gen
        cls.op_gen = Operation()
        cls.tx_gen = Transaction()
        cls.bl_gen = Block(timestamp=int(time()),
                           prev_hash='0x0000000000000000000000000000000000000000000000000000000000000000')

    def test_add_txs_to_block(self):
        self.first.update_balance(20)
        self.second.update_balance(13)
        # Ok operations
        op1, _ = self.op_gen.create_payment_operation(self.first, self.second, 5, self.first.wallet[0])
        # first: 15, second: 13
        op2, _ = self.op_gen.create_payment_operation(self.first, self.second, 8, self.first.wallet[0])
        # first: 7, second: 13
        op3, _ = self.op_gen.create_payment_operation(self.second, self.second, 8, self.second.wallet[0])
        # first: 7, second: 5
        # bad operation
        op4, _ = self.op_gen.create_payment_operation(self.second, self.first, 8, self.first.wallet[0])
        # first: 7, second: 5

        # Ok transactions
        tx1 = self.tx_gen.crete_transaction([op1, op2], 255)
        tx2 = self.tx_gen.crete_transaction([op3], 120)

        # Add normal tx
        self.assertTrue(self.bl_gen.add_transaction(tx1))
        # Add normal tx
        self.assertTrue(self.bl_gen.add_transaction(tx2))
        # Add duplicate tx
        self.assertFalse(self.bl_gen.add_transaction(tx1))

        tx2_1 = self.tx_gen.crete_transaction([op1, op2], 12)
        tx2_2 = self.tx_gen.crete_transaction([op3], 121)
        # Add duplicate tx with less sequence
        self.assertFalse(self.bl_gen.add_transaction(tx2_1))
        # Add duplicate tx with greater sequence
        self.assertTrue(self.bl_gen.add_transaction(tx2_2))
        # Check if more important tx replace other tx
        self.assertEqual(len(self.bl_gen.set_of_transactions), 2)
        self.assertEqual(self.bl_gen.set_of_transactions[1], tx2_2)

        # Bad transaction
        tx3 = self.tx_gen.crete_transaction([op3, op4], 120)
        tx4 = self.tx_gen.crete_transaction([op2, op3], 120)
        # Add tx with bad op
        self.assertFalse(self.bl_gen.add_transaction(tx3))
        # Add tx with duplicate op
        self.assertFalse(self.bl_gen.add_transaction(tx4))

    def test_add_coinbase_txs_to_block(self):
        # Ok coinbase transaction
        self.assertTrue(self.bl_gen.add_coinbase_transaction(self.first, 10))

        # Ok operations
        op1, _ = self.op_gen.create_payment_operation(self.first, self.second, 5, self.first.wallet[0])
        # first: 15, second: 13
        op2, _ = self.op_gen.create_payment_operation(self.first, self.second, 8, self.first.wallet[0])
        # first: 7, second: 13
        op3, _ = self.op_gen.create_payment_operation(self.second, self.second, 8, self.first.wallet[0])
        # first: 7, second: 5

        # Ok transactions
        tx1 = self.tx_gen.crete_transaction([op1, op2], 255)
        tx2 = self.tx_gen.crete_transaction([op3], 120)

        # Add normal tx, but it's forbidden to add transactions after coinbase
        self.assertFalse(self.bl_gen.add_transaction(tx1))
        # Add normal tx, but it's forbidden to add transactions after coinbase
        self.assertFalse(self.bl_gen.add_transaction(tx2))


if __name__ == '__main__':
    unittest.main()
