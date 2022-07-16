from copy import deepcopy
from dataclasses import dataclass, field
from typing import Optional, List, Callable

from blockchain.account import Account
from blockchain.transaction.transaction import Transaction


@dataclass
class Block:
    # Unique block ID (hash value from all other data).
    block_id: Optional[str] = field(default=None, repr=False)

    # identifier of the preceding block (needed to ensure the integrity of the story).
    prev_hash: Optional[str] = field(default=None, init=True)

    # List of transactions validated in this block.
    set_of_transactions: Optional[List[Transaction]] = field(default=None, init=True)

    # Timestamp
    timestamp: Optional[int] = field(default=None, init=True)

    # Target
    target: str = field(default=0x00ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)

    # Nonce
    nonce: int = field(default=0)

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

    def add_coinbase_transaction(self, miner: Account, amount: int) -> None:
        tx = Transaction().crete_coinbase_transaction(miner, amount)
        self.set_of_transactions.append(tx)


    def verify_block(self) -> bool:
        seen = set()
        for tx in self.set_of_transactions:
            if not tx.verify_transaction():
                return False
            if tx in seen:
                return False
            seen.add(tx)

        if self.target < self.block_id:
            return False

        return True
