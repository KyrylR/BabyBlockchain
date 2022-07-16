"""
I find these approaches beautiful, simple and effective.
I don't want to reinvent the wheel, so I just use them.
All links are provided!
"""

from math import log

from blockchain.hash import Hash

"""
Modular multiplicative inverse function in Python:
https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
"""


def egcd(a, b):
    """
    In arithmetic and computer programming, the extended Euclidean algorithm is an extension to the Euclidean
    algorithm, and computes, in addition to the greatest common divisor (gcd) of integers a and b,
    also the coefficients of Bezout's identity, which are integers x and y such that
    ax + by = gcd(a, b).

    Given two integers ``b`` and ``n``
    returns ``(gcd(b, n), a, m)`` such that ``a*b + n*m == gcd(b, n)``.
    """
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def mod_inv(a, m):
    """
    In mathematics, particularly in the area of arithmetic, a modular multiplicative inverse of
    an integer `a` is an integer x such that the product ax is congruent to 1 with respect to the modulus m.
    In the standard notation of modular arithmetic this congruence is written as
    ax ≡ 1 (mod m)
    :return: multiplicative inverse of an integer a
    """
    a = a % m
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("modular inverse does not exist")
    else:
        return x % m


"""
Quadratic Residue:
https://github.com/darkwallet/python-obelisk/blob/5812ccfd78a66963f7238d9835607908a8c8f392/obelisk/numbertheory.py
"""


def mod_sqrt(a, p):
    """
    Find a quadratic residue (mod p) of 'a'. p must be an odd prime.
    Solve the congruence of the form: x^2 = a (mod p)
    And returns x. Note that p - x is also a root.
    0 is returned is no square root exists for these a and p.
    The Tonelli-Shanks algorithm is used (except for some simple cases
    in which the solution is known from an identity).
    This algorithm runs in polynomial time (unless thegeneralized Riemann hypothesis is false).
    """

    # Simple cases
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    # Partition p-1 to s * 2^e for an odd s (i.e.
    # reduce all the powers of 2 from p-1)
    s = p - 1
    e = 0
    while s % 2 == 0:
        # Interesting bug. s /= 2 and s = int(s) not equals to s //= 2
        # s /= 2
        # s = int(s)
        s //= 2
        e += 1

    # Find some 'n' with a legendre symbol n|p = -1.
    # Shouldn't take long.
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    # Here be dragons!
    # Read the paper "Square roots from 1; 24, 51,
    # 10 to Dan Shanks" by Ezra Brown for more information
    #

    # x is a guess of the square root that gets better
    # with each iteration.
    # b is the "fudge factor" - by how much we're off
    # with the guess. The invariant x^2 = ab (mod p)
    # is maintained throughout the loop.
    # g is used for successive powers of n to update
    # both a and b
    # r is the exponent - decreases with each update
    #
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


def legendre_symbol(a, p):
    """
    Compute the Legendre symbol a|p using Euler's criterion. p is a prime,
    a is relatively prime to p (if p divides a, then a|p = 0)
    :return: 1 if a has a square root modulo p, -1 otherwise.
    """
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls


def bytes_needed(n: int) -> int:
    """
    Get size in Bytes needed for an integer.
    https://stackoverflow.com/questions/14329794/get-size-in-bytes-needed-for-an-integer-in-python
    :param n: integer.
    :return: byte size.
    """
    if n == 0:
        return 1
    return int(log(n, 256)) + 1


def performance(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        from time import time
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function: {func.__name__} took {t2 - t1} s')
        return result

    return wrapper


def get_transaction_message(sender_acc_id: str, receiver_acc_id: str, amount: int) -> str:
    return Hash().to_sha1(sender_acc_id + receiver_acc_id + str(amount))


def get_coinbase_tx_msg(receiver_acc_id: str, amount: int) -> str:
    return Hash().to_sha1(receiver_acc_id + str(amount))
