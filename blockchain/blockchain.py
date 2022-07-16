from copy import deepcopy
from dataclasses import dataclass, field
from time import time
from typing import Optional, List, Set, Dict

from blockchain.account import Account
from blockchain.block import Block
from blockchain.hash import Hash
from blockchain.transaction.transaction import Transaction

"""
This is the first attempt to use blockchain. 
We will have to do a lot of optimizations in the future for better performance!
"""

GENESIS_BLOCK_PREV_HASH = '0x00000000000000000000000000000000000000000000'


@dataclass
class Blockchain:
    # A table showing the current state of balances in the system.
    # The account ID is used as the key, the user balance as the value. (to do)
    coin_database: Optional[Dict] = field(default=None)

    # An array containing all blocks added to the history.
    block_history: Optional[List[Block]] = field(default=None)

    # An array storing all the transactions in the history.
    # This will be used for quicker access when checking the
    # existence of a transaction in the history (duplicate protection).
    tx_database: Optional[List[Transaction]] = field(default=None)

    # An integer value defining the number of coins available in the tap for testing.
    faucetCoins: int = field(default=100)

    def __post_init__(self):
        self.coin_database = dict()
        self.block_history = []
        self.tx_database = []
        self.__init_blockchain()

    def __init_blockchain(self) -> None:
        """
        A function to initialize the blockchain.
        Under the bonnet, the genesis block is created and added to the history.
        :return:
        """
        creator = Account().get_account()
        self.coin_database[creator.account_id] = creator.get_balance
        genesis_block = proof_of_work(Block(timestamp=int(time()),
                                            prev_hash=GENESIS_BLOCK_PREV_HASH),
                                      creator)

        self.tx_database.extend(genesis_block.set_of_transactions)
        self.block_history.append(genesis_block)

    def get_lat_block(self) -> Optional[Block]:
        if self.block_history is not None:
            return self.block_history[-1]
        return None

    def get_token_from_faucet(self, account: Account, amount: int) -> bool:
        """
        A function to retrieve test coins from the tap.
        Updates the coinDatabase and balance of the account that called the method.
        :return: true if operation is successful
        """
        if amount > self.faucetCoins:
            return False
        self.faucetCoins -= amount
        account.update_balance(amount)
        return True

    def validate_block(self, block_to_add: Block) -> bool:
        """
        Helps to validate the block and add it to the history.
        :return:
        """

        """
        Функция validateBlock должна содержать набор следующих проверок:
        +Проверка что блок содержит ссылку на последний актуальный блок в истории(validate_block func);
        +Проверка что транзакции в блоке еще не были добавлены в историю(validate_block func);
        +Проверка того что блок не содержит конфликтующих транзакций(verify_block func in Block class).
        +Проверка каждой операции в транзакции(verify_transaction func in Transaction class):
        +Проверка подписи(verify_operation func in Operation class);
        +Проверка того что операция платит не больше монет чем хранится на балансе аккаунта 
        (verify_operation func in Operation class).
        """
        if block_to_add.prev_hash != self.get_lat_block().block_id:
            return False

        for tx in block_to_add.set_of_transactions:
            if tx in self.tx_database:
                return False

        if not block_to_add.verify_block():
            return False

        for tx in block_to_add.set_of_transactions:
            for op in tx.set_of_operations:
                if tx.sequence != -1:
                    self.coin_database[op.sender.account_id] -= op.amount
                self.coin_database[op.receiver.account_id] += op.amount

        self.block_history.append(block_to_add)
        self.tx_database.extend(block_to_add.set_of_transactions)
        return True

    def get_account_state(self) -> Dict:
        """
        Gets the current state of accounts and balances.
        :return: Accounts list.
        """
        return deepcopy(self.coin_database)

    def add_account(self, account: Account) -> None:
        """
        Adds account to coin database
        :return: Nothings.
        """
        self.coin_database[account.account_id] = account.get_balance


emission_value = 50


def proof_of_work(block: Block, miner: Account) -> Block:
    block.add_coinbase_transaction(miner, emission_value)
    block.get_new_block_id(Hash.to_sha1)
    while block.target < int(block.block_id, 16):
        block.get_new_block_id(Hash.to_sha1)
        # print(hex(block.target))
        # print(block.block_id)

    return block.create_block()
