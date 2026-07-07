"""
Athena AI - Math Agent
Offline mathematical reasoning using SymPy.
"""

import re

from sympy import (
    symbols,
    solve,
    simplify,
    diff,
    integrate,
    factor,
    expand,
    Eq
)

from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)

# Default variable
x = symbols("x")

transformations = (
    standard_transformations
    + (implicit_multiplication_application,)
)


def preprocess_expression(expression: str) -> str:
    """
    Convert user-friendly math into SymPy-compatible syntax.
    """

    expression = expression.strip().lower()

    # Remove common command words
    for word in [
        "solve",
        "calculate",
        "find",
        "evaluate",
        "equation",
    ]:
        expression = expression.replace(word, "")

    expression = expression.strip()

    # Unicode powers
    expression = expression.replace("²", "**2")
    expression = expression.replace("³", "**3")

    # Allow ^
    expression = expression.replace("^", "**")

    return expression


def parse_math(expression: str):
    expression = preprocess_expression(expression)

    if "=" in expression:
        left, right = expression.split("=", 1)

        left_expr = parse_expr(
            left,
            transformations=transformations
        )

        right_expr = parse_expr(
            right,
            transformations=transformations
        )

        return Eq(left_expr, right_expr)

    return parse_expr(
        expression,
        transformations=transformations
    )


def solve_equation(expression: str):
    print("DEBUG:", expression)

    expr = parse_math(expression)

    if isinstance(expr, Eq):
        result = solve(expr, x)
    else:
        result = solve(expr, x)

    if not result:
        return "No solution found."

    return "Solutions: " + ", ".join(map(str, result))


def simplify_expression(expression: str):
    expr = parse_math(expression)
    return simplify(expr)


def differentiate_expression(expression: str):
    expr = parse_math(expression)
    return diff(expr, x)


def integrate_expression(expression: str):
    expr = parse_math(expression)
    return integrate(expr, x)


def factor_expression(expression: str):
    expr = parse_math(expression)
    return factor(expr)


def expand_expression(expression: str):
    expr = parse_math(expression)
    return expand(expr)

def handle(user_name: str, message: str) -> str:
    return solve_equation(message)


if __name__ == "__main__":

    print(solve_equation("Solve x² + 5x + 6 = 0"))

    print(solve_equation("2x + 5 = 9"))

    print(simplify_expression("(x**2-1)/(x-1)"))

    print(differentiate_expression("x^3 + 4x"))

    print(integrate_expression("x²"))

    print(factor_expression("x²+5x+6"))

    print(expand_expression("(x+2)^3"))