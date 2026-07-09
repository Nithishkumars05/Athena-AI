import json
from pathlib import Path


class Settings:

    def __init__(self):

        self.settings_file = (
            Path(__file__).parent / "settings.json"
        )

        self.load()

    # -------------------------
    # Load
    # -------------------------

    def load(self):

        if not self.settings_file.exists():

            self.ai_mode = "auto"
            self.model = "gemini-2.5-flash"
            self.temperature = 0.7
            self.max_history = 20

            self.save()

            return

        with open(
            self.settings_file,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        self.ai_mode = data.get(
            "ai_mode",
            "auto"
        )

        self.model = data.get(
            "model",
            "gemini-2.5-flash"
        )

        self.temperature = data.get(
            "temperature",
            0.7
        )

        self.max_history = data.get(
            "history",
            20
        )

    # -------------------------
    # Save
    # -------------------------

    def save(self):

        data = {

            "ai_mode": self.ai_mode,

            "model": self.model,

            "temperature": self.temperature,

            "history": self.max_history
        }

        with open(
            self.settings_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

    # -------------------------
    # AI Mode
    # -------------------------

    def get_ai_mode(self):
        return self.ai_mode

    def set_ai_mode(self, mode):
        self.ai_mode = mode
        self.save()

    # -------------------------
    # Model
    # -------------------------

    def get_model(self):
        return self.model

    def set_model(self, model):
        self.model = model
        self.save()

    # -------------------------
    # Temperature
    # -------------------------

    def get_temperature(self):
        return self.temperature

    def set_temperature(self, value):
        self.temperature = value
        self.save()

    # -------------------------
    # History
    # -------------------------

    def get_history(self):
        return self.max_history

    def set_history(self, value):
        self.max_history = value
        self.save()


settings = Settings()