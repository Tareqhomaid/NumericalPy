from math import *
import sympy as sp
from flask import flash


def derive(f):
    x = sp.Symbol('x')

    # get the derivative of the function
    dfdx = sp.diff(f(x), x)
    f = sp.lambdify(x, dfdx)
    return f


def fd(f, p):
    f = derive(f)
    return f(p)


def check_sign(f, a, b):
    fa = f(a)
    fb = f(b)
    if fa > 0 and fb < 0:
        return b, a
    elif fa < 0 and fb > 0:
        return a, b
    else:
        return None


class Solver:
    def __init__(self, f, a=None, b=None, c=None, d=None, x0=None, p0=None):
        try:
            self.text = f
            self.f = eval("lambda x:" + f)
        except SyntaxError:
            flash("Syntax Error, Have you tried n*x instead of nx or you missed a ')' ?")
            self.f = None
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.x0 = x0
        self.p0 = p0

    def bisection(self, tol=1*10**-6, max_iter=1000):
        x_val = []
        f = self.f
        i = 1
        a = self.a
        b = self.b
        try:
            a, b = check_sign(f, a, b)
        except TypeError:
            flash(f"Invalid interval fa={f(a)}, fb = {f(b)} for the function {self.text}")
            return ""
        c0 = 0
        while True:
            c = (a + b) / 2
            fc = f(c)
            if fc > 0:
                b = c
            elif fc < 0:
                a = c
            else:
                flash(f"fc = 0, c = {c}")

            x_val.append(f"p[{i}] is: " + str(c))
            if abs(c - c0) < tol:
                return c, x_val
            i += 1
            if i > max_iter:
                flash("Maximum number of iterations exceeded")
                return None, []
            c0 = c

    def fixedpoint(self, tol=1e-6, max_iter=1000):
        x0 = self.x0
        f = self.f
        if not f:
            return None, []
        x_val = []
        i = 1
        while True:
            x = f(x0)
            x_val.append(f"p[{i}] is: " + str(x))
            if abs(x - x0) < tol:
                return x, x_val
            elif abs(x - x0) >= 10:
                flash(f"The sequence is not convergent for f(x0) = {f(x0)}")
                return None, x_val
            i += 1
            if i > max_iter:
                flash("Maximum number of iterations exceeded")
                return None, []
            x0 = x

    def false_position(self, tol=1e-6, max_iter=1000):
        x_val = []
        f = self.f
        a = self.c
        b = self.d
        a, b = check_sign(f, a, b)
        c0 = 0
        n = 1
        while True:
            c = (b - (f(b) * (b - a)) / (f(b) - f(a)))
            fc = f(c)
            if fc > 0:
                b = c
            elif fc < 0:
                a = c
            else:
                return c
            x_val.append(f"p[{n}] is: " + str(c))
            if fabs(c - c0) < tol:
                return c, x_val
            n += 1
            if n > max_iter:
                flash("Maximum number of iterations exceeded")
                return None, []
            c0 = c

    def newton_raphson(self, tol=1e-6, itr=100):
        x_val = []
        f = self.f
        p0 = self.p0
        i = 1
        while True:
            p = p0 - f(p0) / fd(f, p0)
            x_val.append(f"p[{i}] is: " + str(p))
            i += 1
            if i >= itr:
                break
            if abs(p - p0) < tol:
                return p, x_val
            p0 = p
