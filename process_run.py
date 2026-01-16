from args import DownloadArgs
from options import DownloadOptions

import subprocess

class DownloadProcess:
    def __init__(self):
        self.process = None
        self.options: DownloadOptions | None = None

    def start(self):
        dl_args = DownloadArgs()
        arg_list = dl_args.create_arg_list(self.options)
        p = subprocess.Popen(arg_list, text=True)
        self.process = p