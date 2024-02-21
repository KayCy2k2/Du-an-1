import tkinter as tk
from tkinter import filedialog

class FileChooser:
    def __init__(self, code_text, dram_text, file_path_var, file_path_label):
        self.code_text = code_text
        self.dram_text = dram_text
        self.file_path_var = file_path_var
        self.file_path_label = file_path_label
        
    def choose_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Chọn file",
                                              filetypes=(("Python files", "*.py"), ("All files", "*.*")))
        if filename:
            self.file_path_var.set(filename)
            with open(filename, "r", encoding="utf-8") as file:
                self.dram_text.delete(1.0, tk.END)
                self.code_text.delete('1.0', tk.END)
                self.code_text.insert(tk.END, file.read())

            self.code_text.event_generate("<<LoadNewFile>>")

            # Update the file path label
            self.file_path_label.config(text=filename)
