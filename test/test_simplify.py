from simplify.simplify import *
from parser import parse
import unittest

class TestSimplify( unittest.TestCase ):
    def assertSame( self, a, b ):
        sa = simplify( parse( a ) )
        sb = simplify( parse( b ) )
        self.assertEqual( sa, sb )
    def assertNotSame( self, a, b ):
        self.assertNotEqual( simplify( parse( a ) ), simplify( parse( b ) ) )
    def testId( self ):
        self.assertSame( 'x', 'x' )
        self.assertSame( '5', '5' )
        self.assertNotSame( 'x', 'y' )
        self.assertNotSame( 'x', '5' )
        self.assertNotSame( '3', '5' )
    def testParens( self ):
        self.assertSame( 'x + y', '(x + y)' )
        self.assertSame( 'x + y', '(((x + y)))' )
    def testAssociativity( self ):
        self.assertSame( 'x + (y + z)', '(x + y) + z' )
        self.assertSame( 'x * (y * z)', '(x * y) * z' )
        self.assertNotSame( 'x / (y / z)', '(x / y) / z' )
        self.assertNotSame( 'x - (y - z)', '(x - y) - z' )
    def testCommutativity( self ):
        self.assertSame( 'x + y', 'y + x' )
        self.assertSame( 'x * y', 'y * x' )
        self.assertNotSame( 'x / y', 'y / x' )
        self.assertNotSame( 'x - y', 'y - x' )
    def testDistributivity( self ):
        self.assertSame( '-(x + y)', '-x -y' )
        self.assertSame( '-(x - y)', '-x + y' )
        self.assertSame( 'x * (y + z)', 'x * y + x * z' )
        self.assertNotSame( 'x / (y + z)', 'x / y + x / z' )
        self.assertNotSame( 'x - (y - z)', '(x - y) - (x - z)' )
    def testCollect( self ):
        self.assertSame( '3 * x + 2 * x', '5 * x' )
        self.assertSame( '3 * x + 3 * x^2 + y - 2 * x^2 + x - 3 * y', '4 * x + x^2 - 2 * y' )
        self.assertSame( 'x + y + z + 2 * y + 2 * x - x', '2 * x + 3 * y + z' )
    def testErasure( self ):
        self.assertSame( 'x - x', '0' )
        self.assertSame( '2 * x - 2 * x', '0' )
        # two assertions by rob kolstad
        self.assertSame( '(x+3-x-2-1)*x^2', '0' )
        self.assertSame( '(x+4-x-2-1)*x^2', 'x^2' )
        # from ##math
        self.assertSame( '0 - (a + b)', '-a -b' )
        self.assertSame( '(a+b)^2+(a-b)^2 - 2*(a^2+b^2)', '0' )
        self.assertSame( '(a+b)^2+(a-b)^2 - 2*(a^2+b^2+c)', '(-2) * c' )
