from ast import *
import unittest

class TestAst( unittest.TestCase ):
    def setUp( self ):
        self.zero = astConst( 0 )
        self.one = astConst( 1 )
    def testConstruction( self ):
        self.assertEqual( astConst( 5 ).const, 5 )
        self.assertEqual( astVar( 'x' ).var, 'x' )
        f = astFunc( 'sin', self.zero )
        self.assertEqual( f.func, 'sin' )
        self.assertEqual( f.arg, self.zero )
        plus = astPlus( self.zero, self.one )
        self.assertEqual( plus.left, self.zero )
        self.assertEqual( plus.right, self.one )
        minus = astMinus( self.zero, self.one )
        self.assertEqual( minus.left, self.zero )
        self.assertEqual( minus.right, self.one )
        times = astTimes( self.zero, self.one )
        self.assertEqual( times.left, self.zero )
        self.assertEqual( times.right, self.one )
        div = astDivide( self.zero, self.one )
        self.assertEqual( div.left, self.zero )
        self.assertEqual( div.right, self.one )
        u = astUminus( self.one )
        self.assertEqual( u.arg, self.one )
        power = astPower( self.zero, self.one )
        self.assertEqual( power.left, self.zero )
        self.assertEqual( power.right, self.one )
    def testOverloading( self ):
        plus = self.one + self.zero
        self.assertTrue( isinstance( plus, astPlus ) )
        self.assertEqual( plus.left, self.one )
        self.assertEqual( plus.right, self.zero )
        minus = self.one - self.zero
        self.assertTrue( isinstance( minus, astMinus ) )
        self.assertEqual( minus.left, self.one )
        self.assertEqual( minus.right, self.zero )
        times = self.one * self.zero
        self.assertTrue( isinstance( times, astTimes ) )
        self.assertEqual( times.left, self.one )
        self.assertEqual( times.right, self.zero )
        div = self.zero / self.one
        self.assertTrue( isinstance( div, astDivide ) )
        self.assertEqual( div.left, self.zero )
        self.assertEqual( div.right, self.one )
    def testEqual( self ):
        self.assertEqual( astConst( 0 ), astConst( 0 ) )
        self.assertNotEqual( astConst( 0 ), astConst( 1 ) )
        self.assertEqual( astVar( 'x' ), astVar( 'x' ) )
        self.assertNotEqual( astVar( 'x' ), astVar( 'y' ) )
        self.assertNotEqual( astVar( 'x' ), -astVar( 'x' ) )
        self.assertNotEqual( astConst( 0 ), astFunc( 'sin', astConst( 1 ) ) )
        self.assertEqual( astConst( 2 ) + astConst( 5 ) * astVar( 'x' ), \
                          astConst( 2 ) + astConst( 5 ) * astVar( 'x' ) )
