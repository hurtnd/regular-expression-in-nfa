import customtkinter as ctk
from RegEx import is_correct_regex, match
from PIL import Image
from os import path, sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)


class RegExGUI:
    def __init__(self):
        STICKER_SIZE = 40
        self.window = ctk.CTk()
        self.window.title("Match RE")
        try:
            self.window.iconbitmap(resource_path("../assets/icon.ico"))
        except Exception:
            self.window.iconbitmap(resource_path("assets/icon.ico"))

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.resizable(False, False)

        width = 300
        height = 300
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.window.geometry(f"{width}x{height}+{x}+{y}")

        self.regex_entry = ctk.CTkEntry(self.window, placeholder_text="Enter a regular expression",
                                        width=250, height=30)
        self.regex_entry.grid(row=0, column=0, padx=25, pady=20, sticky="ew")
        self.word_entry = ctk.CTkEntry(self.window, placeholder_text="Enter the word",
                                       width=250, height=30)
        self.word_entry.grid(row=1, column=0, padx=25, pady=0, sticky="ew")

        self.check_button = ctk.CTkButton(self.window, text="Check", command=self.check_regex)
        self.check_button.grid(row=2, column=0, padx=25, pady=20)

        def bind_enter_button(event):
            return self.check_regex()
        
        self.window.bind('<Return>', bind_enter_button)

        filenames = ["../assets/waving_hand.png", "../assets/thumbs_up.png", "../assets/thumbs_down.png"]
        images = []
        for filename in filenames:
            try:
                image = Image.open(resource_path(filename))
            except Exception:
                image = Image.open(resource_path(filename[3:]))
            images.append(ctk.CTkImage(light_image=image, size=(STICKER_SIZE, STICKER_SIZE)))

        self.startup, self.thumbs_up, self.thumbs_down = images

        self.pop_up_sticker = ctk.CTkLabel(master=self.window, image=self.startup, text="")
        self.pop_up_sticker.grid(row=3, column=0, padx=0, pady=15)

        self.result_label = ctk.CTkLabel(self.window, text="", text_color="#A9A9A9")
        self.result_label.grid()

        self.company_label = ctk.CTkLabel(self.window, text="© 2023 Mesa Research", text_color="#696969")
        self.company_label.grid()

        self.window.mainloop()

    def check_regex(self):
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
