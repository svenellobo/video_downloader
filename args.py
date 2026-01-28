from pathlib import Path
from options import DownloadOptions


class DownloadArgs:  

    def create_arg_list(self, options: DownloadOptions) -> list[str]:
        args_list: list[str] = []

        if not options.url:
            raise ValueError("No URL provided")        

        
        if not options.saving_folder:
            raise ValueError("No destination folder provided")
        
        output_path: Path = options.saving_folder / "%(title)s.%(ext)s"
        args_list.extend(("uv", "run", "yt-dlp", "--newline", "--no-color", "--progress"))
        args_list.extend(("--trim-filenames", "180", "--restrict-filenames"))
        
        
        if options.audio_only:
            args_list.append("-x")
            #args_list.extend(("--audio-format", "mp3"))


        args_list.extend(("-o", str(output_path)))
        args_list.append(options.url)

        return args_list
    
    def create_analyze_args(self, url) -> list[str]:
        analyze_list = []

        if not url:
            raise ValueError("No URL provided")
        analyze_list.extend(("uv", "run", "yt-dlp", "-J", "--no-playlist", "--no-color", "--quiet", url))
        return analyze_list
        