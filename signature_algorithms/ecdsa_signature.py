from dataclasses import dataclass, field
from random import randint
from typing import Tuple, Optional
from curve import MontgomeryCurve, Point
from blockchain.hash import Hash
from features.utils import mod_inv
from features.utils import performance

from signature_algorithms.key_pair import KeyPairGenerator


@dataclass
class ECDSA:
    gen_point: Optional[Point] = field(default=None)
    curve: MontgomeryCurve = field(default=MontgomeryCurve())

    def __post_init__(self):
        self.gen_point = self.curve.G

    # @performance
    def sign(self, _private_key: int, message: str) -> Tuple[int, int]:
        r, s, rand_k = 0, 0, 0
        while s == 0:
            while r == 0:
                # 1. Select a random or pseudorandom integer k, 1 ≤ k ≤ n - 1
                rand_k = randint(1, self.curve.n - 1)
                # 2. Compute kG = (x1, y1) and convert x1 to an integer x1
                k_g = self.curve.mul_point(rand_k, self.gen_point)
                # 3. Compute r = x1 mod n. If r = 0 then go to step 1.
                r = int(k_g.x) % self.curve.n

            # 4. Compute k-1 mod n.
            inv_k = mod_inv(rand_k, self.curve.n)

            # 5. Compute SHA-1(m) and convert this bit string to an integer e.
            e = int(Hash().to_sha1(message), 16)

            # 6. Compute 5 = k-1(e + dr) mod n. If s = 0 then go to step 1.
            s = inv_k * (e + _private_key * r) % self.curve.n

        # 7. A's signature for the message m is (r, s).
        return r, s

    # @performance
    def verify(self, _public_key: Point, message: str, r: int, s: int) -> bool:
        # 1. Verify that r and s are integers in the interval [1, n - 1].
        if r not in range(1, self.curve.n - 1) or r not in range(1, self.curve.n - 1):
            return False

        # 2. Compute SHA-1(m) and convert this bit string to an integer e
        e = int(Hash().to_sha1(message), 16)

        # 3. Compute w = s^-1 mod n.
        w = mod_inv(s, self.curve.n)

        # 4. Compute u1 = ew mod n and u2 = rw mod n.
        u1 = (e * w) % self.curve.n
        u2 = (r * w) % self.curve.n

        # 5. Compute X = u1G + u2Q.
        point_x = self.curve.add_point(self.curve.mul_point(u1, self.gen_point), self.curve.mul_point(u2, _public_key))

        # 6. If X = 0, then reject the signature.
        # Otherwise, convert the x-coordinate x1 of X to an integer x1, and compute v = x1 mod n.
        if not self.curve.is_on_curve(point_x):
            return False
        v = point_x.x % self.curve.n

        # 7. Accept the signature if and only if u = r.
        return v == r


if __name__ == "__main__":
    sign = ECDSA()
    key_pair = KeyPairGenerator()
    public_keys_list = []
    private_keys = []

    for idx in range(20):
        pk, pbk = key_pair.gen_keypair()
        public_keys_list.append(pbk)
        private_keys.append(pk)

    test_index = 2
    msg = "This is a ECDSA signature"
    signature = sign.sign(private_keys[test_index], msg)
    # True
    print(sign.verify(public_keys_list[test_index], msg, *signature))
    # False
    print(sign.verify(public_keys_list[0], msg, *signature))
