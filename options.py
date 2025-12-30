from dataclasses import dataclass
from pathlib import Path


@dataclass
class DownloadOptions:
    url: str
    saving_folder: Path 
    audio_only: bool = False
    audio_format: str = "bestaudio"
    video_format: str = "bestvideo"
    
