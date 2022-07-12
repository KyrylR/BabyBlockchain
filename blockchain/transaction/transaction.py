"""
Замечания и предложения:
В случае если не обеспечивать контроль дублирования транзакции валидаторы могут не распознать что необходимая транзакция
была уже добавлена в историю. Для этого можно использовать значение nonce, которое влияет на формирование идентификатора
транзакции (хеш-значение от всех данных транзакции).
"""
from dataclasses import dataclass, field
from typing import Optional, List

from hash_lib.Keccak import Keccak

from operation import Operation


@dataclass
class Transaction:
    # unique transaction ID (hash value from all other transaction fields).
    transaction_id: Optional[int] = field(default=None)

    # set of payment transactions validated in this transaction.
    set_of_operations: Optional[List[Operation]] = field(default=None)

    # value to protect duplicate transactions with the same transactions.
    nonce: int = field(default=0)

    def __post_init__(self):
        self.transaction_id = Keccak().update(self.__repr__().encode())

    @staticmethod
    def crete_transaction(transactions: List[Operation], nonce: int) -> "Transaction":
        """
        The function allows to create a transaction with all necessary details.
        It takes a list of transactions and nonce as input.
        :return: Transaction object.
        """
        return Transaction(set_of_operations=transactions, nonce=nonce)
