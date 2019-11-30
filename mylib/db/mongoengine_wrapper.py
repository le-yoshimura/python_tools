import pandas as pd
from mongoengine.document import Document
from mongoengine.fields import *


class DocumentWrapper(Document):
    meta = {'allow_inheritance': True}

    def df2doc_gen(self: Document, df: pd.DataFrame):
        for item in df.itertuples():
            self.__init__(*item)
            yield self

    @classmethod
    def docs2df(cls):
        result = pd.DataFrame()
        for idx, item in enumerate(cls.objects):
            item_dict = item.to_mongo()
            del item_dict['_id']
            del item_dict['_cls']
            result = result.append(pd.DataFrame(item_dict, index=[idx]))
        return result
