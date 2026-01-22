from dataclasses import dataclass
from pathlib import Path


@dataclass
class DownloadOptions:
    url: str | None = None
    saving_folder: Path | None = None
    audio_only: bool = False
    audio_format: str = "bestaudio"
    video_format: str = "bestvideo"
    
