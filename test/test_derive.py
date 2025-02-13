from simplify.simplify import *
from parser import parse
from derive import derive
import unittest


class TestDerive(unittest.TestCase):
    def assertDerivative(self, function, derivative):
        self.assertEqual(
            simplify(derive(parse(function), "x")), simplify(parse(derivative))
        )

    def testConst(self):
        self.assertDerivative("0", "0")
        self.assertDerivative("12", "0")
        self.assertDerivative("12 + 7", "0")
        self.assertDerivative("c", "0")
        self.assertDerivative("38 * c + 12", "0")

    def testLinear(self):
        self.assertDerivative("x", "1")
        self.assertDerivative("2 * x", "2")
        self.assertDerivative("2 * x + 5", "2")
        self.assertDerivative("(2 + 3) * x + 5 * x", "10")

    def testPolynomial(self):
        self.assertDerivative("x^3 + x^2 + x", "3 * x^2 + 2 * x + 1")
        self.assertDerivative("x^12 + x^5 - 2 * x - 3 + y", "12 * x ^ 11 + 5 * x^4 - 2")

    def testTrig(self):
        self.assertDerivative("sin(x)", "cos(x)")
        self.assertDerivative("cos(x)", "-sin(x)")
        # requires trig simplification; TODO
        # self.assertDerivative( 'tan(x)', '1 / cos( x )^2' )

    def testComposite(self):
        self.assertDerivative("sin(cos(x))", "sin(x)*(-cos(cos(x)))")
        self.assertDerivative(
            "sin(x * cos(x))", "cos(x * cos(x)) * (cos(x) - x * sin(x))"
        )
