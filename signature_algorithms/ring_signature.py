import itertools
from random import randint
from typing import Optional

from dataclasses import dataclass, field
from curve import MontgomeryCurve, Point

# Use my own implementation of Keccak
from hash_lib.Keccak.Keccak import Keccak

from key_pair import KeyPairGenerator


@dataclass
class RingSignature:
    """
    curve: Curve that used here is curve25519.
    gen_point: Curve generator point,
    """
    gen_point: Optional[Point] = field(default=None)
    curve: MontgomeryCurve = field(default=MontgomeryCurve())

    def __post_init__(self):
        self.gen_point = self.curve.G

    @staticmethod
    def convert_to_hash_string(lc_msg: str, lc_point: Point):
        """
        :param lc_msg: String.
        :param lc_point: Elliptic curve Point.
        :return: create a string which you hash -> int.
        """
        str2hash = "%s,%d,%d" % (lc_msg, lc_point.x, lc_point.y)

        return int(Keccak().update(str2hash.encode()), 16)

    def sign(self, msg: str, public_keys: list, private_key: int, signer_key_index: int):
        """
        Function that accepts message, arrays of public and private keys and private key index of signer
        and generate
        :param msg: plain text.
        :param public_keys: array of public keys.
        :param private_key: private key.
        :param signer_key_index: index of public key in array.
        :return: signature.
        """
        keys_count = len(public_keys)
        e: list = [0] * keys_count
        ss: list = [0] * keys_count
        z_s: list = [0] * keys_count

        alfa = randint(0, self.curve.n)
        beta = self.curve.mul_point(alfa, self.gen_point)

        # Determine the index pi_plus_1 and calculate the value of e separately
        pi_plus_1 = (signer_key_index + 1) % keys_count
        e[pi_plus_1] = self.convert_to_hash_string(msg, beta)

        for i in itertools.chain(range(signer_key_index + 1, keys_count), range(signer_key_index)):
            if i != signer_key_index:
                # Determine a random value
                ss[i] = randint(0, self.curve.n)
                next_i = (i + 1) % keys_count

                # Two new EC points are created by multiplying ss_i by G and e_i
                z_s[i] = self.curve.add_point(self.curve.mul_point(ss[i], self.gen_point),
                                              self.curve.mul_point(e[i], public_keys[i]))
                e[next_i] = self.convert_to_hash_string(msg, z_s[i])

        # The signer part itself is calculated separately. This is where the private key is used
        ss[signer_key_index] = (alfa - private_key * e[signer_key_index]) % self.curve.n
        return e[0], ss

    def verify(self, msg: str, public_keys: list, e_0, ss) -> bool:
        """
        Check signature: specifies that the 's' values are calculated after the 'e' values,
        so it involves the use of a private key
        :param msg: Plain text.
        :param public_keys: Array of public keys.
        :param e_0: first part of signature.
        :param ss: second part of signature.
        :return: true if signature is valid.
        """
        keys_count = len(public_keys)
        e: list = [0] * keys_count
        e[0] = e_0
        z_s: list = [0] * keys_count

        # Iterate over the array and calculate the z_s_i values used to determine the e's, similar to the signature
        for i in range(keys_count):
            z_s[i] = self.curve.add_point(self.curve.mul_point(ss[i], self.gen_point),
                                          self.curve.mul_point(e[i], public_keys[i]))
            if i < keys_count - 1:
                e[i + 1] = self.convert_to_hash_string(msg, z_s[i])

        to_check = self.convert_to_hash_string(msg, z_s[keys_count - 1])
        return e[0] == to_check


if __name__ == "__main__":
    sign = RingSignature()
    key_pair = KeyPairGenerator()
    public_keys_list = []
    private_keys = []

    for idx in range(4):
        pk, pbk = key_pair.gen_keypair()
        public_keys_list.append(pbk)
        private_keys.append(pk)

    test_index = 2
    message = "This is a ring signature"
    signature = sign.sign(message, public_keys_list, private_keys[test_index], test_index)
    print(sign.verify(message, public_keys_list, *signature))
