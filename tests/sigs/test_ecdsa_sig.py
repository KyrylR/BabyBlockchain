import unittest

from signature_algorithms.ecdsa_signature import ECDSA
from signature_algorithms.key_pair import KeyPairGenerator


class ECDSATestCase(unittest.TestCase):
    def test_all_process(self):
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
        self.assertTrue(sign.verify(public_keys_list[test_index], msg, *signature))
        # False
        self.assertFalse(sign.verify(public_keys_list[0], msg, *signature))


if __name__ == '__main__':
    unittest.main()
