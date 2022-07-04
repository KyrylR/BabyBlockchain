from binascii import hexlify
from dataclasses import dataclass, field
from os import urandom
from curve import MontgomeryCurve, Point
from typing import Tuple

"""
I find these approaches beautiful, simple and effective.
I don't want to reinvent the wheel, so I just use them.
All links are provided!
Code modification from: https://github.com/AntonKueltz/fastecdsa
"""


@dataclass
class KeyPair:
    """
    A class designed to handle key pairs.
    It generates private and public keys based on Elliptic Curve math.
    The curve used is curve25519.
    Refs to: https://github.com/AntonKueltz/fastecdsa/blob/master/fastecdsa/keys.py
    """
    curve: MontgomeryCurve = field(default=MontgomeryCurve())

    def gen_keypair(self) -> Tuple[int, Point]:
        """
        Generate a keypair that consists of a private key and a public key.
        The private key :math:`d` is an integer generated via a cryptographically secure random number
        generator that lies in the range :math:`[1,n)`, where :math:`n` is the curve order. The public
        key :math:`Q` is a point on the curve calculated as :math:`Q = dG`, where :math:`G` is the
        curve's base point.
        Args:
            curve (fastecdsa.curve.Curve): The curve over which the keypair will be calulated.
        Returns:
            int, fastecdsa.point.Point: Returns a tuple with the private key first and public key
            second.
        """
        private_key = self.gen_private_key(self.curve)
        public_key = self.get_public_key(private_key, self.curve)
        return private_key, public_key

    @staticmethod
    def gen_private_key(curve: MontgomeryCurve) -> int:
        """
        Generate a private key to sign data with.
        The private key :math:`d` is an integer generated via a cryptographically secure random number
        generator that lies in the range :math:`[1,n)`, where :math:`n` is the curve order. The default
        random number generator used is /dev/urandom.
        Args:
            |  curve (fastecdsa.curve.Curve): The curve over which the key will be calulated.
            |  randfunc (function): A function taking one argument 'n' and returning a bytestring
                                of n random bytes suitable for cryptographic use.
                                The default is "os.urandom"
        Returns:
            int: Returns a positive integer smaller than the curve order.
        """
        order_bits = 0
        order = curve.n

        while order > 0:
            order >>= 1
            order_bits += 1

        order_bytes = (order_bits + 7) // 8
        extra_bits = order_bytes * 8 - order_bits

        rand = int(hexlify(urandom(order_bytes)), 16)
        rand >>= extra_bits

        while rand >= curve.n:
            rand = int(hexlify(urandom(order_bytes)), 16)
            rand >>= extra_bits

        return rand

    @staticmethod
    def get_public_key(d: int, curve: MontgomeryCurve) -> Point:
        """
        Generate a public key from a private key.
        The public key :math:`Q` is a point on the curve calculated as :math:`Q = dG`, where :math:`d`
        is the private key and :math:`G` is the curve's base point.
        Args:
            |  d (long): An integer representing the private key.
            |  curve (fastecdsa.curve.Curve): The curve over which the key will be calulated.
        Returns:
            fastecdsa.point.Point: The public key, a point on the given curve.
        """
        return d * curve.G
