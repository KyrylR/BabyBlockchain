from dataclasses import dataclass, field
import time
from typing import Optional, List, Tuple

from blockchain.account import Account
from blockchain.block import Block
from blockchain.blockchain import Blockchain, proof_of_work
from blockchain.transaction.operation import Operation
from blockchain.transaction.transaction import Transaction


@dataclass
class Auction:
    # Blockchain
    blockchain: Blockchain
    # Params of the Auction
    beneficiary: Account
    # The auction starts when the auction transaction is confirmed in the block
    auction_end_time: int

    # Current state of Auction
    highest_bidder: Optional[Account] = field(default=None)
    highest_bid: Optional[int] = field(default=None)
    ended: bool = field(default=None)

    pending_returns: Optional[List[Operation]] = field(default=None)

    def __post_init__(self):
        self.pending_returns = []
        block = self.__build_block(self.beneficiary, 0)
        if block is None:
            print('Something went wrong try again later!')
            self.ended = True
            return
        block = proof_of_work(block, self.beneficiary)
        self.blockchain.validate_block(block)
        self.auction_end_time += int(block.timestamp)
        print(f"Auction has started! Time left: {time.strftime('%H:%M:%S', time.gmtime(self.get_time_left()))}")

    def get_time_left(self):
        if not self.ended:
            return self.auction_end_time - int(time.time())
        return 0

    def bid(self, account: Account, block: Block, transaction: Transaction) -> bool:
        self.beneficiary.sync_balance(self.blockchain.coin_database)
        correct, amount = self.verify_bid(account, block, transaction)
        if not correct:
            print("The data is incorrect!")
            return False

        if block.timestamp > self.auction_end_time or self.ended:
            print("The auction has already ended!")
            self.__send_money_back(account=account, amount=amount)
            if not self.ended:
                self.auction_end()
            return False

        if amount <= self.highest_bid:
            print("There is already a higher or equal bid")
            self.__add_to_pending_returns(account, amount)
            return False

        if self.highest_bid != 0:
            self.__add_to_pending_returns(account, amount)
            return False

        self.highest_bid = amount
        self.highest_bidder = account
        return True

    def verify_bid(self, account: Account, block: Block, transaction: Transaction) -> Tuple[bool, int]:
        if block not in self.blockchain.block_history or \
                transaction not in self.blockchain.tx_database or \
                account not in self.blockchain.coin_database:
            return False, 0

        amount = 0
        for operation in transaction.set_of_operations:
            if operation.receiver == self.beneficiary and operation.verify_operation():
                amount += operation.amount
        if amount == 0:
            return False, 0

        return True, amount

    def __add_to_pending_returns(self, account: Account, amount: int):
        op, _ = Operation().create_payment_operation(self.beneficiary,
                                                     account,
                                                     amount,
                                                     self.beneficiary.wallet[0])
        self.pending_returns.append(op)

    def __send_money_back(self, account: Account, amount: int) -> None:
        block = self.__build_block(account, amount)
        if block is None:
            print('Something went wrong try again later!')
            return
        block = proof_of_work(block, self.beneficiary)
        self.blockchain.validate_block(block)

    def __build_block(self,
                      receiver: Optional[Account] = None,
                      amount: int = -1,
                      operations: Optional[List[Operation]] = None) -> Optional[Block]:
        tx: Optional[Transaction] = None
        if amount != -1:
            op, _ = Operation().create_payment_operation(self.beneficiary,
                                                         receiver,
                                                         amount,
                                                         self.beneficiary.wallet[0])
            tx = Transaction().crete_transaction([op], 255)
        elif operations is not None:
            tx = Transaction().crete_transaction(operations, 255)
        else:
            return None

        if tx is not None:
            block = Block(int(time.time()), self.blockchain.get_lat_block().block_id)
            block.add_transaction(tx)
            return block
        return None

    def auction_end(self):
        self.ended = True
        block = self.__build_block(operations=self.pending_returns)
        block = proof_of_work(block, self.beneficiary)
        self.blockchain.validate_block(block)
        print(f"Winner account: {self.highest_bidder.account_id}\n"
              f"Winner paid: {self.highest_bid}")
