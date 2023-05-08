import customtkinter as ctk
from RegEx import is_correct_regex, match
from PIL import Image
from os import path


class RegExGUI:
    def __init__(self):
        STICKER_SIZE = 30
        self.window = ctk.CTk()
        self.window.title("Match RE")
        self.window.iconbitmap('assets/icon.ico')

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.resizable(False, False)

        width = 350
        height = 250
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.window.geometry(f"{width}x{height}+{x}+{y}")

        self.regex_entry = ctk.CTkEntry(self.window, placeholder_text="Enter a regular expression",
                                        width=250, height=30)
        self.regex_entry.pack(pady=15)

        self.word_entry = ctk.CTkEntry(self.window, placeholder_text="Enter the word",
                                       width=250, height=30)
        self.word_entry.pack()

        self.check_button = ctk.CTkButton(self.window, text="Check", command=self.check_regex)
        self.check_button.pack(pady=15)
        self.window.bind('<Return>', self.check_regex)

        self.startup = ctk.CTkImage(light_image=Image.open(path.join("assets/waving_hand.png")), 
                                    size=(STICKER_SIZE, STICKER_SIZE))
        self.thumbs_up = ctk.CTkImage(light_image=Image.open(path.join("assets/thumbs_up.png")), 
                                      size=(STICKER_SIZE, STICKER_SIZE))
        self.thumbs_down = ctk.CTkImage(light_image=Image.open(path.join("assets/thumbs_down.png")), 
                                        size=(STICKER_SIZE, STICKER_SIZE))
        self.pop_up_sticker = ctk.CTkLabel(master=self.window, image=self.startup, text="")
        self.pop_up_sticker.pack(pady=10)

        self.result_label = ctk.CTkLabel(self.window, text="", text_color="#A9A9A9")
        self.result_label.pack()

        self.company_label = ctk.CTkLabel(self.window, text="© 2023 Mesa Research", text_color="#696969")
        self.company_label.pack()

        self.window.mainloop()

    def check_regex(self, event):
        regex = self.regex_entry.get()
        word = self.word_entry.get()
        if not is_correct_regex(regex):
            self.pop_up_sticker.configure(image=self.thumbs_down)
            self.result_label.configure(text="Invalid regular expression")
            return
        if word == "":
            self.pop_up_sticker.configure(image=self.thumbs_down)
            self.result_label.configure(text=f"Enter the word")
        else:
            if match(regex, word):
                self.pop_up_sticker.configure(image=self.thumbs_up)
                self.result_label.configure(text=f"The word belongs to a regular expression")
            else:
                self.pop_up_sticker.configure(image=self.thumbs_down)
                self.result_label.configure(text=f"The word doesn't belong to a regular expression")
