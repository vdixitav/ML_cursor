# Structured logs
# Design goals (production-grade)

# Structured logs (machine-readable)

# Human-friendly console output

# File logging for audits

# Easy integration with LangGraph & agents

# Zero external infra dependency (Phase-1)


import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

from rich.logging import RichHandler

# log directory
LOG_DIR=Path("logs")
LOG_DIR.mkdir(exist_ok=True)

DEFAULT_LOG_FILE=LOG_DIR/"ml_cursor.log"


def _build_file_handler(log_file: Path)->logging.FileHandler:
    """
    File handler for persistent audit logs.
    """
    handler = logging.FileHandler(log_file, encoding="utf-8")
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    return handler


def get_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
) -> logging.Logger:
    """
    Create or fetch a configured logger.

    Parameters
    ----------
    name : str
        Logger name (usually __name__).
    level : int
        Logging level (INFO by default).
    log_file : Optional[Path]
        Custom log file path. Defaults to logs/ml_cursor.log

    Returns
    -------
    logging.Logger
    """
    logger = logging.getLogger(name)

    # Prevent duplicate handlers in reloads / notebooks
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # Console handler (rich, human-friendly)
    console_handler = RichHandler(
        rich_tracebacks=True,
        show_time=True,
        show_level=True,
        show_path=False,
    )

    # File handler (audit-safe)
    file_handler = _build_file_handler(log_file or DEFAULT_LOG_FILE)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False
    return logger