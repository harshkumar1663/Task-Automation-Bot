"""
File downloading utilities.

Responsible for downloading files from URLs and saving them into the
configured download directory.

Author: Harsh Kumar
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

import requests  # type: ignore

logger = logging.getLogger(__name__)


class FileDownloader:
    """Download files from HTTP/HTTPS URLs into a local directory."""

    def __init__(self, download_dir: Path) -> None:
        self.download_dir = download_dir
        self.download_dir.mkdir(parents=True, exist_ok=True)

    def download_files(self, urls: Iterable[str]) -> list[Path]:
        """
        Download multiple files.

        Returns a list of Paths to successfully downloaded files.
        Any failed downloads are logged and skipped.
        """
        downloaded_paths: list[Path] = []

        for url in urls:
            try:
                path = self._download_single(url)
                if path:
                    downloaded_paths.append(path)
            except Exception as exc:  # noqa: BLE001
                # We don't want one failed URL to stop the whole batch.
                logger.exception("Failed to download %s: %s", url, exc)

        return downloaded_paths

    def _download_single(self, url: str) -> Path | None:
        """
        Download a single file. Returns the destination Path or None on failure.
        """
        logger.info("Downloading: %s", url)

        parsed = urlparse(url)
        filename = Path(parsed.path).name or "downloaded_file"

        dest_path = self.download_dir / filename

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with dest_path.open("wb") as f:
            f.write(response.content)

        logger.info("Downloaded %s -> %s", url, dest_path)
        return dest_path
