from unittest import TestCase
from aspects.aop_printer import AOPPrinter


@AOPPrinter()
def after_process_target():
    print("Execute")


class TestAOPPrinter(TestCase):

    def self_method(self):
        self.self_value = "Self value"
        print(self.self_value)

    @AOPPrinter()
    def pre_process_target(self, a, b, name="", value=""):
        print("Execute")
        self.self_method()
        print(a, b, name, value)
        return a + b

    @AOPPrinter()
    def raise_process_target(self):
        print("Execute")
        self.self_method()
        a, b = 1, 0
        print(a/b)

    def test_pre_process(self):
        self.pre_process_target(1, 2, name="Name", value="Value")
        self.assertTrue(True)

    def test_after_process(self):
        after_process_target()
        self.assertTrue(True)

    def test_raise_process(self):
        with self.assertRaises(ZeroDivisionError):
            self.raise_process_target()

