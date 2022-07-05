from dataclasses import dataclass, field
from pprint import pprint
from typing import List, Optional

from signature_algorithms.key_pair import KeyPair


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

    def get_account(self) -> "Account":
        """
        The function allows the creation of an account. Returns an object of
        class Account. Under the bonnet, the first key pair is generated and
        assigned to the account.
        :return:
        """
        pass

    def add_key_pair_to_wallet(self, key_pair: KeyPair) -> None:
        """
        A function that allows you to add a new key pair to a wallet and use it to sign transactions
        initiated from that account in the future. Doesn't return anything.
        :return: None
        """
        pass

    def update_balance(self, value: int) -> None:
        """
        This function allows to update the user's balance.
        It takes an integer value as input, returns nothing.
        :return: None
        """
        pass

    def create_payment_operation(self):
        """
        A function that allows to create a payment transaction on behalf of this account for the recipient.
        It accepts the account object to which the payment will be made, the amount of the
        transfer and the wallet's key index.
        :return:
        """
        pass

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

    def sign_data(self, message: str, keys_index: int):
        """
        A function which allows the user to sign arbitrary data.
        It takes a message and a wallet key pair index as input.
        :return: value for the signature
        """
        pass

    def print(self) -> None:
        """
        A function to print the keypair objects.
        :return: None
        """
        pprint(self.wallet)
