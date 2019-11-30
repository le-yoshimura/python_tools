import unittest
from mylib.db.mongoengine_wrapper import *


class DummyDocument(DocumentWrapper):
    field1 = IntField()
    field2 = StringField()


class MyTestCase(unittest.TestCase):
    def test_df2doc_gen(self):
        df = pd.DataFrame([item, f'text{item}'] for item in range(10))
        df = df.rename(columns={0: 'field1', 1: 'field2'})
        for item in DummyDocument().df2doc_gen(df.iloc[:,1:]):
            print(item.field1, item.field2)
        self.assertTrue(True)

    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
