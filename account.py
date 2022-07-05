from copy import deepcopy
from dataclasses import dataclass, field
from pprint import pprint
from random import randint
from typing import List, Optional

from signature_algorithms.key_pair import KeyPair
from hash_lib.Keccak.Keccak import Keccak

from signature_algorithms.ring_signature import RingSignature


@dataclass
class Account:
    """
    account_id: a unique value intended to identify the account within the system.
    Just hash value of initial wallet.
    """
    account_id: Optional[str] = field(default=None)
    wallet: Optional[List[KeyPair]] = field(default=None)
    balance: Optional[int] = field(default=0)

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

    def update_balance(self, value: int) -> None:
        """
        This function allows to update the user's balance.
        It takes an integer value as input.
        :return: None
        """
        if self.balance + value >= 0:
            # TODO, verify that everything is correct!
            self.balance += value

    def create_payment_operation(self, other_account: "Account", value: int, wallet_key_index: int):
        """
        A function that allows to create a payment transaction on behalf of this account for the recipient.
        It accepts the account object to which the payment will be made, the amount of the
        transfer and the wallet's key index.
        :return: true if everything is fine.
        """
        if value <= 0 or value > self.balance:
            return False
        # TODO, make it through transactions
        other_account.update_balance(value)
        self.sign_data("Dummy!", wallet_key_index)
        return True

    @property
    def get_balance(self) -> int:
        """
        A function to get the user's balance.
        :return: integer value of balance.
        """
        return self.balance

    def print_balance(self) -> None:
        """
        Prints the user's balance.
        :return: None.
        """
        pprint(f"Balance: {self.balance} for account: {self.account_id}")

    def sign_data(self, message: str, public_keys: list, keys_index: int):
        """
        A function which allows the user to sign arbitrary data.
        It takes a message and a wallet key pair index as input.
        :return: value for the signature
        """
        key_idx = randint(0, len(public_keys))
        return RingSignature().sign(message, public_keys, self.wallet[keys_index].private_key, key_idx)

    def print(self) -> None:
        """
        A function to print the keypair objects.
        :return: None
        """
        pprint(self.wallet)
