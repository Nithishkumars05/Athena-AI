from app.settings import settings
import app.memory as memory

# Import lazily inside initialize() where appropriate
# to avoid circular imports.


class ServiceRegistry:
    """
    Central registry for Athena services.

    One shared instance exists during the application's lifetime.
    """

    def __init__(self):
        self._initialized = False

        self.settings = None
        self.memory = None
        self.dispatcher = None

        # Future services
        self.logger = None
        self.database = None
        self.ollama = None
        self.gemini = None

    def initialize(self):
        """Initialize all core services once."""

        if self._initialized:
            return

        from agents.dispatcher import dispatcher

        self.settings = settings
        self.memory = memory
        self.dispatcher = dispatcher

        self._initialized = True

    @property
    def initialized(self):
        return self._initialized


registry = ServiceRegistry()
