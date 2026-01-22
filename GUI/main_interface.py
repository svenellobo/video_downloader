import customtkinter as ctk
from options import DownloadOptions
from process_run import DownloadProcess
from tkinter import filedialog
from pathlib import Path
from tkinter import messagebox

class MainInterface(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid()
        self.parent = parent
        #self.parent.columnconfigure(0, weight=1)
        #self.parent.rowconfigure(0, weight=1)
        
        self.download_process_reference = None
        self.selected_folder : Path | None = None
        
        self.init_screen()

    def init_screen(self):
        main_frame = ctk.CTkFrame(self, fg_color="#2B2B2B", width=800,height=600)
        main_frame.grid(row=0, column=0, padx=5, pady=5)
        main_frame.grid_propagate(False)

        self.url_enter = ctk.CTkEntry(main_frame, placeholder_text="Enter url here")
        self.url_enter.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        url_enter_btn = ctk.CTkButton(main_frame, text="Download", command=self.video_download)
        url_enter_btn.grid(row=1, column=0, padx=5, pady=5)

        self.choose_folder_btn = ctk.CTkButton(main_frame, text="Choose Folder", command=self.choose_folder)
        self.choose_folder_btn.grid(row=2, column=0, padx=5, pady=5)

        self.audio_only_var = ctk.BooleanVar(value="false")
        checkbox = ctk.CTkCheckBox(main_frame, text="Audio Only", variable=self.audio_only_var)
        checkbox.grid(row=3, column=0, padx=5, pady=5)
        

        self.folder_label = ctk.CTkLabel(main_frame, text="No folder selected")
        self.folder_label.grid(row=5, column=0, padx=5, pady=5)


    def video_download(self):
        options: DownloadOptions = self.create_options()
        if options:
            download_process = DownloadProcess(options)
            self.download_process_reference = download_process
            download_process.start()
            self.url_enter.delete(0, "end")
            

    def create_options(self) -> DownloadOptions | None:
        download_options = DownloadOptions()
        download_options.url = self.url_enter.get().strip()
        
        download_options.audio_only = self.audio_only_var.get()
        if self.selected_folder is None:
            messagebox.showwarning(title="Missing path", message="No folder detected")
            return
        elif not self.selected_folder.exists():
            messagebox.showwarning(title="Wrong path", message="Chosen folder does not exist")
            return
        elif not self.selected_folder.is_dir():
            messagebox.showwarning(title="Wrong path", message="Selected path is not a folder")
            return

        download_options.saving_folder = self.selected_folder
        return download_options
            


    def choose_folder(self):
        folder = filedialog.askdirectory(title="Select download folder")
        if folder:
            self.selected_folder = Path(folder)
            self.folder_label.configure(text=folder)

    


