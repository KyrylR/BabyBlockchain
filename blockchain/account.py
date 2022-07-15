from copy import deepcopy
from dataclasses import dataclass, field
from pprint import pprint
from random import randint
from typing import List, Optional, Tuple

from blockchain.transaction.operation import Operation
from features.utils import get_transaction_message as tx_msg
from signature_algorithms.ecdsa_signature import ECDSA
from signature_algorithms.key_pair import KeyPair
from hash_lib.Keccak.Keccak import Keccak


@dataclass
class Account:
    # A unique value intended to identify the account within the system.
    # Just hash value of initial wallet.
    account_id: Optional[str] = field(default=None)
    wallet: Optional[List[KeyPair]] = field(default=None)
    __balance: Optional[int] = field(default=0)

    def __str__(self):
        return self.account_id

    def __eq__(self, other):
        return self.account_id == other.account_id

    @staticmethod
    def get_account() -> "Account":
        """
        The function allows the creation of an account. Under the bonnet, the first key pair is generated and
        assigned to the account.
        :return: object of class Account.
        """
        acc = Account()
        acc.wallet.append(KeyPair())
        acc.wallet.append(KeyPair())
        print(str(acc.wallet))
        acc.account_id = Keccak().update(str(acc.wallet).encode())
        return deepcopy(acc)

    def add_key_pair_to_wallet(self, key_pair: KeyPair) -> None:
        """
        A function that allows you to add a new key pair to a wallet and use it to sign transactions
        initiated from that account in the future.
        :return: None
        """
        self.wallet.append(key_pair)

    def update_balance(self, value: int) -> bool:
        """
        This function allows to update the user's balance.
        It takes an integer value as input.
        :return: true if everything is fine.
        """
        if self.__balance + value >= 0:
            self.__balance += value
            return True

        return False

    def create_payment_operation(self,
                                 other_account: "Account",
                                 amount: int,
                                 private_key: int) -> Tuple[Optional[Operation], bool]:
        """
        A function that allows to create a payment transaction on behalf of this account for the recipient.
        It accepts the account object to which the payment will be made, the amount of the
        transfer and the wallet's key index.
        :return: true if everything is fine and Operation itseld
        """
        if amount <= 0 or amount > self.__balance:
            return None, False

        signature, correct = self.__sign_data(private_key, tx_msg(self, other_account, amount))
        if correct is False:
            return None, False

        op, correct = Operation().create_operation(self, other_account, amount, signature)
        if correct is True:
            return op, True
        else:
            return None, False

    def __sign_data(self, private_key: int, message: str) -> Tuple[Optional[Tuple[int, int]], bool]:
        """
        A function which allows the user to sign arbitrary data.
        It takes a message and a wallet key pair index as input.
        :return: value for the signature
        """
        for pair in self.wallet:
            if private_key == pair.private_key:
                return ECDSA().sign(private_key, message), True
        return None, False

    @property
    def get_balance(self) -> int:
        """
        A function to get the user's balance.
        :return: integer value of balance.
        """
        return self.__balance

    def print(self) -> None:
        """
        A function to print the keypair objects.
        :return: None
        """
        pprint(self.wallet)

    def print_balance(self) -> None:
        """
        Prints the user's balance.
        :return: None.
        """
        pprint(f"Balance: {self.__balance} for account: {self.account_id}")
