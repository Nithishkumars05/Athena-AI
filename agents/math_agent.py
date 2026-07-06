"""
Athena AI - Math Agent
Offline mathematical reasoning using SymPy.
"""

from sympy import (
    symbols,
    sympify,
    solve,
    simplify,
    diff,
    integrate,
    factor,
    expand
)

# Default variable
x = symbols("x")


def solve_equation(expression: str):
    """
    Solve equations like:
    x**2 + 5*x + 6
    """

    expr = sympify(expression)
    return solve(expr, x)


def simplify_expression(expression: str):
    expr = sympify(expression)
    return simplify(expr)


def differentiate_expression(expression: str):
    expr = sympify(expression)
    return diff(expr, x)


def integrate_expression(expression: str):
    expr = sympify(expression)
    return integrate(expr, x)


def factor_expression(expression: str):
    expr = sympify(expression)
    return factor(expr)


def expand_expression(expression: str):
    expr = sympify(expression)
    return expand(expr)

if __name__ == "__main__":

    print("Equation:", solve_equation("x**2 + 5*x + 6"))

    print("Simplify:",
          simplify_expression("(x**2-1)/(x-1)"))

    print("Derivative:",
          differentiate_expression("x**3 + 4*x"))

    print("Integral:",
          integrate_expression("x**2"))

    print("Factor:",
          factor_expression("x**2+5*x+6"))

    print("Expand:",
          expand_expression("(x+2)**3"))