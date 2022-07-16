"""
Замечания и предложения:
В случае если не обеспечивать контроль дублирования транзакции валидаторы могут не распознать что необходимая транзакция
была уже добавлена в историю. Для этого можно использовать значение nonce, которое влияет на формирование идентификатора
транзакции (хеш-значение от всех данных транзакции).
"""
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Optional, List

from hash_lib.SHA1 import SHA1

from blockchain.account import Account
from blockchain.transaction.operation import Operation
from features.utils import performance


@dataclass
class Transaction:
    # unique transaction ID (hash value from all other transaction fields).
    transaction_id: Optional[str] = field(default=None, repr=False)

    # set of payment transactions validated in this transaction.
    set_of_operations: Optional[List[Operation]] = field(default=None)

    # value to protect duplicate transactions with the same transactions.
    # in range [0, 255]
    sequence: int = field(default=0)

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
        self.__initialize_fields([op], 255)
        if self.verify_transaction(True):
            return deepcopy(self)
        return None

    def verify_transaction(self, coinbase: bool = False) -> bool:
        if self.sequence < 0 or \
                self.sequence > 255 or \
                self.transaction_id is None or \
                self.transaction_id != SHA1().update(self.__repr__().encode()):
            return False

        for op in self.set_of_operations:
            if op is None or (not op.verify_operation() and not coinbase):
                return False

        return True
