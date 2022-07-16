"""
Замечания и предложения:
В случае если не обеспечивать контроль дублирования транзакции валидаторы могут не распознать что необходимая транзакция
была уже добавлена в историю. Для этого можно использовать значение nonce, которое влияет на формирование идентификатора
транзакции (хеш-значение от всех данных транзакции).
"""
from copy import deepcopy
from dataclasses import dataclass, field
from time import time
from typing import Optional, List

from hash_lib.SHA1 import SHA1

from blockchain.account import Account
from blockchain.transaction.operation import Operation


@dataclass
class Transaction:
    # unique transaction ID (hash value from all other transaction fields).
    transaction_id: Optional[str] = field(default=None, repr=False)

    # set of payment transactions validated in this transaction.
    set_of_operations: Optional[List[Operation]] = field(default=None)

    # value to protect duplicate transactions with the same transactions.
    # in range [0, 255]
    sequence: int = field(default=0, repr=False)

    # Timestamp
    __timestamp: Optional[int] = field(default=int(time()))

    # @performance
    def __initialize_fields(self, operations: List[Operation], sequence: int):
        self.set_of_operations = operations
        self.sequence = sequence
        self.transaction_id = SHA1().update(self.__repr__().encode())

    def crete_transaction(self, operations: List[Operation], sequence: int) -> Optional["Transaction"]:
        """
        The function allows to create a transaction with all necessary details.
        It takes a list of transactions and nonce as input.
        :return: Transaction object.
        """
        self.__initialize_fields(operations, sequence)
        if self.verify_transaction():
            return deepcopy(self)
        return None

    def crete_coinbase_transaction(self, miner: Account, amount: int) -> Optional["Transaction"]:
        """
        The function allows to create a transaction with all necessary details.
        It takes a list of transactions and nonce as input.
        :return: Transaction object.
        """
        op = Operation().create_coinbase_op(miner, amount)
        self.__initialize_fields([op], -1)
        if self.verify_transaction(True):
            return deepcopy(self)
        return None

    def verify_transaction(self, coinbase: bool = False) -> bool:
        if (self.sequence < 0 and not coinbase) or \
                self.sequence > 255 or \
                self.transaction_id is None or \
                self.transaction_id != SHA1().update(self.__repr__().encode()):
            return False

        for op in self.set_of_operations:
            if op is None or (not op.verify_operation() and not coinbase):
                return False

        return True

    def update_time(self):
        self.__timestamp = int(time())
        self.transaction_id = SHA1().update(self.__repr__().encode())

    def __hash__(self):
        return int(SHA1().update(self.__repr__().encode()), 16)

    def to_text_tx(self):
        return f"{'Transaction id:':15} {self.transaction_id}\n" + \
               f"{'Timestamp:':15} {self.__timestamp}\n" + \
               f"{'Sequence:':15} {self.sequence}]\n"