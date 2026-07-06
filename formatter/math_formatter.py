"""
Mathematical formatter for Athena AI.
Converts math expressions into readable Unicode format.
"""

import re

from formatter.unicode_map import (
    SUPERSCRIPT,
    SUBSCRIPT,
    GREEK,
    SYMBOLS
)


# -----------------------------
# Helpers
# -----------------------------

def to_superscript(text: str) -> str:
    return "".join(SUPERSCRIPT.get(ch, ch) for ch in text)


def to_subscript(text: str) -> str:
    return "".join(SUBSCRIPT.get(ch, ch) for ch in text)


# -----------------------------
# Main Formatter
# -----------------------------

def format_math(text: str) -> str:

    if not text:
        return text

    # -----------------------------
    # Normalize SymPy-style output
    # -----------------------------
    text = (
        text
        .replace("**", "^")   # exponent fix
        .replace("Pow", "")    # remove SymPy noise
        .replace("Mul", "")
        .replace("(", "")
        .replace(")", "")
    )

    # -----------------------------
    # Replace symbols (basic math operators)
    # -----------------------------
    for normal, symbol in SYMBOLS.items():
        text = text.replace(normal, symbol)

    # -----------------------------
    # Replace Greek letters (alpha, beta, theta...)
    # -----------------------------
    for word, greek in GREEK.items():
        text = re.sub(
            rf"\b{word}\b",
            greek,
            text,
            flags=re.IGNORECASE
        )

    # -----------------------------
    # Superscript conversion (x^2 → x²)
    # FIXED for multi-digit exponents
    # -----------------------------
    text = re.sub(
        r"\^([^\s^_()]+)",
        lambda m: to_superscript(m.group(1)),
        text
    )

    # -----------------------------
    # Subscript conversion (x_1 → x₁)
    # -----------------------------
    text = re.sub(
        r"_([A-Za-z0-9]+)",
        lambda m: to_subscript(m.group(1)),
        text
    )

    # -----------------------------
    # sqrt(x) → √x
    # -----------------------------
    text = re.sub(
        r"sqrt\s*([a-zA-Z0-9]+)",
        r"√\1",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"sqrt\((.*?)\)",
        r"√(\1)",
        text,
        flags=re.IGNORECASE
    )

    # -----------------------------
    # Final cleanup spacing
    # -----------------------------
    text = re.sub(r"\s+", " ", text).strip()

    return text


# -----------------------------
# Self Test
# -----------------------------

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
        "x**2 + 2*x"
    ]

    for test in tests:
        print(f"{test}  --->  {format_math(test)}")