from ecc.curve import Curve25519
from ecc.key import gen_keypair


class KeyPair:
    __slots__ = ['private_key', 'public_key']

    def __init__(self):
        self.private_key, self.public_key = gen_keypair(Curve25519)

    def get_key_pair(self):
        return self.private_key, self.public_key

    def print_key_pair(self):
        print(f"Private key: {self.private_key}\n"
              f"Public key: {self.public_key}")
