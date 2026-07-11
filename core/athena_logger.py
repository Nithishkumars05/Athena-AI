import logging
from pathlib import Path


# -----------------------------
# Create logs folder
# -----------------------------
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

log_file = logs_dir / "athena.log"


# -----------------------------
# Create Logger
# -----------------------------
athena_logger = logging.getLogger("Athena")

# Prevent duplicate handlers
if not athena_logger.handlers:

    athena_logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File
    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    athena_logger.addHandler(console_handler)
    athena_logger.addHandler(file_handler)