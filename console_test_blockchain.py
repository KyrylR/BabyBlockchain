import unittest
from time import time

from blockchain.account import Account
from blockchain.block import Block
from blockchain.blockchain import Blockchain, ConsensusAlgorithms
from blockchain.transaction.operation import Operation
from blockchain.transaction.transaction import Transaction


class BlockchainTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        account_gen = Account()
        cls.first = account_gen.get_account()
        cls.second = account_gen.get_account()
        cls.gen = account_gen
        cls.op_gen = Operation()
        cls.tx_gen = Transaction()
        cls.blockchain = Blockchain()

    def test_blockchain(self):
        self.first.update_balance(20)
        print(f"{'Account 1:':15} {self.first.print_balance()}", end='\n')
        self.second.update_balance(13)
        print(f"{'Account 2:':15} {self.second.print_balance()}", end='\n')

        self.blockchain.add_account(self.first)
        print(f"{'Coin database:':15} {self.blockchain.coin_database}", end='\n')
        self.blockchain.add_account(self.second)
        print(f"{'Coin database:':15} {self.blockchain.coin_database}", end='\n')

        g_block = self.blockchain.get_lat_block()
        self.assertIsNotNone(g_block)

        # Ok operations
        op1, _ = self.op_gen.create_payment_operation(self.first, self.second, 5, self.first.wallet[0])
        # first: 15, second: 13 (confirmed: f: 15, s: 18)
        op2, _ = self.op_gen.create_payment_operation(self.first, self.second, 8, self.first.wallet[0])
        # first: 7, second: 13 (confirmed: f: 7, s: 26)
        op3, _ = self.op_gen.create_payment_operation(self.second, self.second, 8, self.second.wallet[0])
        # first: 7, second: 5 (confirmed: f: 7, s: 26)

        # Ok transactions
        tx1 = self.tx_gen.crete_transaction([op1, op2], 255)
        print(f"{'Transaction:':15} {tx1.to_text_tx()}", end='\n')
        tx2 = self.tx_gen.crete_transaction([op3], 120)
        print(f"{'Transaction:':15} {tx2.to_text_tx()}", end='\n')

        block1 = Block(int(time()), g_block.block_id)
        block1.add_transaction(tx1)
        block1.add_transaction(tx2)
        block1 = ConsensusAlgorithms(50).proof_of_work(block1, self.first)
        print(f"{'Block 1:':15} {block1.to_text_block()}", end='\n')
        # first: 7, second: 5 (confirmed: f: 57, s: 26)
        self.assertTrue(self.blockchain.validate_block(block1))
        print(f"{'Block history:':15} {self.blockchain.get_block_history()}", end='\n')

        self.first.sync_balance(self.blockchain.coin_database)
        self.second.sync_balance(self.blockchain.coin_database)
        self.assertEqual(self.first.get_balance, 57)
        self.assertEqual(self.second.get_balance, 26)
        print(f"{'Coin database:':15} {self.blockchain.coin_database}", end='\n')

        tx1.update_time()
        tx2.update_time()

        block2 = Block(int(time()), block1.block_id)
        self.assertTrue(block2.add_transaction(tx1))
        self.assertTrue(block2.add_transaction(tx2))
        block2 = ConsensusAlgorithms(50).proof_of_work(block2, self.first)
        print(f"{'Block 2:':15} {block2.to_text_block()}", end='\n')
        self.assertTrue(self.blockchain.validate_block(block2))
        print(f"{'Block history:':15} {self.blockchain.get_block_history()}", end='\n')
        self.first.sync_balance(self.blockchain.coin_database)
        self.second.sync_balance(self.blockchain.coin_database)
        self.assertEqual(self.first.get_balance, 94)  # first: 57 - 13 + 50
        self.assertEqual(self.second.get_balance, 39)  # second: 26 + 13
        print(f"{'Coin database:':15} {self.blockchain.coin_database}", end='\n')


if __name__ == '__main__':
    unittest.main()
