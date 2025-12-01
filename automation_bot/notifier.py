"""
Email notification utilities.

Allows sending a simple summary email with optional attachment.

Author: Harsh Kumar
"""

from __future__ import annotations

import logging
import smtplib
from email.message import EmailMessage
from pathlib import Path

from .config import EmailConfig

logger = logging.getLogger(__name__)


class EmailNotifier:
    """Send email notifications with optional attachments."""

    def __init__(self, config: EmailConfig) -> None:
        self.config = config

    def send_notification(self, subject: str, body: str, attachment: Path | None = None) -> None:
        """
        Send an email notification if email is enabled.

        If disabled, this function just logs and returns.
        """
        if not self.config.enabled:
            logger.info("Email notifications are disabled. Skipping send.")
            return

        if not self.config.to_addresses:
            logger.warning("Email enabled but no recipients configured. Skipping send.")
            return

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.config.from_address
        msg["To"] = ", ".join(self.config.to_addresses)
        msg.set_content(body)

        if attachment is not None and attachment.exists():
            logger.info("Attaching file to email: %s", attachment)
            with attachment.open("rb") as f:
                data = f.read()
            msg.add_attachment(
                data,
                maintype="text",
                subtype="csv",
                filename=attachment.name,
            )

        try:
            logger.info("Connecting to SMTP server %s:%s", self.config.smtp_server, self.config.smtp_port)
            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port, timeout=30) as server:
                if self.config.use_tls:
                    server.starttls()
                if self.config.username and self.config.password:
                    server.login(self.config.username, self.config.password)
                server.send_message(msg)
            logger.info("Notification email sent successfully.")
        except Exception as exc:  # noqa: BLE001
            # Email failure should not crash the bot.
            logger.exception("Failed to send notification email: %s", exc)
