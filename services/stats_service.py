from pathlib import Path


class StatsService:

    BASE_DIR = Path(__file__).resolve().parent.parent

    OUTPUTS = BASE_DIR / "outputs"
    DOCS = BASE_DIR / "docs"

    @staticmethod
    def report_count():
        if not StatsService.OUTPUTS.exists():
            return 0

        return len([
            f for f in StatsService.OUTPUTS.iterdir()
            if f.is_file()
        ])

    @staticmethod
    def document_count():
        if not StatsService.DOCS.exists():
            return 0

        return len([
            f for f in StatsService.DOCS.iterdir()
            if f.is_file()
        ])

    @staticmethod
    def chat_count():
        # Will be implemented later
        return 0

    @staticmethod
    def math_count():
        # Will be implemented later
        return 0