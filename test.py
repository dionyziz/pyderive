class MC(type):
    def __repr__(self):
        return 'Wahaha!'

class C(object):
    __metaclass__ = MC
    def __init__( self, num ):
        pass

print C( 54 )
