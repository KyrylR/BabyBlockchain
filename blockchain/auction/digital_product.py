from dataclasses import dataclass, field
from typing import Optional, Tuple

from blockchain.account import Account
from signature_algorithms.ecdsa_signature import ECDSA


@dataclass
class DigitalProduct:
    # Some string data
    __data: Optional[str] = field(default=None)

    signature: Optional[Tuple[int, int]] = field(default=None)

    @property
    def get_data(self):
        """
        Get digital data.
        :return: data.
        """
        return self.__data

    def become_owner(self, account: Account) -> bool:
        self.signature, ok = account.sign_data(account.wallet[0].private_key, self.get_data)
        return ok

    def verify_owner(self, account: Account) -> bool:
        for pair in account.wallet:
            if ECDSA().verify(pair.public_key, self.get_data, *self.signature):
                return True
        return False
