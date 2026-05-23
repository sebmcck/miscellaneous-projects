# Clipboard Auto-Saver

A small Python/Tkinter desktop utility that watches the clipboard and saves copied text and images locally.

## Features

- Start/stop clipboard monitoring from a simple GUI
- Save copied text into daily log files
- Save copied images as timestamped PNG files
- Store all captured content locally in a `logs/` folder

## Run from source

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python clipboard_autosaver.py
```

