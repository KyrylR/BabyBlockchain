import unittest
from time import time


from blockchain.account import Account
from blockchain.auction.auction import Auction
from blockchain.block import Block
from blockchain.blockchain import Blockchain, ConsensusAlgorithms
from blockchain.transaction.operation import Operation
from blockchain.transaction.transaction import Transaction


class AuctionTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        account_gen = Account()
        cls.first = account_gen.get_account()
        cls.second = account_gen.get_account()
        cls.third = account_gen.get_account()
        cls.gen = account_gen
        cls.op_gen = Operation()
        cls.tx_gen = Transaction()
        cls.blockchain = Blockchain()

    def test_auction(self):
        # Registration only for test purposes!
        # Registrate first
        self.first.update_balance(20)
        self.blockchain.add_account(self.first)

        # Registrate second
        self.second.update_balance(13)
        self.blockchain.add_account(self.second)

        # Registrate third
        self.third.update_balance(32)
        self.blockchain.add_account(self.third)

        g_block = self.blockchain.get_lat_block()
        self.assertIsNotNone(g_block)

        self.auction = Auction(beneficiary=self.first, auction_end_time=100, blockchain=self.blockchain)
        self.assertFalse(self.auction.ended)

        # Ok operations
        op1, _ = self.op_gen.create_payment_operation(self.second, self.first, 5, self.second.wallet[0])
        op2, _ = self.op_gen.create_payment_operation(self.third, self.first, 8, self.third.wallet[0])
        op3, _ = self.op_gen.create_payment_operation(self.second, self.first, 4, self.second.wallet[0])
        op4, _ = self.op_gen.create_payment_operation(self.third, self.first, 1, self.third.wallet[0])
        op5, _ = self.op_gen.create_payment_operation(self.third, self.first, 2, self.third.wallet[0])
        op6, _ = self.op_gen.create_payment_operation(self.second, self.first, 1, self.second.wallet[0])

        # Execute op1
        block, tx = self.execute_operation(op1)
        self.assertTrue(self.auction.bid(self.second, block, tx))
        self.first.sync_balance(self.blockchain.coin_database)
        self.second.sync_balance(self.blockchain.coin_database)
        # Tests after operation
        self.assertEqual(self.auction.highest_bidder, self.second)
        self.assertEqual(self.auction.highest_bid, 5)

        # Execute op2
        block, tx = self.execute_operation(op2)
        self.assertTrue(self.auction.bid(self.third, block, tx))
        self.first.sync_balance(self.blockchain.coin_database)
        self.third.sync_balance(self.blockchain.coin_database)
        # Tests after operation
        self.assertEqual(self.auction.highest_bidder, self.third)
        self.assertEqual(self.auction.highest_bid, 8)

        # Execute op3
        block, tx = self.execute_operation(op3)
        self.assertTrue(self.auction.bid(self.second, block, tx))
        self.first.sync_balance(self.blockchain.coin_database)
        self.second.sync_balance(self.blockchain.coin_database)
        # Tests after operation
        self.assertEqual(self.auction.highest_bidder, self.second)
        self.assertEqual(self.auction.highest_bid, 9)

        # Execute op4
        block, tx = self.execute_operation(op4)
        self.assertFalse(self.auction.bid(self.third, block, tx))
        self.first.sync_balance(self.blockchain.coin_database)
        self.third.sync_balance(self.blockchain.coin_database)
        # Tests after operation
        self.assertEqual(self.auction.highest_bidder, self.second)
        self.assertEqual(self.auction.highest_bid, 9)

        # Execute op5
        block, tx = self.execute_operation(op5)
        self.assertTrue(self.auction.bid(self.third, block, tx))
        self.first.sync_balance(self.blockchain.coin_database)
        self.third.sync_balance(self.blockchain.coin_database)
        # Tests after operation
        self.assertEqual(self.auction.highest_bidder, self.third)
        self.assertEqual(self.auction.highest_bid, 11)

        # Execute op6
        self.auction.ended = True
        self.auction.auction_end()
        self.first.sync_balance(self.blockchain.coin_database)
        self.second.sync_balance(self.blockchain.coin_database)

        block, tx = self.execute_operation(op6)
        self.assertFalse(self.auction.bid(self.second, block, tx))
        self.first.sync_balance(self.blockchain.coin_database)
        self.second.sync_balance(self.blockchain.coin_database)
        # Tests after operation
        self.assertEqual(self.auction.highest_bidder, self.third)
        self.assertEqual(self.auction.highest_bid, 11)

        self.first.sync_balance(self.blockchain.coin_database)
        self.assertEqual(self.first.get_balance, 31)

        self.second.sync_balance(self.blockchain.coin_database)
        self.assertEqual(self.second.get_balance, 13)

        self.third.sync_balance(self.blockchain.coin_database)
        self.assertEqual(self.third.get_balance, 21)

    def execute_operation(self, operation: Operation):
        tx = self.tx_gen.crete_transaction([operation], 255)
        tx.update_time()
        block = Block(int(time()), self.blockchain.get_lat_block().block_id)
        block.add_transaction(tx)
        block = ConsensusAlgorithms(0).proof_of_work(block, self.first)
        self.assertTrue(self.blockchain.validate_block(block))
        return block, tx


if __name__ == '__main__':
    unittest.main()
