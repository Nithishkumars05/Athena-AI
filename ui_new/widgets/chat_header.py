from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QPushButton,
)

from PySide6.QtCore import (
    Qt,
    Signal,
)


class ChatHeader(QFrame):

    export_requested = Signal()

    def __init__(
        self,
        title="🦉 Athena AI",
        subtitle="Your Personal AI Engineer"
    ):

        super().__init__()

        self.setFixedHeight(85)

        self.setStyleSheet("""
        QFrame{
            background-color:#202123;
            border-bottom:1px solid #3a3a3a;
        }

        QLabel#title{
            color:white;
            font-size:18px;
            font-weight:bold;
        }

        QLabel#subtitle{
            color:#A0A0A0;
            font-size:12px;
        }

        QLabel#status{
            color:#42d66b;
            font-size:13px;
            font-weight:bold;
        }

        QLabel#model{
            color:#8FAAFF;
            font-size:12px;
        }

        QPushButton{
            background:#2F3136;
            color:white;
            border:1px solid #444;
            border-radius:6px;
            padding:6px 14px;
        }

        QPushButton:hover{
            background:#3A3D42;
        }

        QPushButton:pressed{
            background:#242629;
        }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)

        # =====================================
        # Left Section
        # =====================================

        left = QVBoxLayout()

        self.title = QLabel(title)
        self.title.setObjectName("title")

        self.subtitle = QLabel(subtitle)
        self.subtitle.setObjectName("subtitle")

        left.addWidget(self.title)
        left.addWidget(self.subtitle)

        layout.addLayout(left)
        layout.addStretch()

        # =====================================
        # Right Section
        # =====================================

        right = QVBoxLayout()
        right.setAlignment(Qt.AlignRight)

        top_row = QHBoxLayout()
        top_row.setAlignment(Qt.AlignRight)

        self.export_btn = QPushButton("⬇ Export")
        self.export_btn.setCursor(Qt.PointingHandCursor)
        self.export_btn.clicked.connect(
            self.export_requested.emit
        )

        top_row.addWidget(self.export_btn)

        right.addLayout(top_row)

        self.status = QLabel("● Online")
        self.status.setObjectName("status")
        self.status.setAlignment(Qt.AlignRight)

        self.model = QLabel("Model: Auto")
        self.model.setObjectName("model")
        self.model.setAlignment(Qt.AlignRight)

        right.addWidget(self.status)
        right.addWidget(self.model)

        layout.addLayout(right)

    # =====================================
    # Public API
    # =====================================

    def set_title(
        self,
        text: str
    ):
        self.title.setText(text)

    def set_subtitle(
        self,
        text: str
    ):
        self.subtitle.setText(text)

    def set_status(
        self,
        text: str
    ):
        self.status.setText(text)

    def set_model(
        self,
        model_name: str
    ):
        self.model.setText(
            f"Model: {model_name}"
        )