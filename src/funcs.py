import math
import random


def build_expr(prob=0.99):
    """Builds a random expression based on given probability."""
    if random.random() < prob:
        return random.choice([SinPi, CosPi, SinPi, CosPi, Times, Cos, Sin, Times])(prob)
    return random.choice([X, Y, PI, X, Y])()


class BaseExpression:
    """Base class for all expressions."""

    def __str__(self):
        return self.__class__.__name__

    def eval(self, x, y):
        raise NotImplementedError(
            "Eval method must be implemented in the derived class."
        )


class UnaryOperation(BaseExpression):
    def __init__(self, arg, new=True):
        self.arg = build_expr(arg * arg) if new else arg
    
    def eval(self, x, y):
        super().eval(None, None)


class X(BaseExpression):
    def eval(self, x, y):
        return x

    def __str__(self):
        return "x"


class PI(BaseExpression):
    def eval(self, x, y):
        return math.pi

    def __str__(self):
        return "pi"


class Y(BaseExpression):
    def eval(self, x, y):
        return y

    def __str__(self):
        return "y"


class Cos(UnaryOperation):
    def __str__(self):
        return f"cos({self.arg})"

    def eval(self, x, y):
        return math.cos(self.arg.eval(x, y))


class Sin(UnaryOperation):
    def __str__(self):
        return f"sin({self.arg})"

    def eval(self, x, y):
        return math.sin(self.arg.eval(x, y))


class Times(BaseExpression):
    def __init__(self, prob=None, lhs=None, rhs=None, new=True):
        if new:
            self.lhs = build_expr(prob * prob)
            self.rhs = build_expr(prob * prob)
        else:
            self.lhs = lhs
            self.rhs = rhs

    def __str__(self):
        return f"{self.lhs}*{self.rhs}"

    def eval(self, x, y):
        return self.lhs.eval(x, y) * self.rhs.eval(x, y)


class SinPi(UnaryOperation):
    def __str__(self):
        return "sin(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        return math.sin(math.pi * self.arg.eval(x, y))


class CosPi(UnaryOperation):
    def __str__(self):
        return "cos(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        return math.cos(math.pi * self.arg.eval(x, y))
