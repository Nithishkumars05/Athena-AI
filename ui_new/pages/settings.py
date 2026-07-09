from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QComboBox,
    QSlider,
    QSpinBox,
    QGroupBox,
    QMessageBox
)

from PySide6.QtCore import Qt

from app.settings import settings



class SettingsPage(QWidget):

    def __init__(self):

        super().__init__()

        self.create_ui()

        self.load_settings()



    def create_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            30,
            30,
            30,
            30
        )

        layout.setSpacing(20)



        # Title

        title = QLabel(
            "⚙ Settings"
        )

        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
        """)

        layout.addWidget(title)



        # AI Group

        ai_group = QGroupBox(
            "AI Settings"
        )

        ai_layout = QVBoxLayout()
        # AI Mode

        mode_row = QHBoxLayout()

        mode_row.addWidget(
            QLabel("AI Mode")
        )

        self.mode_box = QComboBox()

        self.mode_box.addItems(
            [
                "auto",
                "cloud",
                "offline"
            ]
        )

        mode_row.addWidget(
            self.mode_box
        )

        ai_layout.addLayout(
            mode_row
        )


        # Model

        model_row = QHBoxLayout()

        model_row.addWidget(
            QLabel("Model")
        )


        self.model_box = QComboBox()

        self.model_box.addItems(
            [
                "gemini-2.5-flash",
                "qwen3:8b",
                "qwen2.5-coder:7b",
                "qwen3:14b"
            ]
        )


        model_row.addWidget(
            self.model_box
        )

        ai_layout.addLayout(
            model_row
        )



        # Temperature

        temp_row = QHBoxLayout()

        temp_row.addWidget(
            QLabel("Temperature")
        )


        self.temp_slider = QSlider(
            Qt.Horizontal
        )

        self.temp_slider.setRange(
            0,
            100
        )


        temp_row.addWidget(
            self.temp_slider
        )


        ai_layout.addLayout(
            temp_row
        )



        # History

        history_row = QHBoxLayout()


        history_row.addWidget(
            QLabel("Max History")
        )


        self.history_box = QSpinBox()

        self.history_box.setRange(
            5,
            100
        )


        history_row.addWidget(
            self.history_box
        )


        ai_layout.addLayout(
            history_row
        )


        ai_group.setLayout(
            ai_layout
        )


        layout.addWidget(
            ai_group
        )



        # Save button

        self.save_button = QPushButton(
            "Save Settings"
        )


        self.save_button.clicked.connect(
            self.save_settings
        )


        layout.addWidget(
            self.save_button
        )


        layout.addStretch()



    def load_settings(self):

        self.mode_box.setCurrentText(
            settings.get_ai_mode()
        )

        self.model_box.setCurrentText(
            settings.get_model()
        )

        self.temp_slider.setValue(
            int(
                settings.get_temperature()
            *   100
            )
        )

        self.history_box.setValue(
            settings.get_history()
        )


    def save_settings(self):

        settings.set_ai_mode(
            self.mode_box.currentText()
        )

        settings.set_model(
            self.model_box.currentText()
        )

        settings.set_temperature(
            self.temp_slider.value() / 100
        )

        settings.set_history(
            self.history_box.value()
        )

        QMessageBox.information(
            self,
            "Athena AI",
            "Settings saved"
        )

        print("Settings Updated")