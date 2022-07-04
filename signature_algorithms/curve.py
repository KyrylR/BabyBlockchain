from dataclasses import dataclass, field
from os import urandom
from typing import Optional
from utils import *

"""
Here is my motivation to use some tools:
Optional -> https://stackoverflow.com/questions/51710037/how-should-i-use-the-optional-type-hint
@dataclass -> https://blog.logrocket.com/understanding-python-dataclasses/

I find these approaches beautiful, simple and effective.
I don't want to reinvent the wheel, so I just use them.
All links are provided!
Code modification from: https://github.com/lc6chang/ecc-pycrypto/blob/master/ecc/curve.py
"""


@dataclass
class Point:
    x: Optional[int]
    y: Optional[int]
    curve: "MontgomeryCurve"

    def is_ideal_point(self) -> bool:
        """
        https://en.wikipedia.org/wiki/Point_at_infinity
        :return: true if point is ideal(None in our case).
        """
        return self.x is None and self.y is None

    def __post_init__(self):
        if not self.is_ideal_point() and not self.curve.is_on_curve(self):
            raise ValueError("The point is not on the curve.")

    def __str__(self):
        if self.is_ideal_point():
            return f"Point(At infinity, Curve={str(self.curve)})"
        else:
            return f"Point(X={self.x}, Y={self.y}, Curve={str(self.curve)})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.curve == other.curve and self.x == other.x and self.y == other.y

    def __neg__(self):
        return self.curve.neg_point(self)

    def __add__(self, other):
        return self.curve.add_point(self, other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        negative = - other
        return self.__add__(negative)

    def __mul__(self, scalar: int):
        return self.curve.mul_point(scalar, self)

    def __rmul__(self, scalar: int):
        return self.__mul__(scalar)


@dataclass
class MontgomeryCurve:
    """
    by^2 = x^3 + ax^2 + x
    https://en.wikipedia.org/wiki/Montgomery_curve

    Constants are used to implement the curve25519.
    https://en.wikipedia.org/wiki/Curve25519
    """

    name: str = field(default="Curve25519")
    a: int = field(default=486662)
    b: int = field(default=1)
    p: int = field(default=0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffed)
    # Order
    n: int = field(default=0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed)
    G_x: int = field(default=0x9)
    G_y: int = field(default=0x20ae19a1b8a086b4e01edd2c7748d14c923d4d7e6d7c61b229e9c5a27eced3d9)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
                self.a == other.a and self.b == other.b and self.p == other.p and
                self.n == other.n and self.G_x == other.G_x and self.G_y == other.G_y)

    @property
    def G(self) -> Point:
        return Point(self.G_x, self.G_y, self)

    @property
    def INF(self) -> Point:
        return Point(None, None, self)

    def is_on_curve(self, p: Point) -> bool:
        if p.curve != self:
            return False
        return p.is_ideal_point() or self._is_on_curve(p)

    def _is_on_curve(self, p: Point) -> bool:
        left = self.b * p.y * p.y
        right = (p.x * p.x * p.x) + (self.a * p.x * p.x) + p.x
        return (left - right) % self.p == 0

    def add_point(self, p: Point, q: Point) -> Point:
        if (not self.is_on_curve(p)) or (not self.is_on_curve(q)):
            raise ValueError("The points are not on the curve.")
        if p.is_ideal_point():
            return q
        elif q.is_ideal_point():
            return p

        if p == -q:
            return self.INF
        if p == q:
            return self._double_point(p)

        return self._add_point(p, q)

    def _add_point(self, p: Point, q: Point) -> Point:
        # s = (yP - yQ) / (xP - xQ)
        # xR = b * s^2 - a - xP - xQ
        # yR = yP + s * (xR - xP)
        delta_x = p.x - q.x
        delta_y = p.y - q.y
        s = delta_y * mod_inv(delta_x, self.p)
        res_x = (self.b * s * s - self.a - p.x - q.x) % self.p
        res_y = (p.y + s * (res_x - p.x)) % self.p
        return - Point(res_x, res_y, self)

    def _double_point(self, p: Point) -> Point:
        # s = (3 * xP^2 + 2 * a * xP + 1) / (2 * b * yP)
        # xR = b * s^2 - a - 2 * xP
        # yR = yP + s * (xR - xP)
        up = 3 * p.x * p.x + 2 * self.a * p.x + 1
        down = 2 * self.b * p.y
        s = up * mod_inv(down, self.p)
        res_x = (self.b * s * s - self.a - 2 * p.x) % self.p
        res_y = (p.y + s * (res_x - p.x)) % self.p
        return - Point(res_x, res_y, self)

    def mul_point(self, d: int, p: Point) -> Point:
        """
        https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
        """
        if not self.is_on_curve(p):
            raise ValueError("The point is not on the curve.")
        if p.is_ideal_point():
            return self.INF
        if d == 0:
            return self.INF

        res = self.INF
        is_negative_scalar = d < 0
        d = -d if is_negative_scalar else d
        tmp = p
        while d:
            if d & 0x1 == 1:
                res = self.add_point(res, tmp)
            tmp = self.add_point(tmp, tmp)
            d >>= 1
        if is_negative_scalar:
            return -res
        else:
            return res

    def neg_point(self, p: Point) -> Point:
        if not self.is_on_curve(p):
            raise ValueError("The point is not on the curve.")
        if p.is_ideal_point():
            return self.INF

        return self._neg_point(p)

    def _neg_point(self, p: Point) -> Point:
        return Point(p.x, -p.y % self.p, self)

    def compute_y(self, x: int) -> int:
        right = (x * x * x + self.a * x * x + x) % self.p
        inv_b = mod_inv(self.b, self.p)
        right = (right * inv_b) % self.p
        y = mod_sqrt(right, self.p)
        return y

    def encode_point(self, plaintext: bytes) -> Point:
        plaintext = len(plaintext).to_bytes(1, byteorder="big") + plaintext
        while True:
            x = int.from_bytes(plaintext, "big")
            y = self.compute_y(x)
            if y:
                return Point(x, y, self)
            plaintext += urandom(1)

    def decode_point(self, m: Point) -> bytes:
        byte_len = bytes_needed(m.x)
        plaintext_len = (m.x >> ((byte_len - 1) * 8)) & 0xff
        plaintext = ((m.x >> ((byte_len - plaintext_len - 1) * 8))
                     & (int.from_bytes(b"\xff" * plaintext_len, "big")))
        return plaintext.to_bytes(plaintext_len, byteorder="big")
