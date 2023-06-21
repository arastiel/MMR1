from math import *
import matplotlib.pyplot as plt
import numpy as np


class Function:
    def __call__(self, x):
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


class AddFunction(Function):
    def __init__(self, f, g):
        self.f = f
        self.g = g

    def __call__(self, x):
        return self.f(x) + self.g(x)


class NegFunction(Function):
    def __init__(self, f):
        self.f = f

    def __call__(self, x):
        return -self.f(x)


class MulFunction(Function):
    def __init__(self, f, g):
        self.f = f
        self.g = g

    def __call__(self, x):
        return self.f(x) * self.g(x)


class DivFunction(Function):
    def __init__(self, f, g):
        self.f = f
        self.g = g

    def __call__(self, x):
        return self.f(x) / self.g(x)


class PowFunction(Function):
    def __init__(self, f, g):
        self.f = f
        self.g = g

    def __call__(self, x):
        return self.f(x) ** self.g(x)


class Composition(Function):
    def __init__(self, f, g):
        self.f = f
        self.g = g

    def __call__(self, x):
        return self.f(self.g(x))


class Id(Function):
    def __call__(self, x):
        return x


class Sin(Function):
    def __call__(self, x):
        return sin(x)


class Cos(Function):
    def __call__(self, x):
        return cos(x)


class Exp(Function):
    def __call__(self, x):
        return exp(x)


class Ln(Function):
    def __call__(self, x):
        return log(x)


class Log(Function):
    def __init__(self, base):
        self.b = base

    def __call__(self, x):
        return log(x, self.b)


class Const(Function):
    def __init__(self, n):
        self.num = n

    def __call__(self, x):
        return self.num


if __name__ == "__main__":
    f = Sin() / Cos() + Exp()
    g = Exp() + Id() ** 7
    a = Exp() @ Ln() @ (Id() + 3)
    b = Ln() @ Exp()
    c = Log(2) @ (Const(4) ** Id())
    f2 = Exp() @ (Id() * 2)
    print("Funktion und Verknüpfungen korrekt: ", f(42) == sin(42) / cos(42) + exp(42))
    print("Mit Zahl funktioniert(Bonus 4.2.1): ", g(5))
    print("Komposition: ", a(9), b(4), c(3))
    print(f2(3))

    # Einige Anwendungen
    f1 = Sin()
    x1 = np.linspace(0, 6.5, 100)
    y1 = np.zeros(len(x1))
    for i in range(len(x1)):
        y1[i] = f1(x1[i])
    f2 = Cos()
    x2 = np.linspace(0, 6.5, 100)
    y2 = np.zeros(len(x2))
    for i in range(len(x2)):
        y2[i] = f2(x2[i])

    fig = plt.figure()
    ax1 = fig.add_subplot(231)
    ax2 = fig.add_subplot(232)
    ax3 = fig.add_subplot(233)
    ax4 = fig.add_subplot(234)
    ax5 = fig.add_subplot(235)
    ax6 = fig.add_subplot(236)

    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.plot(x1, y1, color="#c40202")
    ax1.plot(x2, y2, color="orange")
    ax1.set_title("Sin/Cos")

    f3 = (Id() - 5) ** 2 + Const(10)
    x3 = np.linspace(0, 10, 100)
    y3 = np.zeros(len(x3))
    for i in range(len(x3)):
        y3[i] = f3(x3[i])
    ax2.plot(x3, y3, color="blue")
    ax2.set_ylabel("y")
    ax2.set_xlabel("x")
    ax2.set_title("Parabel")

    f4 = Exp()
    x4 = np.linspace(0, 10, 100)
    y4 = np.zeros(len(x4))
    for i in range(len(x4)):
        y4[i] = f4(x4[i])

    ax3.plot(x4, y4, color="green")
    ax3.set_ylabel("y")
    ax3.set_xlabel("x")
    ax3.set_title("Exp")

    f5 = Ln()
    x5 = np.linspace(0.1, 5, 100)
    y5 = np.zeros(len(x5))
    for i in range(len(x5)):
        y5[i] = f5(x5[i])

    ax4.plot(x5, y5, color="lightgreen")
    ax4.set_ylabel("y")
    ax4.set_xlabel("x")
    ax4.set_title("ln")

    f5 = Exp() @ Ln() @ Id()
    x5 = np.linspace(0, 10, 100)
    y5 = np.zeros(len(x5))
    for i in range(len(x5)):
        y5[i] = f5(x5[i])

    ax5.plot(x5, y5, color="green")
    ax5.set_ylabel("y")
    ax5.set_xlabel("x")
    ax5.set_title("Exp(ln(x))=x")

    f6 = Id() ** 3 + (Id() ** 2) * 6 + Sin() @ (Id() ** 2)
    x6 = np.linspace(-6, 2, 100)
    y6 = np.zeros(len(x6))
    for i in range(len(x6)):
        y6[i] = f6(x6[i])

    ax6.plot(x6, y6, color="green")
    ax6.set_ylabel("y")
    ax6.set_xlabel("x")
    ax6.set_title("Irgendwas")
    plt.show()
