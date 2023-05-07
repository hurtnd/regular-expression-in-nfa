import customtkinter as ctk
from RegEx import is_correct_regex, match


class RegExGUI:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Match RE")
        self.window.iconbitmap('icon.ico')

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.resizable(False, False)

        width = 400
        height = 250
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.window.geometry(f"{width}x{height}+{x}+{y}")

        self.regex_entry = ctk.CTkEntry(self.window, placeholder_text="Enter a regular expression",
                                        width=250, height=30)
        self.regex_entry.pack(pady=20)

        self.word_entry = ctk.CTkEntry(self.window, placeholder_text="Enter the word",
                                       width=250, height=30)
        self.word_entry.pack()

        self.check_button = ctk.CTkButton(self.window, text="Check", command=self.check_regex)
        self.check_button.pack(pady=20)

        self.result_label = ctk.CTkLabel(self.window, text="")
        self.result_label.pack(pady=15)

        self.window.mainloop()

    def check_regex(self):
        regex = self.regex_entry.get()
        word = self.word_entry.get()
        if not is_correct_regex(regex):
            self.result_label.configure(text="Invalid regular expression")
            return
        if word == "":
            self.result_label.configure(text=f"Enter the word")
        else:
            if match(regex, word):
                self.result_label.configure(
                    text=f"The word belongs to a regular expression")
            else:
                self.result_label.configure(
                    text=f"The word doesn't belong to a regular expression")
