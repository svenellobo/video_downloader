from dataclasses import dataclass
from pathlib import Path

@dataclass
class DownloadOptions:
    url: str
    saving_folder: Path
