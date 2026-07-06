from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class MetricCard(QFrame):

    def __init__(self, title, value, subtitle=""):
        super().__init__()

        self.setObjectName("Card")
        self.setMinimumHeight(120)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        title_label = QLabel(title.upper())
        title_label.setStyleSheet(
            "font-size:12px;"
            "color:#9498A4;"
            "font-weight:bold;"
        )

        value_label = QLabel(str(value))
        value_label.setStyleSheet(
            "font-size:28px;"
            "font-weight:bold;"
        )

        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet(
            "font-size:11px;"
            "color:#3DDC97;"
        )

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(subtitle_label)
        layout.addStretch()