from copy import deepcopy

from blockchain.block import Block
from blockchain.hash import Hash


def proof_of_work(block: Block) -> Block:
    print(block.__repr__())
    while block.target < block.block_id:
        block.get_new_block_id(Hash.to_sha1)

    return block.create_block()
