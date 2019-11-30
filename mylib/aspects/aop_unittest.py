from .aspect import Aspect
import time


class AOPUnitTest(Aspect):
    _unittest_start_time = None

    def pre_process(self, *args, **kwargs):
        print("START", self.func.__name__, sep='\t')
        AOPUnitTest._unittest_start_time = time.process_time()

    def after_process(self, result):
        duration = time.process_time() - AOPUnitTest._unittest_start_time
        print("END", self.func.__name__, 'duration={:.3f}s result={}'.format(duration, result), sep='\t')

    def raise_process(self, e: Exception):
        print("RAISE", self.func.__name__, e, sep='\t')
