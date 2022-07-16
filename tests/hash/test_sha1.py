import unittest

from blockchain.hash import Hash


class SHA1TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        website = "https://emn178.github.io/online-tools/sha1.html"
        print(f"To ensure that the algorithm is implemented correctly, you can use this website: \n{website}")

    @classmethod
    def pretty_print(cls, expected, actual_hash, actual):
        print("-" * 20, end='\n')
        info = (actual[:30] + '...(see string in code)') if len(actual) > 30 else actual
        print(f"{'Message:':15} {info}", end='\n')
        print(f"{'My hash:':15} {actual_hash}")
        print(f"{'Expected hash:':15} {expected}")
        print("-" * 20, end='\n')

    def test_on_keccak_strings(self):
        actual = "Keccak"
        expected = "34a663a04dabe538f7e6b01cb2e4727d55d1364b"
        actual_hash = Hash().to_sha1(actual)
        # self.pretty_print(expected, actual_hash, actual)
        self.assertEqual(actual_hash, expected)

    def test_on_long_strings(self):
        actual = "SHA1 and other hash functions online generator"
        expected = "7e16b5527c77ea58bac36dddda6f5b444f32e81b"
        actual_hash = Hash().to_sha1(actual)
        # self.pretty_print(expected, actual_hash, actual)
        self.assertEqual(actual_hash, expected)

    def test_on_number_strings(self):
        actual = "123123123"
        expected = "88ea39439e74fa27c09a4fc0bc8ebe6d00978392"
        actual_hash = Hash().to_sha1(actual)
        # self.pretty_print(expected, actual_hash, actual)
        self.assertEqual(actual_hash, expected)


if __name__ == '__main__':
    unittest.main()
