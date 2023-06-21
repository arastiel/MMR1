from math import *
import numpy as np
import matplotlib.pyplot as plt


class Function:
    def __call__(self, x):
        pass

    def __str__(self):
        pass

    def __add__(self, g):
        if not isinstance(g, Function):
            g = Const(g)
        return AddFunction(self, g)

    def __neg__(self):
        if not isinstance(g, Function):
            g = Const(g)
        return NegFunction(self)

    def __sub__(self, g):
        if not isinstance(g, Function):
            g = Const(g)
        return AddFunction(self, NegFunction(g))

    def __mul__(self, g):
        if not isinstance(g, Function):
            g = Const(g)
        return MulFunction(self, g)

    def __truediv__(self, g):
        if not isinstance(g, Function):
            g = Const(g)
        return DivFunction(self, g)

    def __pow__(self, g):
        if not isinstance(g, Function):
            g = Const(g)
        return PowFunction(self, g)

    def __matmul__(self, g):
        if not isinstance(g, Function):
            g = Const(g)
        # Python ist dafür leider zu blöd, also händisch
        if isinstance(self, Exp) & isinstance(g, Ln):
            return Id()
        if isinstance(g, Exp) & isinstance(self, Ln):
            return Id()
        if isinstance(self, Id):
            return g
        return Composition(self, g)


class DualNumber:
    def __init__(self, wert, ableitung):
        self.wert = wert
        self.ableitung = ableitung

    def __add__(self, g):
        return DualNumber(self.wert + g.wert, self.ableitung + g.ableitung)

    def __neg__(self):
        return DualNumber(-self.wert, -self.ableitung)

    def __sub__(self, g):
        return self + (-g)

    def __mul__(self, g):
        return DualNumber(self.wert * g.wert, self.wert * g.ableitung + self.ableitung * g.wert)

    def __truediv__(self, g):
        return DualNumber(self.wert / g.wert, (self.ableitung * g.wert - self.wert * g.ableitung) / g.wert ** 2)

    def __pow__(self, n):
        if isinstance(n.wert, int):
            return DualNumber(self.wert ** n.wert, n.wert * (self.wert ** (n.wert - 1)) * self.ableitung)
        return DualNumber(self.wert ** n.wert, "Nicht berechenbar")

    def __str__(self):
        return "(" + str(self.wert) + "," + str(self.ableitung) + ")"


class AddFunction(Function):
    def __init__(self, f, g):
        self.f = f
        self.g = g

    def __call__(self, x):
        return self.f(x) + self.g(x)

    def __str__(self):
        return "AddFunction(" + str(self.f) + ", " + str(self.g) + ")"


class NegFunction(Function):
    def __init__(self, f):
        self.f = f

    def __call__(self, x):
        return -self.f(x)

    def __str__(self):
        return "NegFunction(" + str(self.f) + ")"


class MulFunction(Function):
    def __init__(self, f, g):
        self.f = f
        self.g = g

    def __call__(self, x):
        return self.f(x) * self.g(x)

    def __str__(self):
        return "MulFunction(" + str(self.f) + ", " + str(self.g) + ")"


class DivFunction(Function):
    def __init__(self, f, g):
        self.f = f
        self.g = g

    def __call__(self, x):
        return self.f(x) / self.g(x)

    def __str__(self):
        return "DivFunction(" + str(self.f) + ", " + str(self.g) + ")"


class PowFunction(Function):
    def __init__(self, f, g):
        self.f = f
        self.g = g

    def __call__(self, x):
        return self.f(x) ** self.g(x)

    def __str__(self):
        return "PowFunction(" + str(self.f) + ", " + str(self.g) + ")"


class Composition(Function):
    def __init__(self, f, g):
        self.f = f
        self.g = g

    def __call__(self, x):
        return self.f(self.g(x))

    def __str__(self):
        return "Composition(" + str(self.f) + "(" + str(self.g) + "))"


class Id(Function):
    def __call__(self, x):
        return DualNumber(x, 1)

    def __str__(self):
        return "x"


class Sin(Function):
    def __call__(self, x):
        if isinstance(x, DualNumber):
            return DualNumber(sin(x.wert), cos(x.wert) * x.ableitung)
        return DualNumber(sin(x), cos(x))

    def __str__(self):
        return "Sin"


class Cos(Function):
    def __call__(self, x):
        if isinstance(x, DualNumber):
            return DualNumber(cos(x.wert), -sin(x.wert) * x.ableitung)
        return DualNumber(cos(x), -sin(x))

    def __str__(self):
        return "Cos"


class Exp(Function):
    def __call__(self, x):
        if isinstance(x, DualNumber):
            return DualNumber(exp(x.wert), exp(x.wert) * x.ableitung)
        return DualNumber(exp(x), exp(x))

    def __str__(self):
        return "Exp"


class Ln(Function):
    def __call__(self, x):
        if isinstance(x, DualNumber):
            return DualNumber(log(x.wert), (1 / x.wert) * x.ableitung)
        return DualNumber(log(x), 1 / x)

    def __str__(self):
        return "Ln"


class Log(Function):
    def __init__(self, base):
        self.b = base

    def __call__(self, x):
        if isinstance(x, DualNumber):
            return DualNumber(log(x.wert, self.b), x.ableitung / (x.wert * log(self.b)))
        return DualNumber(log(x, self.b), 1 / (x * log(self.b)))

    def __str__(self):
        return "Log" + str(self.b)


class Const(Function):
    def __init__(self, n):
        self.num = n

    def __call__(self, x):
        return DualNumber(self.num, 0)

    def __str__(self):
        return str(self.num)


if __name__ == "__main__":
    f = Sin()
    g = Ln() @ Exp() @ (Id() ** 2 + Id() * 3 + Const(3))
    c = Exp() @ Ln()
    print("Funktion und Ableitung Korrekt: ", f(3), "==", sin(3), cos(3))
    print("Ableitungstest", g(1))
    print(c(4))
    print(g)

    # Darstellung
    testf = Id() ** 3 + Const(5) * Id() ** 2
    x = np.linspace(-5, 2, 100)
    y = np.zeros(len(x))
    ya = np.zeros(len(x))
    for i in range(len(x)):
        d = testf(x[i])
        y[i] = d.wert
        ya[i] = d.ableitung

    plt.plot(x, y, color="red", label="f")
    plt.plot(x, ya, color="orange", label="f´")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Funktion mit Ableitung")
    plt.legend()
    plt.show()
