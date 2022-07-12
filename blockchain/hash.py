from dataclasses import dataclass
from hash_lib import Keccak, SHA1


@dataclass
class Hash:
    @staticmethod
    def to_sha1(message: str) -> str:
        """
        Produce a hex SHA-1 digest of the input message.

        :param message: plain text
        :return: the final hash value (big-endian) as a hex string
        """
        return SHA1().update(message.encode())

    @staticmethod
    def to_keccak(message: str) -> str:
        """
        Produce a hex Keccak-256 digest of the input message.

        :param message: plain text
        :return: the final hash value (big-endian) as a hex string
        """
        return Keccak().update(message.encode())
