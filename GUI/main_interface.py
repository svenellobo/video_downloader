import customtkinter as ctk

class MainInterface(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid()
        self.parent = parent
        #self.parent.columnconfigure(0, weight=1)
        #self.parent.rowconfigure(0, weight=1)
        
        self.init_screen()

    def init_screen(self):
        main_frame = ctk.CTkFrame(self, fg_color="#2B2B2B", width=800,height=600)
        main_frame.grid(row=0, column=0, padx=5, pady=5)
        main_frame.grid_propagate(False)

        url_enter = ctk.CTkEntry(main_frame, placeholder_text="Enter url here")
        url_enter.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        url_enter_btn = ctk.CTkButton(main_frame)

