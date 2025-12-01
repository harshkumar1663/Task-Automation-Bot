<<<<<<< HEAD
# Task Automation Bot

**Author:** Harsh Kumar  
**Role Target:** Python Developer / Automation Engineer

---

## Project Purpose

The **Task Automation Bot** is a production-style Python automation project
designed to showcase real-world skills that a Python Developer or Automation
Engineer would use in a workplace environment.

It automates a small but realistic workflow:

1. Downloading files from external URLs.
2. Renaming the files according to a consistent pattern.
3. Sorting files into folders by type.
4. Generating a CSV report with details of all processed files.
5. Optionally sending a summary email with the report attached.

The codebase is modular, logged, and structured in a way that mirrors
a junior-level production automation tool.

---

## Features

- **Automatic file downloading** from configurable URLs.
- **Auto-renaming** of files using customizable prefix/suffix.
- **File sorting** into subfolders based on file extension.
- **CSV report generation** (file name, extension, size, folder).
- **Optional email notification** using SMTP, with CSV report attached.
- **Defensive error handling** – failures in one step do not crash everything.
- **Logging** to both console and file (`logs/automation_bot.log`).

---

## Folder Structure

```text
task-automation-bot/
├─ automation_bot/
│  ├─ __init__.py           # Package metadata
│  ├─ config.py             # Configuration loading and types
│  ├─ file_downloader.py    # Download logic
│  ├─ file_manager.py       # Renaming and sorting
│  ├─ report_generator.py   # CSV report generation
│  └─ notifier.py           # Email notifications
├─ config/
│  ├─ settings.example.json # Example configuration
│  └─ settings.json         # Your real configuration (not committed)
├─ downloads/               # Downloaded files
├─ logs/                    # Log files
├─ reports/                 # Generated CSV reports
├─ task_automation_bot.py   # Main orchestration script
├─ requirements.txt
└─ README.md
=======
# Task-Automation-Bot
>>>>>>> 5f16873fe70bed5362eb6418afc73654b1cb41a7
