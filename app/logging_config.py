"""Logging configuration"""

import logging
import logging.handlers
from pathlib import Path
from app.config import settings


def setup_logging() -> None:
    """Configure application logging"""

    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(settings.log_level)

    # Create formatters
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.log_level)
    console_handler.setFormatter(detailed_formatter)
    logger.addHandler(console_handler)

    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10_000_000,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(settings.log_level)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)

    # Service-specific loggers
    service_logger = logging.getLogger("services")
    service_handler = logging.handlers.RotatingFileHandler(
        log_dir / "services.log",
        maxBytes=10_000_000,
        backupCount=5
    )
    service_handler.setFormatter(detailed_formatter)
    service_logger.addHandler(service_handler)


if __name__ == "__main__":
    setup_logging()
