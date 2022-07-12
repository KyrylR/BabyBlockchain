from dataclasses import dataclass, field
from typing import Optional, List

from blockchain.transaction.transaction import Transaction


@dataclass
class Block:
    # Unique block ID (hash value from all other data).
    block_id: Optional[str] = field(default=None)

    # identifier of the preceding block (needed to ensure the integrity of the story).
    prev_hash: Optional[str] = field(default=None)

    # List of transactions validated in this block.
    set_of_transactions: Optional[List[Transaction]] = field(default=None)

    @staticmethod
    def create_block(block_id: str, prev_hash: str, set_of_transactions: List[Transaction]) -> "Block":
        """
        The function allows to create a block with all the necessary details. Accepts a list of transactions and
        the previous block's identifier as input.

        :return: Block object.
        """
        return Block(block_id=block_id, prev_hash=prev_hash, set_of_transactions=set_of_transactions)
