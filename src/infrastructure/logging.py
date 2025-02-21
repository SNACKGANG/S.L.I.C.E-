from pathlib import Path

from loguru import logger


class LoguruConfig:
    def __init__(
        self,
        log_dir="logs",
        log_file="app.log",
        console_level="INFO",
        file_level="DEBUG",
    ):
        self.LOG_DIR = Path(log_dir)
        self.LOG_DIR.mkdir(exist_ok=True)
        self.log_file = self.LOG_DIR / log_file
        self.console_level = console_level
        self.file_level = file_level

    def setup_logging(self):
        logger.add(
            self.log_file,
            rotation="10 MB",
            retention="5 days",
            compression="zip",
            encoding="utf-8",
            level=self.file_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {file}:{line} - {message}",
        )

        logger.disable("discord")
        logger.info("Loguru successfully configured!")
