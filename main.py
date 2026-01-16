import customtkinter as ctk
from GUI.main_interface import MainInterface

class App(ctk.CTk):

    def __init__(self, title: str):
        super().__init__()
        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        
        self.create_screen()

    def create_screen(self):
        MainInterface(self)


if __name__ == "__main__":
    app = App("Video Downloader")
    app.mainloop()
