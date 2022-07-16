from dataclasses import dataclass, field
from typing import Optional, List

from blockchain.account import Account
from blockchain.block import Block
from blockchain.hash import Hash
from blockchain.transaction.transaction import Transaction

"""
This is the first attempt to use blockchain. 
We will have to do a lot of optimizations in the future for better performance!
"""


@dataclass
class Blockchain:
    # A table showing the current state of balances in the system.
    # The account ID is used as the key, the user balance as the value. (to do)
    coin_database: Optional[List[Account]] = field(default=None)

    # An array containing all blocks added to the history.
    block_history: Optional[List[Block]] = field(default=None)

    # An array storing all the transactions in the history.
    # This will be used for quicker access when checking the
    # existence of a transaction in the history (duplicate protection).
    tx_database: Optional[List[Transaction]] = field(default=None)

    # An integer value defining the number of coins available in the tap for testing.
    faucetCoins: int = field(default=100)

    def __post_init__(self):
        self.__init_blockchain()

    def __init_blockchain(self) -> None:
        """
        A function to initialize the blockchain.
        Under the bonnet, the genesis block is created and added to the history.
        :return:
        """
        creators = Account()
        genesis_block = Block()

    def get_lat_block(self) -> Optional[Block]:
        if self.block_history is not None:
            return self.block_history[-1]
        return None

    def get_token_from_faucet(self) -> None:
        """
        A function to retrieve test coins from the tap.
        Updates the coinDatabase and balance of the account that called the method.
        :return:
        """
        pass

    @staticmethod
    def validate_block() -> bool:
        """
        Helps to validate the block and add it to the history.
        :return:
        """

        """
        Функция validateBlock должна содержать набор следующих проверок:
        Проверка что блок содержит ссылку на последний актуальный блок в истории;
        Проверка что транзакции в блоке еще не были добавлены в историю;
        Проверка того что блок не содержит конфликтующих транзакций.
        Проверка каждой операции в транзакции:
        Проверка подписи;
        Проверка того что операция платит не больше монет чем хранится на балансе аккаунта отправителя.
        """
        return True

    def get_account_state(self):
        """
        Gets the current state of accounts and balances.
        :return:
        """
        pass


emission_value = 50


def proof_of_work(block: Block, miner: Account) -> Block:
    print(block.__repr__())
    while block.target < block.block_id:
        block.get_new_block_id(Hash.to_sha1)

    block.add_coinbase_transaction(miner, emission_value)
    return block.create_block()
