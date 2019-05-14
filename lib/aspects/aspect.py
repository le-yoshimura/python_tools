from abc import ABCMeta, abstractmethod


class Aspect(metaclass=ABCMeta):
    """アスペクト指向抽象クラス"""

    @abstractmethod
    def pre_process(self, *args, **kwargs):
        """
        関数実行前処理
        :param args: 位置引数
        :param kwargs: キーワード引数
        :return:
        """
        pass

    @abstractmethod
    def after_process(self, result):
        """
        関数実行後処理
        :return:
        """
        pass

    @abstractmethod
    def raise_process(self, e: Exception):
        """
        例外発生時処理
        :param e: 発生例外
        :return:
        """
        pass

    def __call__(self, func: object):
        """
        アスペクト指向クラスデコレータコール処理
        :param func: 修飾対象関数
        :return: 修飾後関数
        """
        # 修飾対象メソッドの属性を取得できるように保持します
        self.func = func

        def wrapper(*args, **kwargs):
            self.pre_process(*args, **kwargs)
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                self.raise_process(e)
                raise e
            self.after_process(result)
            return result
        return wrapper
