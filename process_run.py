from args import DownloadArgs
from options import DownloadOptions
import subprocess
import json
import threading


class DownloadProcess:
    def __init__(self, options):
        self.process_reference = None
        self.options: DownloadOptions = options

    def start(self):
        dl_args = DownloadArgs()
        arg_list = dl_args.create_arg_list(self.options)
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!{arg_list}")        
        self.p = subprocess.Popen(arg_list, text=True, bufsize=1,stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        self.process_reference = self.p

        

    @staticmethod
    def analyze(url) -> dict:
        analyze_args = DownloadArgs()
        arg_list = analyze_args.create_analyze_args(url)
        p = subprocess.Popen(arg_list, text=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout_text, stderr_text = p.communicate()
        
        if p.returncode != 0:
            error_msg = stderr_text if stderr_text else stdout_text
            if error_msg:
                raise RuntimeError(error_msg.strip())
            
        if not stdout_text.strip():
            raise ValueError("stdout is empty")
        data = json.loads(stdout_text)
        if not isinstance(data, dict):
            raise ValueError("yt-dlp analyze returned unexpected JSON type")

        return data
        