"""
Configuration handling for the Task Automation Bot.

Loads configuration from a JSON file under config/settings.json.
Provides a typed Config object for the rest of the codebase.

Author: Harsh Kumar
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass
class EmailConfig:
    enabled: bool = False
    smtp_server: str = "smtp.example.com"
    smtp_port: int = 587
    use_tls: bool = True
    username: str = ""
    password: str = ""
    from_address: str = ""
    to_addresses: List[str] = field(default_factory=list)


@dataclass
class Config:
    download_urls: List[str]
    download_dir: Path
    working_dir: Path
    reports_dir: Path
    logs_dir: Path
    rename_prefix: str
    rename_suffix: str
    sort_by_extension: bool
    email: EmailConfig

    @staticmethod
    def default() -> "Config":
        """Return default configuration values for local testing."""
        return Config(
            download_urls=[],
            download_dir=BASE_DIR / "downloads",
            working_dir=BASE_DIR / "downloads",
            reports_dir=BASE_DIR / "reports",
            logs_dir=BASE_DIR / "logs",
            rename_prefix="",
            rename_suffix="",
            sort_by_extension=True,
            email=EmailConfig(),
        )


def load_config(path: Optional[Path] = None) -> Config:
    """
    Load configuration from JSON file. If file is missing or invalid,
    fall back to default configuration.

    This is deliberately defensive to avoid hard crashes in production.
    """
    if path is None:
        path = BASE_DIR / "config" / "settings.json"

    if not path.exists():
        # File not found -> return default config
        return Config.default()

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        # Invalid JSON -> fall back to default
        return Config.default()

    email_data = data.get("email", {})
    email_cfg = EmailConfig(
        enabled=email_data.get("enabled", False),
        smtp_server=email_data.get("smtp_server", "smtp.example.com"),
        smtp_port=email_data.get("smtp_port", 587),
        use_tls=email_data.get("use_tls", True),
        username=email_data.get("username", ""),
        password=email_data.get("password", ""),
        from_address=email_data.get("from_address", ""),
        to_addresses=email_data.get("to_addresses", []),
    )

    cfg = Config(
        download_urls=data.get("download_urls", []),
        download_dir=Path(data.get("download_dir", BASE_DIR / "downloads")),
        working_dir=Path(data.get("working_dir", BASE_DIR / "downloads")),
        reports_dir=Path(data.get("reports_dir", BASE_DIR / "reports")),
        logs_dir=Path(data.get("logs_dir", BASE_DIR / "logs")),
        rename_prefix=data.get("rename_prefix", ""),
        rename_suffix=data.get("rename_suffix", ""),
        sort_by_extension=data.get("sort_by_extension", True),
        email=email_cfg,
    )

    return cfg
