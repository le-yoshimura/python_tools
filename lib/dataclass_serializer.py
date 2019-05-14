import dataclasses
import json


class Dataclass2JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class DataclassSerializer:

    @staticmethod
    def deserialize(data_type, path):
        return data_type(** DataclassSerializer._load_config_as_dict(path))

    @staticmethod
    def _load_config_as_dict(path):
        with open(path, mode='r', encoding='utf-8') as f:
            dict_data = json.load(f)
        return dict_data

    @staticmethod
    def serialize(data, path):
        with open(path, mode='w', encoding='utf-8') as f:
            json.dump(data, f, cls=Dataclass2JSONEncoder, indent=4)
