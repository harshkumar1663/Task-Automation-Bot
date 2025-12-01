"""
CSV report generation utilities.

Generates a report summarizing processed files, including:
- file name
- extension
- size (bytes)
- folder

Author: Harsh Kumar
"""

from __future__ import annotations

import csv
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

logger = logging.getLogger(__name__)


@dataclass
class FileInfo:
    path: Path

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def extension(self) -> str:
        return self.path.suffix.lower()

    @property
    def size_bytes(self) -> int:
        try:
            return self.path.stat().st_size
        except FileNotFoundError:
            return 0

    @property
    def folder(self) -> str:
        return self.path.parent.name


class ReportGenerator:
    """Generate CSV reports for processed files."""

    def __init__(self, reports_dir: Path) -> None:
        self.reports_dir = reports_dir
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_file_report(self, files: Iterable[Path], output_name: str) -> Path:
        """
        Generate a CSV report for the provided files.

        Returns the path to the generated CSV file.
        """
        report_path = self.reports_dir / output_name
        file_infos = [FileInfo(path=f) for f in files]

        logger.info("Generating report: %s", report_path)

        with report_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["file_name", "extension", "size_bytes", "folder"])
            for info in file_infos:
                writer.writerow([info.name, info.extension, info.size_bytes, info.folder])

        logger.info("Report generated: %s", report_path)
        return report_path
