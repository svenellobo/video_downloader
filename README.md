# Video Downloader

A simple desktop application for downloading videos and audio using yt-dlp.

This is a small portfolio project built to practice threading and subprocess management in Python. The focus is on running yt-dlp as a subprocess, reading its output in real time, and keeping the GUI responsive by handling all background work on separate threads.

## Features

- Download video or audio from any site supported by yt-dlp
- Analyze a URL before downloading to preview the title, duration, thumbnail, and file size
- Real time download progress bar
- Cancel an ongoing download

## Requirements

- Python 3.12 or higher
- uv

## Installation and running

Sync the environment and then run with uv:

```
uv sync
uv run main.py
```

## Dependencies

- yt-dlp
- customtkinter
- Pillow

## Code quality
Linted and formatted with ruff.