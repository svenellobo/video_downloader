from options import DownloadOptions
class DownloadArgs:  

    def create_arg_list(self, options: DownloadOptions) -> list[str]:
        args_list: list[str] = []

        if not options.url:
            raise ValueError("No URL provided")        

        
        if not options.saving_folder:
            raise ValueError("No destination folder provided")
        
        output_path = options.saving_folder / "%(title)s.%(ext)s"
        args_list.extend(("uv", "run", "yt-dlp"))
        
        
        if options.audio_only:
            args_list.append("-x")


        args_list.extend(("-o", str(output_path)))

        return args_list
        