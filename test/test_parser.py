from parser import *
import unittest


class TestParser(unittest.TestCase):
    def setUp(self):
        pass

    def testConst(self):
        self.assertEqual(parse("5"), astConst(5))

    def testVar(self):
        self.assertEqual(parse("x"), astVar("x"))

    def testOperators(self):
        self.assertEqual(parse("x + y"), astVar("x") + astVar("y"))
        self.assertEqual(parse("x - y"), astVar("x") - astVar("y"))
        self.assertEqual(parse("x * y"), astVar("x") * astVar("y"))
        self.assertEqual(parse("x / y"), astVar("x") / astVar("y"))
        self.assertEqual(parse("x ^ y"), astVar("x") ** astVar("y"))

    def testParens(self):
        self.assertEqual(parse("(x + y)"), astVar("x") + astVar("y"))
        self.assertEqual(
            parse("(x + y) * z"), (astVar("x") + astVar("y")) * astVar("z")
        )
        self.assertNotEqual(
            parse("(x + y) * z"), astVar("x") + astVar("y") * astVar("z")
        )

    def testFuncs(self):
        self.assertEqual(parse("sin(x)"), astFunc("sin", astVar("x")))
        self.assertEqual(parse("cos(x)"), astFunc("cos", astVar("x")))
        self.assertEqual(parse("tan(x)"), astFunc("tan", astVar("x")))
        self.assertEqual(parse("exp(x)"), astFunc("exp", astVar("x")))
        self.assertEqual(parse("ln(x)"), astFunc("ln", astVar("x")))

    def testWhitespace(self):
        self.assertEqual(parse("           x              "), astVar("x"))
        self.assertEqual(parse(" sin( x ) "), parse("sin(x)"))

    def testComposition(self):
        self.assertEqual(
            parse("sin(cos(tan(x * y)))"),
            astFunc("sin", astFunc("cos", astFunc("tan", astVar("x") * astVar("y")))),
        )

    def testOrder(self):
        self.assertEqual(parse("-(a^2)"), parse("-a^2"))
        self.assertNotEqual(parse("-a^2"), parse("(-a)^2"))

    def testError(self):
        self.assertRaises(ParseException, lambda: parse("( x + y"))
        self.assertRaises(LexException, lambda: parse('( x "+" y )'))

    def tearDown(self):
        pass
