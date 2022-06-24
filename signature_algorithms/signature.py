import hashlib
import itertools as it
import random
import secrets
from pprint import pprint
from typing import Union

from ecpy.curves import Curve
from ecpy.eddsa import EDDSA
from ecpy.keys import ECPrivateKey
from hash_lib.Keccak.Keccak import Keccak

from signature_algorithms.key_pair import KeyPair


class Signature:
    __slots__ = ['curve', 'G']

    def __init__(self):
        """
        I use Ed-25519 curve during the program ( also in Monero )
        I have plotted the equation and characteristics of the curve
        The G -generator point will be used later
        """
        self.curve = Curve.get_curve('Ed25519')
        self.G = self.curve.generator
        pprint(f"Name: {self.curve.name}, "
               f"Equation: -x^2 + y^2 = 1 -121665/121666 * x^2*y^2 (mod p) "
               f"Type: {self.curve.type}")
        pprint(f"Size: {self.curve.size}, a={self.curve.a}, d={self.curve.d}")
        pprint(f"G={self.curve.generator}, field={self.curve.field}, order={self.curve.order}\n")

    @staticmethod
    def hash_function(_message, _p1: Union[int, list[int]]):
        """
        :param _message: String.
        :param _p1: Elliptic curve Point.
        :return: create a string which you hash -> int.
        """
        str2hash = "%s,%d,%d" % (_message, _p1.x, _p1.y)

        return int(Keccak().get_hash(str2hash.encode()), 16)

    def sign(self, _curve, _message, _public_keys, _private_key, _key_index):
        """
        The ring_sign method is used to create the signature
        :param _curve: Elliptic curve.
        :param _message: String.
        :param _public_keys: Array of public keys.
        :param _private_key: Array of private keys.
        :param _key_index: who is the signer
        :return:
        """
        # key_count - how many people are in the ring
        key_count = len(_public_keys)
        e = [0] * key_count
        ss = [0] * key_count
        z_s = [0] * key_count

        # ---- First step ----
        # Alpha is chosen randomly, up to the order of the curve
        alfa = random.randint(0, _curve.order)

        # Calculate Q (which works as a public key), which is alpha*G (curve.mul_point - multiplication(scalar, Point))
        Q = _curve.mul_point(alfa, self.G)

        # Determine the index pi_plus_1 and calculate the value of e separately
        pi_plus_1 = (_key_index + 1) % key_count
        e[pi_plus_1] = self.hash_function(_message, Q)

        # ---- Step two ----
        # We go through the array so that i != key_index, so we count on the other members of the ring
        for i in it.chain(range(_key_index + 1, key_count), range(_key_index)):
            if i != _key_index:
                # print(i)
                # Determine a random value
                ss[i] = random.randint(0, _curve.order)

                # print(ss[i])
                # And the index
                next_i = (i + 1) % key_count

                # Two new EC points are created by multiplying ss_i by G and e_i by as
                # print(curve.is_on_curve(curve.mul_point(e[i],publicKeys[i].W)))
                z_s[i] = _curve.add_point(_curve.mul_point(ss[i], self.G), _curve.mul_point(e[i], _public_keys[i].W))
                e[next_i] = self.hash_function(_message, z_s[i])

        # The signer part itself is calculated separately. This is where the private key is inserted
        # print(e)
        # ss[key_indexx] = (privateKeys[key_indexx].d  - signer.private_key * cs[signer_index] ) % curve.order
        ss[_key_index] = (alfa - _private_key[_key_index].d * e[_key_index]) % _curve.order

        print("Signature is partially calculated:")
        print("'e' array")
        pprint(e)
        print()
        print("array of s-k")
        pprint(ss)
        print()

        # Reproduce the arrays containing the public keys, the message, the first element of the e, and the random
        # s's + the s of the signer
        return _public_keys, _message, e[0], ss

    def verify(self, _curve, _public_keys, _message, _e_0, _ss) -> None:
        """
        Check signature: specifies that the 's' values are calculated after the 'e' values,
        so it involves the use of a private key
        :param _curve: Elliptic curve.
        :param _public_keys: Array of public keys.
        :param _message: String.
        :param _e_0: array of e_0
        :param _ss: s's previously calculated
        """
        # I prepare the blocks
        n = len(_public_keys)
        e = [_e_0] + [0] * (n - 1)
        z_s = [0] * n

        # Iterate over the array and calculate the z_s_i values used to determine the e's, similar to the signature
        for i in range(n):
            z_s[i] = _curve.add_point(_curve.mul_point(_ss[i], self.G), _curve.mul_point(e[i], _public_keys[i].W))
            if i < n - 1:
                e[i + 1] = self.hash_function(_message, z_s[i])
                # print(e)

        print("Verify partially:")
        print("e-k")
        pprint(e)
        print()
        print("to_check value")
        to_check = self.hash_function(_message, z_s[n - 1])
        pprint(to_check)
        print()

        if e[0] == to_check:
            pprint("The signature is valid")
        else:
            pprint("Invalid signature")


if __name__ == "__main__":
    sign = Signature()
    # I create 4 private-public keypairs and put them in the arrays
    publicKeys = []
    privateKeys = []
    signer = EDDSA(hashlib.sha512)

    for x in range(4):
        # privKey, pubKey = KeyPair().get_key_pair()
        privKey = ECPrivateKey(secrets.randbits(32 * 8), sign.curve)
        pubKey = signer.get_public_key(privKey, hashlib.sha512)
        publicKeys.append(privKey.get_public_key())
        privateKeys.append(privKey)

        print("Priv - pubkey pairs:")
        print(privKey)
        print(pubKey)
        print()

        # TESTING#
        # I select the person on index 2 as the signer (but it could be random)

    key_index = 2
    message = "This is a ring signature"
    sign.verify(sign.curve, *sign.sign(sign.curve, message, publicKeys, privateKeys, key_index))
