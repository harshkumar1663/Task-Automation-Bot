"""
Task Automation Bot

Orchestrates a real-world style automation workflow:

1. Download files from configured URLs.
2. Rename files using a prefix/suffix pattern.
3. Sort files into folders by file type.
4. Generate a CSV report summarizing processed files.
5. Optionally send an email notification with the report attached.

Author: Harsh Kumar
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from automation_bot.config import load_config
from automation_bot.file_downloader import FileDownloader
from automation_bot.file_manager import FileManager, FileSortConfig
from automation_bot.report_generator import ReportGenerator
from automation_bot.notifier import EmailNotifier


def setup_logging(logs_dir: Path) -> None:
    """Configure logging for both console and file."""
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "automation_bot.log"

    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)


def main() -> None:
    """Entry point for the Task Automation Bot."""
    config = load_config()
    setup_logging(config.logs_dir)

    logger = logging.getLogger(__name__)
    logger.info("Starting Task Automation Bot")

    try:
        # 1. Download files
        downloader = FileDownloader(config.download_dir)
        downloaded_files = downloader.download_files(config.download_urls)
        logger.info("Downloaded %d files.", len(downloaded_files))

        # 2. Rename files with prefix/suffix
        file_manager = FileManager(config.working_dir, sort_config=FileSortConfig())

        renamed_files = file_manager.rename_files(
            files=downloaded_files,
            prefix=config.rename_prefix,
            suffix=config.rename_suffix,
        )
        logger.info("Renamed %d files.", len(renamed_files))

        # 3. Sort files by extension (if enabled)
        if config.sort_by_extension:
            sorted_files = file_manager.sort_files_by_extension(renamed_files)
        else:
            sorted_files = renamed_files

        logger.info("Sorted %d files.", len(sorted_files))

        # 4. Generate CSV report
        now_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        report_name = f"file_report_{now_str}.csv"
        report_generator = ReportGenerator(config.reports_dir)
        report_path = report_generator.generate_file_report(sorted_files, report_name)

        # 5. Optional email notification
        notifier = EmailNotifier(config.email)
        subject = "Task Automation Bot - File Processing Report"
        body = (
            f"Task Automation Bot has completed processing.\n\n"
            f"Total URLs configured: {len(config.download_urls)}\n"
            f"Files downloaded: {len(downloaded_files)}\n"
            f"Files renamed: {len(renamed_files)}\n"
            f"Files sorted: {len(sorted_files)}\n"
            f"Report path: {report_path}\n"
        )
        notifier.send_notification(subject=subject, body=body, attachment=report_path)

        logger.info("Task Automation Bot completed successfully.")
    except Exception as exc:  # noqa: BLE001
        # Top-level catch to ensure we log any unexpected crash.
        logger = logging.getLogger(__name__)
        logger.exception("Task Automation Bot encountered a fatal error: %s", exc)


if __name__ == "__main__":
    main()
