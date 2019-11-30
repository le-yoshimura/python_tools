import dataclasses
import json
import mylib.cryptos.aes as aes
import base64


class DataclassSerializer:

    class Dataclass2JSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)

    @staticmethod
    def deserialize(data_type, path):
        return data_type(** DataclassSerializer.load_json_as_dict(path))

    @staticmethod
    def deserialize_with_decrypt(data_type, path, password):
        with open(path, mode='r', encoding='utf-8') as f:
            file = f.read()
            iv = base64.b64decode(file[:24])
            text = base64.b64decode(file[24:])
            decrypted = aes.AES(password).decrypt(text=text, iv=iv)
            dict_data = json.loads(decrypted)
        return data_type(** dict_data)

    @staticmethod
    def load_json_as_dict(path):
        with open(path, mode='r', encoding='utf-8') as f:
            dict_data = json.load(f)
        return dict_data

    @staticmethod
    def serialize(data, path):
        with open(path, mode='w', encoding='utf-8') as f:
            json.dump(data, f, cls=DataclassSerializer.Dataclass2JSONEncoder, indent=4)

    @staticmethod
    def serialize_with_encrypt(data, path, password):
        with open(path, mode='w', encoding='utf-8') as f:
            text = json.dumps(data, cls=DataclassSerializer.Dataclass2JSONEncoder, indent=4)
            iv, encrypted = aes.AES(password).encrypt(text=text)
            base64text = (base64.b64encode(iv) + base64.b64encode(encrypted)).decode('ascii')
            f.write(base64text)
