"""
Mathematical formatter for Athena AI.
"""

import re

from formatter.unicode_map import (
    SUPERSCRIPT,
    SUBSCRIPT,
    GREEK,
    SYMBOLS
)


def to_superscript(text: str) -> str:
    return "".join(SUPERSCRIPT.get(ch, ch) for ch in text)


def to_subscript(text: str) -> str:
    return "".join(SUBSCRIPT.get(ch, ch) for ch in text)


def format_math(text: str) -> str:

    # -----------------------------
    # Replace symbols
    # -----------------------------

    for normal, symbol in SYMBOLS.items():
        text = text.replace(normal, symbol)

    # -----------------------------
    # Replace Greek names
    # -----------------------------

    for word, greek in GREEK.items():
        text = re.sub(
            rf"\b{word}\b",
            greek,
            text,
            flags=re.IGNORECASE
        )

    # -----------------------------
    # x^2 → x²
    # -----------------------------

    text = re.sub(
        r"\^([A-Za-z0-9+\-=()]+)",
        lambda m: to_superscript(m.group(1)),
        text
    )

    # -----------------------------
    # x_1 → x₁
    # -----------------------------

    text = re.sub(
        r"_([A-Za-z0-9+\-=()]+)",
        lambda m: to_subscript(m.group(1)),
        text
    )

    # -----------------------------
    # sqrt(x) → √(x)
    # -----------------------------

    text = re.sub(
        r"sqrt\((.*?)\)",
        r"√(\1)",
        text,
        flags=re.IGNORECASE
    )

    return text


# ---------------------------------
# Testing
# ---------------------------------

if __name__ == "__main__":

    tests = [
        "x^2",
        "x^10",
        "x_1",
        "A_25",
        "sqrt(x)",
        "alpha + beta",
        "theta >= pi",
        "x != y",
        "a +- b",
        "E = mc^2",
    ]

    for test in tests:
        print(f"{test}  --->  {format_math(test)}")