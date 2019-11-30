from abc import ABCMeta, abstractmethod
import base64


class ABCCrypto(metaclass=ABCMeta):

    @abstractmethod
    def encrypt(self, *args, **kwargs):
        pass

    @abstractmethod
    def decrypt(self, *args, **kwargs):
        pass

    @staticmethod
    def to_base64(b: bytes):
        return base64.b64encode(b)

    @staticmethod
    def from_base64(text: str):
        return base64.b64decode(text)
