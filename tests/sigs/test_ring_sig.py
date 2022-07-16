import unittest

from signature_algorithms.key_pair import KeyPairGenerator
from signature_algorithms.ring_signature import RingSignature


class RingSignatureTestCase(unittest.TestCase):
    def test_all_process(self):
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
        self.assertTrue(sign.verify(message, public_keys_list, *signature))


if __name__ == '__main__':
    unittest.main()
