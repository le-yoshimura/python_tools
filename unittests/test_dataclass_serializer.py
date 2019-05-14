import unittest
from mylib.aspects.aop_unittest import AOPUnitTest
from dataclasses import dataclass
from mylib.dataclass_serializer import DataclassSerializer


@dataclass
class NestModel:
    nest1: int = 1
    nest2: str = "nest"


@dataclass
class TestModel:
    value1: str
    value2: int
    value3: float
    value4: dict


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._path = './dat/dataclass.json'
        cls._data = TestModel("1", 2, 3.3, {'dict1': 12, 'dict2': "text"})

    @AOPUnitTest()
    def test_serialize(self):
        import os
        if os.path.exists(self._path):
            os.remove(self._path)
        DataclassSerializer.serialize(self._data, self._path)
        self.assertTrue(os.path.exists(self._path))

    @AOPUnitTest()
    def test_deserialize(self):
        res: TestModel = DataclassSerializer.deserialize(TestModel, self._path)
        self.assertEqual(res, self._data)


if __name__ == '__main__':
    unittest.main()
