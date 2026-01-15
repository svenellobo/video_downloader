from options import DownloadOptions
class download_args:
    def __init__(self):
        self.args_list: list = list[str]
        

    def create_arg_list(self, options=DownloadOptions()):
        if not options.url:
            raise ValueError("No URL provided")        

        
        if not options.saving_folder:
            raise ValueError("No destination folder provided")
        
        output_path = options.saving_folder / "%(title)s.%(ext)s"
        self.args_list.extend(("uv", "run", "yt-dlp"))
        
        if options.audio_only:
            if options.audio_only == True:
                self.args_list.append("-x")
                

        self.args_list.extend(("-o", str(output_path)))
        