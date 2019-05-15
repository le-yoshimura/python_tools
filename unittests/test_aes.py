import unittest
import base64
from mylib.cryptos.aes import AES
from Crypto import Cipher
from mylib.aspects.aop_unittest import AOPUnitTest


class MyTestCase(unittest.TestCase):
    @AOPUnitTest()
    def test_encrypt_decrypt(self):
        def encrypt_decrypt(key, text,
                            mode=Cipher.AES.blockalgo.MODE_CBC,
                            segment_size=8):
            cipher = AES(key, mode, segment_size)
            iv, encrypted = cipher.encrypt(text=text)
            print(f'IV:{iv} crypto:{encrypted} base64:{base64.b64encode(encrypted)}')
            decrypted = cipher.decrypt(text=encrypted, iv=iv)
            print(decrypted)
            self.assertTrue(text == decrypted)

        encrypt_decrypt('1234abcd6789efgh0', '1234567890123456')
        encrypt_decrypt('1234abcd', 'keyが16byte以下')
        encrypt_decrypt('1234abcd6789efgh', 'keyが16byte')
        encrypt_decrypt('1234abcd6789efgh0', 'keyが16byteを超える')
        encrypt_decrypt('1234abcd6789efgh1234abcd', 'keyが24byte')
        encrypt_decrypt('1234abcd6789efgh1234abcd0', 'keyが24byteを超える')
        encrypt_decrypt('1234abcd6789efgh1234abcd6789efgh', 'keyが32byte')
        encrypt_decrypt('1234abcd6789efgh1234abcd6789efgh0', 'keyが32byteを超える')
        encrypt_decrypt('1234abcd6789efgh1234abcd6789efgh0', 'モードCFB', mode=Cipher.AES.blockalgo.MODE_CFB)
        encrypt_decrypt('1234abcd6789efgh1234abcd6789efgh0', 'モードCTR', mode=Cipher.AES.blockalgo.MODE_CTR)
        encrypt_decrypt('1234abcd6789efgh1234abcd6789efgh0', 'モードECB', mode=Cipher.AES.blockalgo.MODE_ECB)
        encrypt_decrypt('1234abcd6789efgh1234abcd6789efgh0', 'モードOFB', mode=Cipher.AES.blockalgo.MODE_OFB)
        

if __name__ == '__main__':
    unittest.main()
