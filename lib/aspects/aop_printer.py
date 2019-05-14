from .aspect import Aspect


class AOPPrinter(Aspect):

    def pre_process(self, *args, **kwargs):
        from datetime import datetime
        print("START", self.func.__module__, self.func.__name__, datetime.now(), args, kwargs, sep='\t')

    def after_process(self, result):
        from datetime import datetime
        print("END", self.func.__module__, self.func.__name__, datetime.now(), 'result={}'.format(result), sep='\t')

    def raise_process(self, e: Exception):
        from datetime import datetime
        print("RAISE", self.func.__module__, self.func.__name__, datetime.now(), e, sep='\t')
