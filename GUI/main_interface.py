import customtkinter as ctk
from options import DownloadOptions
from process_run import DownloadProcess
from output_parser import OutputParser
from tkinter import filedialog
from pathlib import Path
from tkinter import messagebox
import threading

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
        main_frame = ctk.CTkFrame(self, fg_color="#ffffff", width=800,height=600)
        main_frame.grid(row=0, column=0, padx=5, pady=5)
        main_frame.grid_propagate(False)

        self.url_enter = ctk.CTkEntry(main_frame, placeholder_text="Enter url here")
        self.url_enter.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        self.download_btn = ctk.CTkButton(main_frame, text="Download", command=self.start_download)
        self.download_btn.grid(row=1, column=0, padx=5, pady=5)

        self.choose_folder_btn = ctk.CTkButton(main_frame, text="Choose Folder", command=self.choose_folder)
        self.choose_folder_btn.grid(row=2, column=0, padx=5, pady=5)

        self.audio_only_var = ctk.BooleanVar(value=False)
        checkbox = ctk.CTkCheckBox(main_frame, text="Audio Only", variable=self.audio_only_var)
        checkbox.grid(row=3, column=0, padx=5, pady=5)
        

        self.folder_label = ctk.CTkLabel(main_frame, text="No folder selected")
        self.folder_label.grid(row=5, column=0, padx=5, pady=5)

        self.progress_bar = ctk.CTkProgressBar(main_frame)
        self.progress_bar.grid(row=6, column=1, padx=5, pady=5)

        self.progress_display = ctk.CTkLabel(main_frame, text="")
        self.progress_display.grid(row=6, column=0, padx=5, pady=5)

        

        #analysis metadata display
        self.analyze_btn = ctk.CTkButton(main_frame, text="Analyze", command=self.analyze_btn_press)
        self.analyze_btn.grid(row=7, column=0, padx=5, pady=5)

        analysis_display_frame = ctk.CTkFrame(self)
        analysis_display_frame.grid(row=1, column=0, padx=5, pady=5)

        self.analysis_title_lbl = ctk.CTkLabel(analysis_display_frame, text="")
        self.analysis_title_lbl.grid(row=1, column=0, padx=5, pady=5)

        self.analysis_duration_lbl = ctk.CTkLabel(analysis_display_frame, text="")
        self.analysis_duration_lbl.grid(row=2, column=0, padx=5, pady=5)

        self.analysis_thumbnail_lbl = ctk.CTkLabel(analysis_display_frame, text="")
        self.analysis_thumbnail_lbl.grid(row=0, column=0, padx=5, pady=5)

        self.analysis_size_lbl = ctk.CTkLabel(analysis_display_frame, text="")
        self.analysis_size_lbl.grid(row=4, column=0, padx=5, pady=5)


    def start_download(self):
        options = self.create_options()
        if not options:
            return
        self.url_enter.delete(0, "end")
        self.download_btn.configure(state="disabled")
        threading.Thread(target=self.download_running, args=(options,), daemon=True).start()


    def download_running(self, options: DownloadOptions):
        try:   
            download_process = DownloadProcess(options)
            self.download_process_reference = download_process
            download_process.start()            

            for line in download_process.process_reference.stdout:
                line: str = line.strip()
                print(line, flush=True)
                self.after(0, lambda l=line: self.progress_display.configure(text=l))

            rc= download_process.process_reference.wait()
            self.after(0, lambda: self.progress_display.configure(text="Download finished" if rc == 0 else f"Download failed (rc={rc})"))
            self.after(0, lambda: self.download_btn.configure(state="normal"))

        except Exception as e:
            self.after(0, lambda: self.download_btn.configure(state="normal"))
            self.after(0, lambda: self.progress_display.configure(text=f"Download failed: {str(e)}"))

    def analyze_btn_press(self):
        url = self.url_enter.get().strip()
        if not url:
            messagebox.showwarning(title="Url field is empty", message="Please enter the url")
            return
        
        self.analyze_btn.configure(state="disabled")
        self.analysis_title_lbl.configure(text="Analyzing...")

        threading.Thread(target=self.analyze_process, args=(url,), daemon=True).start()

    def analyze_process(self, url: str):

        try:
            data = DownloadProcess.analyze(url)
            analysis_data = OutputParser.parse(data)

            title = self.title_format(analysis_data.get("title")) or "N/A"
            duration = self.duration_format(analysis_data.get("duration"))
            size = self.size_format(analysis_data.get("filesize_approx"))
            #self.analysis_thumbnail_lbl.configure(text=analysis_data.get("thumbnail"))

            self.after(0, lambda:self.update_analysis_info(title, duration, size))

        except Exception as e:
            self.after(0, lambda: self.show_analyze_error(str(e)))
        
        

    def update_analysis_info(self, title: str, duration: str, size: str):
        self.analysis_title_lbl.configure(text=title)
        self.analysis_duration_lbl.configure(text=duration)
        self.analysis_size_lbl.configure(text=size)
        self.analyze_btn.configure(state="normal")

    def show_analyze_error(self, msg: str):
        self.analyze_btn.configure(state="normal")
        messagebox.showerror(title="Something went wrong", message=msg)
            
            

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

    def title_format(self, title: str | None) -> str:
        if title is None:
            return "N/A"
        
        title = str(title)
        if len(title) > 50:
            return f"{title[:50]}..."
        return title


    def duration_format(self, seconds: int | None) -> str:
        if seconds is None:
            return "N/A"
        
        seconds = int(seconds)
        if seconds < 0:
            return "N/A"
        
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60

        return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
    
    
    def size_format(self, size: int | None) -> str:
        if size is None:
            return "N/A"
        
        file_size = float(size)

        if file_size < 0:
            return "N/A"
        
        units = ["B", "KB", "MB", "GB"]
        i = 0
        while file_size >= 1000 and i < len(units) - 1:
            file_size /= 1000
            i += 1

        if i == 0:
            return f"{int(file_size)} {units[i]}"
        return f"{file_size:.1f} {units[i]}"


    


    


