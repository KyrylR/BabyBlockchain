"""
Замечания и предложения:
В случае если не обеспечивать контроль дублирования транзакции валидаторы могут не распознать что необходимая транзакция
была уже добавлена в историю. Для этого можно использовать значение nonce, которое влияет на формирование идентификатора
транзакции (хеш-значение от всех данных транзакции).
"""
from dataclasses import dataclass, field
from typing import Optional, List

from hash_lib.Keccak import Keccak

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
    sequence: int = field(default=0)

    def __post_init__(self):
        print(self.__repr__())
        self.transaction_id = Keccak().update(self.__repr__().encode())

    @staticmethod
    def crete_transaction(operations: List[Operation], sequence: int) -> "Transaction":
        """
        The function allows to create a transaction with all necessary details.
        It takes a list of transactions and nonce as input.
        :return: Transaction object.
        """
        if sequence < 0:
            sequence = 0
        elif sequence > 255:
            sequence = 255

        return Transaction(set_of_operations=operations, sequence=sequence)

    @staticmethod
    def crete_coinbase_transaction(miner: Account, amount: int) -> "Transaction":
        """
        The function allows to create a transaction with all necessary details.
        It takes a list of transactions and nonce as input.
        :return: Transaction object.
        """
        op = Operation().create_coinbase_op(miner, amount)
        return Transaction(set_of_operations=[op], sequence=255)

    def verify_transaction(self) -> bool:
        if self.sequence < 0 or \
                self.sequence > 255 or \
                self.transaction_id != Keccak().update(self.__repr__().encode()):
            return False

        for op in self.set_of_operations:
            if not op.verify_operation():
                return False

        return True
