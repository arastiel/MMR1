from math import *
import numpy as np
import matplotlib.pyplot as plt
from Aufgabe4_2_2 import *


def get_expr(s):
    e = s
    if "(" in s:
        i1 = s.index("(")
        i2 = s.index(")")
        st = s[i1:i2 + 1]
        s = s.replace(st, "")
        st = "".join(st.split("("))
        st = "".join(st.split(")"))
        e = "@ " + s + " " + st

    expr = e.split(" ")
    return expr


def parser_simple(expr):
    """Parst einfache Ausdrücke der Länge 3 oder 1(Zeichen Expr Expr)"""
    if expr == "sin":
        return Sin()
    if expr == "cos":
        return Cos()
    if expr == "exp":
        return Exp()
    if expr == "ln":
        return Ln()
    if "log" in expr:
        e = expr.replace("log", "")
        return Log(int(e))
    if expr[0] == "x":
        return Id()
    if expr[0] == "-" and type(expr) == str:
        e1 = expr[1]
        if not isinstance(e1, Function):
            e1 = parser_simple(expr[1])
        return NegFunction(e1)
    if type(expr) == list:
        e1 = expr[1]
        e2 = expr[2]
        if not isinstance(e1, Function):
            e1 = parser_simple(expr[1])
        if not isinstance(e2, Function):
            e2 = parser_simple(expr[2])
        if expr[0] == "+":
            return AddFunction(e1, e2)
        if expr[0] == "-":
            return AddFunction(e1, NegFunction(e2))
        if expr[0] == "*":
            return MulFunction(e1, e2)
        if expr[0] == "**":
            return PowFunction(e1, e2)
        if expr[0] == "/":
            return DivFunction(e1, e2)
        if expr[0] == "@":
            return Composition(e1, e2)
    else:
        if "." in expr:
            return Const(float(expr))
        return Const(int(expr))


def parser(expr):
    """Parst beliebigen Ausdruck in polnischer notation"""
    # Rekursionsabbrüche
    if len(expr) == 3:
        return parser_simple(expr)
    if len(expr) == 1:
        return parser_simple(expr[0])

    # Teilbestimmungen Unterscheidung gleichgewichtete/ungleichgewichtete Ausdrücke
    # als nach zb (* + 2 3 + 4 5), (* +2 3 5), (* 5 + 2 8)
    if len(expr[1:]) > 3:
        t = ceil(len(expr) / 2)
        if len(expr[1:]) % 3:
            t += 1
        e1 = expr[1:t]
        e2 = expr[t:]

        if e1[0] not in ["+", "-", "*", "**", "/", "@"]:
            e1 = expr[1:t - 2]
            e2 = expr[t - 2:]

        if e2[0] not in ["+", "-", "*", "**", "/", "@"] and len(e2)>1:
            i = 1
            while e2[0] not in ["+", "-", "*", "**", "/", "@"] and len(e2) > 1:
                e1 = expr[1:t+i]
                e2 = expr[t+i:]
                i += 1

        e1 = parser(e1)
        e2 = parser(e2)
        return parser([expr[0], e1, e2])
    return parser([expr[0], parser(expr[1:])])


def Parser(s):
    """Wandelt gegebenen polischen Ausdruck von String in Liste um und parst diesen"""
    expr = get_expr(s)
    return parser(expr)


if __name__ == "__main__":
    e1 = get_expr("+ 123 52.5")
    f1 = parser_simple(e1)
    print(f1, f1(1))
    s2 = "* + x 3 + x 5"  # (x+3)*(x+5)
    s3 = "* + x 3 5"  # (x+3)*5
    f2 = Parser(s2)
    f3 = Parser(s3)
    print(f2, f2(4))
    print(f3, f3(6))

    g1 = Parser("+ log10 / x sin")
    print(g1, g1(100))

    g2 = Parser("+ 3 @ sin x")
    print(g2, g2(1))

    g3 = Parser("sin(+ x 3)")
    print(g3, g3(0))

    g4 = Parser("exp(@ sin ** x 2)")
    print(g4, g4(10))

    d1 = "+ ** x 2 ** x 3"
    d2 = "+ + ** x 2 ** x 3 6"
    d3 = "@ sin + x 4"
    d4 = "+ sin(** x 2) x"
    h1 = Parser(d4)
    print(h1)
