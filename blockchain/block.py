from copy import deepcopy
from dataclasses import dataclass, field
from typing import Optional, List, Callable

from blockchain.account import Account
from blockchain.transaction.transaction import Transaction


@dataclass
class Block:
    # Timestamp
    timestamp: Optional[int] = field(init=True)
    # identifier of the preceding block (needed to ensure the integrity of the story).
    prev_hash: Optional[str] = field(init=True)

    # Unique block ID (hash value from all other data).
    block_id: Optional[str] = field(default=None, repr=False)
    # List of transactions validated in this block.
    set_of_transactions: Optional[List[Transaction]] = field(default=None, init=True)
    # Target
    target: str = field(default=0x00ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)
    # Nonce
    nonce: int = field(default=0)

    def __post_init__(self):
        self.set_of_transactions = []

    def create_block(self) -> Optional["Block"]:
        """
        The function allows to create a block with all the necessary details. Accepts a list of transactions and
        the previous block's identifier as input.

        :return: Block object.
        """
        if self.block_id is None:
            return None

        if self.block_id < self.target:
            return deepcopy(self)

        return None

    def get_new_block_id(self, hash_alg: Callable) -> None:
        self.nonce += 1
        print(self.__repr__())
        self.block_id = hash_alg(self.__repr__())

    def add_coinbase_transaction(self, miner: Account, amount: int) -> bool:
        tx = Transaction().crete_coinbase_transaction(miner, amount)
        if tx is None:
            return False
        self.set_of_transactions.append(tx)
        return True

    def add_transaction(self, transaction: Transaction) -> bool:
        addition_need = True
        if transaction is None or not transaction.verify_transaction():
            return False
        if len(self.set_of_transactions) != 0:
            if self.set_of_transactions[-1] == -1:
                return False

        for tx in self.set_of_transactions:
            if transaction.transaction_id == tx.transaction_id:
                if transaction.sequence > tx.sequence:
                    self.set_of_transactions.remove(tx)
                    self.set_of_transactions.append(transaction)
                    addition_need = False
                    continue
                else:
                    return False
            if not tx.verify_transaction():
                return False

        for tx in self.set_of_transactions:
            for new_op in transaction.set_of_operations:
                if new_op in tx.set_of_operations and tx.transaction_id != transaction.transaction_id:
                    return False

        if addition_need is True:
            self.set_of_transactions.insert(1, transaction)
        return True

    def verify_block(self) -> bool:
        seen = set()
        for tx in self.set_of_transactions:
            if tx.sequence == -1:
                continue
            if not tx.verify_transaction():
                return False
            if tx in seen:
                return False
            seen.add(tx)

        if self.target < self.block_id:
            return False

        return True
