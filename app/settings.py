class Settings:

    def __init__(self):

        
    # AI configuration
        self.ai_mode = "auto"      # cloud | offline | auto
        self.model = "gemini-2.5-flash"
        self.temperature = 0.7

    # Conversation memory
        self.max_history = 20
    # -------------------------
    # Model
    # -------------------------
    # -------------------------
# AI Mode
# -------------------------

    def get_ai_mode(self):

        return self.ai_mode


    def set_ai_mode(self, mode):

        self.ai_mode = mode
    def get_model(self):

        return self.model


    def set_model(self, model):

        self.model = model



    # -------------------------
    # Temperature
    # -------------------------

    def get_temperature(self):

        return self.temperature


    def set_temperature(self, value):

        self.temperature = value



    # -------------------------
    # History
    # -------------------------

    def get_history(self):

        return self.max_history


    def set_history(self, value):

        self.max_history = value



# Global settings object
settings = Settings()