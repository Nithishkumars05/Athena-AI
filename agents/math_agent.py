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
    Eq,
)

from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)

x = symbols("x")

transformations = (
    standard_transformations
    + (implicit_multiplication_application,)
)


# --------------------------------------------------
# Preprocessing
# --------------------------------------------------

def preprocess_expression(expression: str) -> str:

    expression = expression.lower().strip()

    words = [

        "solve",
        "calculate",
        "find",
        "evaluate",
        "equation",
        "what is",
        "compute",
        "differentiate",
        "derivative of",
        "integrate",
        "factor",
        "expand",

    ]

    for word in words:
        expression = expression.replace(word, "")

    expression = expression.strip()

    expression = expression.replace("^", "**")
    expression = expression.replace("²", "**2")
    expression = expression.replace("³", "**3")

    return expression


# --------------------------------------------------
# Parser
# --------------------------------------------------

def parse_math(expression: str):

    expression = preprocess_expression(expression)

    if "=" in expression:

        left, right = expression.split("=", 1)

        return Eq(

            parse_expr(
                left,
                transformations=transformations,
            ),

            parse_expr(
                right,
                transformations=transformations,
            ),

        )

    return parse_expr(

        expression,

        transformations=transformations,

    )


# --------------------------------------------------
# Operations
# --------------------------------------------------

def solve_equation(expression: str):

    expr = parse_math(expression)

    # Pure arithmetic
    if not isinstance(expr, Eq) and len(expr.free_symbols) == 0:
        return f"Answer: {expr.evalf()}"

    result = solve(expr, x)

    if not result:
        return "No solution found."

    return "Solutions: " + ", ".join(map(str, result))


def simplify_expression(expression: str):

    return str(
        simplify(
            parse_math(expression)
        )
    )


def differentiate_expression(expression: str):

    return str(
        diff(
            parse_math(expression),
            x,
        )
    )


def integrate_expression(expression: str):

    return str(
        integrate(
            parse_math(expression),
            x,
        )
    )


def factor_expression(expression: str):

    return str(
        factor(
            parse_math(expression)
        )
    )


def expand_expression(expression: str):

    return str(
        expand(
            parse_math(expression)
        )
    )


# --------------------------------------------------
# Dispatcher
# --------------------------------------------------

def handle(
    user_name: str,
    message: str,
) -> str:

    text = message.lower()

    if "differentiate" in text or "derivative" in text:
        return differentiate_expression(message)

    if "integrate" in text:
        return integrate_expression(message)

    if "factor" in text:
        return factor_expression(message)

    if "expand" in text:
        return expand_expression(message)

    if "simplify" in text:
        return simplify_expression(message)

    return solve_equation(message)


if __name__ == "__main__":

    tests = [

        "Calculate 25*87",

        "Solve x^2+5x+6=0",

        "Differentiate x^3+4x",

        "Integrate x^2",

        "Factor x^2+5x+6",

        "Expand (x+2)^3",

    ]

    for test in tests:

        print(test)

        print(handle("User", test))

        print()