from Crypto import Cipher
from .abc_crypto import ABCCrypto
from Crypto import Random
from Crypto.Util import Counter


class AES(ABCCrypto):
    @staticmethod
    def _pad(text, block_size):
        """
        パディング処理
        端数が生じた場合、ブロックの倍数長になるようにパディングを行う。
        パディングに使うbyte値と、パディングするbyte数を一致させる。
        そうすることで、アンパディングする時に末尾のbyte値を取得すれば、何byteのパディングが行われたか解る。
        元々16byteの倍数長である場合も、アンパディング時にエラーが発生しないように16byte分パディングする。
        Args:
            text: str
            block_size: int

        Returns: str パディング済文字列

        """
        return text + (block_size - len(text.encode()) % block_size) * chr(block_size - len(text.encode()) % block_size)

    def __init__(self
                 , key: str
                 , mode: Cipher.blockalgo = Cipher.AES.blockalgo.MODE_CBC
                 , segment_size=8):
        """
        コンストラクタ
        Args:
            key: 鍵文字列
            mode: 暗号モード
            segment_size: セグメントサイズ(CFBモードでのみ使用)
        """
        self._key = key
        self._mode: Cipher.AES.blockalgo = mode
        self._segment_size = segment_size
        self._cipher: Cipher.AES.AESCipher = None
        self._resize_key()

    def _resize_key(self):
        """
        鍵がAES規格の長さになるように調整
        Returns:None

        """
        size = len(self._key)
        if size > Cipher.AES.key_size[2]:
            # 鍵長が32byteを超える場合
            self._key = self._key[:Cipher.AES.key_size[2]].encode()
        elif size > Cipher.AES.key_size[1]:
            # 鍵長が24byteを超える場合
            self._key = self._key[:Cipher.AES.key_size[1]].encode()
        elif size >= Cipher.AES.key_size[0]:
            # 鍵長が16byte以上の場合
            self._key = self._key[:Cipher.AES.key_size[0]].encode()
        else:
            # 鍵長が16byteに満たない場合
            self._key = self._pad(self._key, Cipher.AES.key_size[0]).encode()

    def _init_cipher(self, iv):
        """
        暗号化インスタンス初期化処理
        Args:
            iv: bytes

        Returns:None

        """
        if self._mode == Cipher.AES.blockalgo.MODE_CTR:
            ctr = Counter.new(128)
            self._cipher = Cipher.AES.new(self._key, self._mode, iv, counter=ctr)
        elif self._mode == Cipher.AES.MODE_CFB:
            self._cipher = Cipher.AES.new(self._key, self._mode, iv, segment_size=self._segment_size)
        else:
            self._cipher = Cipher.AES.new(self._key, self._mode, iv)

    def encrypt(self, *args, **kwargs):
        """
        暗号化処理
        MODE_ECB,MODE_CTRの場合はIVが無視される
        暗号化対象文字列が16byteの倍数長になるようにパディングする
        Args:
            *args:
            **kwargs: text: str

        Returns:IV: bytes, crypto: bytes

        """
        iv = Random.new().read(Cipher.AES.block_size)
        self._init_cipher(iv)
        padded = self._pad(str(kwargs['text']), Cipher.AES.block_size).encode()
        return iv, self._cipher.encrypt(padded)

    def decrypt(self, *args, **kwargs):
        """
        復号処理
        Args:
            *args:
            **kwargs:text: bytes, iv: bytes

        Returns:復号文字列: str

        """
        # IV is ignored for MODE_ECB and MODE_CTR.
        self._init_cipher(kwargs['iv'])
        decrypted = self._cipher.decrypt(kwargs['text'])
        unpadded = decrypted[:-ord(decrypted[len(decrypted) - 1:])]
        return unpadded.decode()






