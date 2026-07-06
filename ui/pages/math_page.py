from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QTextBrowser, QLabel
)
from PySide6.QtCore import Qt

from formatter.math_formatter import format_math
from sympy import sympify


class MathPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        # Title
        title = QLabel("Mathematics Engine")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:22px; font-weight:bold;")

        # Input
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter equation (e.g., x^2 + 2x + 1)")

        # Button
        self.solve_button = QPushButton("Solve")
        self.solve_button.clicked.connect(self.solve_math)

        # Output
        self.output_box = QTextBrowser()

        self.layout.addWidget(title)
        self.layout.addWidget(self.input_box)
        self.layout.addWidget(self.solve_button)
        self.layout.addWidget(self.output_box)

        self.setLayout(self.layout)

    def solve_math(self):

        from sympy.parsing.sympy_parser import (
            parse_expr,
            standard_transformations,
            implicit_multiplication_application,
            convert_xor
    )

        from formatter.math_formatter import format_math

        expr = self.input_box.text().strip()

        if not expr:
            return

        try:
            transformations = (
            standard_transformations +
            (implicit_multiplication_application, convert_xor)
        )

        # -----------------------------
        # SymPy evaluation
        # -----------------------------
            result = parse_expr(expr, transformations=transformations)

        # -----------------------------
        # INPUT formatting
        # -----------------------------
            formatted_input = format_math(expr)

        # -----------------------------
        # OUTPUT normalization (IMPORTANT FIX)
        # -----------------------------
            raw_result = str(result)

            normalized_result = (
                raw_result
                .replace("**", "^")
                .replace("Pow", "")
                .replace("Mul", "")
                .replace("(", "")
                .replace(")", "")
        )

            formatted_result = format_math(normalized_result)

        # -----------------------------
        # DISPLAY
        # -----------------------------
            self.output_box.append(f"Input: {formatted_input}")
            self.output_box.append(f"Result: {formatted_result}")
            self.output_box.append("-" * 40)

        except Exception as e:
            self.output_box.append(f"Error: {str(e)}")