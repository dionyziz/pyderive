from math import *

PLUS = True
MINUS = False


class AbstractClassException(Exception):
    pass


class ComparableMixin(object):
    def __ne__(self, other):
        return self < other or other < self

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not other < self


class astNode(ComparableMixin):
    def __init__(self):
        raise AbstractClassException

    def __repr__(self):
        return self.toString(1)

    def __ne__(self, y):
        assert isinstance(y, astNode)
        return not self == y

    def __neg__(self):
        return astUminus(self)

    def __add__(self, y):
        assert isinstance(y, astNode)
        return astPlus(self, y)

    def __sub__(self, y):
        assert isinstance(y, astNode)
        return astMinus(self, y)

    def __mul__(self, y):
        assert isinstance(y, astNode)
        return astTimes(self, y)

    def __pow__(self, y):
        assert isinstance(y, astNode)
        return astPower(self, y)

    def __truediv__(self, y):
        assert isinstance(y, astNode)
        return astDivide(self, y)

    def __eq__(self, y):
        # each subclass must implement = individually
        raise AbstractClassException

    def __lt__(self, y):
        # each subclass must implement < individually
        # if the classes are of different types, then this is called
        astTypes = [
            "astUminus",
            "astConst",
            "astVar",
            "astPlus",
            "astMinus",
            "astTimes",
            "astDivide",
            "astPower",
            "astFunc",
        ]
        # print( 'Comparing a %s to an %s.' % ( self.__class__.__name__, y.
        assert self.__class__.__name__ in astTypes, (
            "Invalid type: " + self.__class__.__name__
        )
        assert y.__class__.__name__ in astTypes, "Invalid type: " + y.__class__.__name__

        return astTypes.index(self.__class__.__name__) < astTypes.index(
            y.__class__.__name__
        )


class astVar(astNode):
    def __init__(self, var):
        self.var = var

    def toString(self, level):
        return self.var

    def __eq__(self, y):
        if not isinstance(y, astVar):
            return False
        return self.var == y.var

    def __lt__(self, y):
        if self.__class__ != y.__class__:
            return super(astVar, self).__lt__(y)
        return self.var < y.var


class astConst(astNode):
    def __init__(self, const):
        self.const = float(const)

    def toString(self, level):
        if self.const.is_integer():
            return str(int(self.const))
        return str(self.const)

    def __eq__(self, y):
        if not isinstance(y, astConst):
            return False
        return self.const == y.const

    def __lt__(self, y):
        if self.__class__ != y.__class__:
            return super(astConst, self).__lt__(y)
        return self.const < y.const


class astBooleanOperator(astNode):
    def toString(self, level):
        return parenthesize(
            self.left.toString(self.priority)
            + " "
            + self.operator
            + " "
            + self.right.toString(self.priority),
            self.priority,
            level,
        )

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, y):
        return (
            self.__class__.__name__ == y.__class__.__name__
            and self.left == y.left
            and self.right == y.right
        )

    def __lt__(self, y):
        if self.__class__ != y.__class__:
            return super(astBooleanOperator, self).__lt__(y)
        if self.left < y.left:
            return True
        if self.left > y.left:
            return False
        return self.right < y.right


class astPlus(astBooleanOperator):
    operator = "+"
    priority = 1


class astMinus(astBooleanOperator):
    operator = "-"
    priority = 1


class astTimes(astBooleanOperator):
    operator = "*"
    priority = 2


class astDivide(astBooleanOperator):
    operator = "/"
    priority = 2


class astPower(astBooleanOperator):
    operator = "^"
    priority = 3


class astUminus(astNode):
    priority = 4

    def toString(self, level):
        return parenthesize("-" + self.arg.toString(4), self.priority, level)

    def __init__(self, arg):
        self.arg = arg

    def __eq__(self, y):
        if self.__class__ != y.__class__:
            return False
        return self.arg == y.arg

    def __lt__(self, y):
        if self.__class__ != y.__class__:
            return super(astUminus, self).__lt__(y)
        return self.arg < y.arg


class astFunc(astNode):
    def toString(self, level):
        return self.func + "(" + self.arg.toString(1) + ")"

    def __init__(self, func, arg):
        self.func = func
        self.arg = arg

    def __eq__(self, y):
        return isinstance(y, astFunc) and self.func == y.func and self.arg == y.arg

    def __lt__(self, y):
        if self.__class__ != y.__class__:
            return super(astFunc, self).__lt__(y)
        if self.func < y.func:
            return True
        if self.func > y.func:
            return False
        return self.arg < y.arg


def parenthesize(expression, selfLevel, parentLevel):
    if selfLevel < parentLevel:
        left, right = "(", ")"
    else:
        # no parentheses unless required
        left, right = "", ""
    return left + expression + right
