"""
File management utilities.

Handles:
- Auto-renaming files with prefix/suffix patterns.
- Sorting files into subfolders by extension.

Author: Harsh Kumar
"""

from __future__ import annotations

import logging
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable

logger = logging.getLogger(__name__)


@dataclass
class FileSortConfig:
    """
    Configuration for sorting files into folders by extension.

    Keys are lowercase file extensions (including the dot), values are folder names.
    """
    extension_map: Dict[str, str] = field(default_factory=lambda: {
        ".pdf": "documents",
        ".doc": "documents",
        ".docx": "documents",
        ".txt": "documents",
        ".csv": "data",
        ".xlsx": "data",
        ".xls": "data",
        ".jpg": "images",
        ".jpeg": "images",
        ".png": "images",
        ".gif": "images",
        ".mp4": "videos",
        ".mkv": "videos",
        ".mp3": "audio",
    })
    other_folder: str = "others"


class FileManager:
    """Operations for renaming and sorting files."""

    def __init__(self, base_dir: Path, sort_config: FileSortConfig | None = None) -> None:
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.sort_config = sort_config or FileSortConfig()

    def rename_files(
        self,
        files: Iterable[Path],
        prefix: str = "",
        suffix: str = "",
    ) -> list[Path]:
        """
        Rename files by adding a prefix and/or suffix before the extension.

        Example:
        - original: report.pdf
        - prefix="2025_", suffix="_final" -> 2025_report_final.pdf
        """
        renamed_files: list[Path] = []

        for path in files:
            try:
                if not path.exists():
                    logger.warning("File not found, skipping rename: %s", path)
                    continue

                new_name = self._build_new_name(path.name, prefix, suffix)
                new_path = path.with_name(new_name)

                logger.info("Renaming %s -> %s", path.name, new_path.name)
                path.rename(new_path)
                renamed_files.append(new_path)
            except Exception as exc:  # noqa: BLE001
                logger.exception("Failed to rename file %s: %s", path, exc)

        return renamed_files

    @staticmethod
    def _build_new_name(filename: str, prefix: str, suffix: str) -> str:
        stem = Path(filename).stem
        ext = Path(filename).suffix
        return f"{prefix}{stem}{suffix}{ext}"

    def sort_files_by_extension(self, files: Iterable[Path]) -> list[Path]:
        """
        Move files into subfolders based on their extension.

        Returns a list of new Paths after moving.
        """
        sorted_files: list[Path] = []

        for path in files:
            try:
                if not path.exists():
                    logger.warning("File not found, skipping sort: %s", path)
                    continue

                ext = path.suffix.lower()
                target_folder = self.sort_config.extension_map.get(ext, self.sort_config.other_folder)
                target_dir = self.base_dir / target_folder
                target_dir.mkdir(parents=True, exist_ok=True)

                new_path = target_dir / path.name
                logger.info("Moving %s -> %s", path, new_path)
                shutil.move(str(path), str(new_path))
                sorted_files.append(new_path)
            except Exception as exc:  # noqa: BLE001
                logger.exception("Failed to move file %s: %s", path, exc)

        return sorted_files
