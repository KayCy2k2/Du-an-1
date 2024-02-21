import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class CodeSearcher:
    def __init__(self,window, code_text):
        self.window = window
        self.code_text = code_text

        # Tạo frame cho phần tìm kiếm
        self.search_frame = tk.Frame(self.window, background='lightblue')
        self.search_frame.pack(fill=tk.X)

        image5 = Image.open(r"C:\Users\KayCy\OneDrive\Desktop\VSCode\Python\TD\k3.png")
        photo5 = ImageTk.PhotoImage(image5.resize((21, 21), Image.LANCZOS))
        self.restore_button = tk.Button(self.search_frame, compound="left", width=-10, background="white", image=photo5, command=self.restore_code_text)
        self.restore_button.pack(side=tk.RIGHT, padx=10)

        image3 = Image.open(r"C:\Users\KayCy\OneDrive\Desktop\VSCode\Python\TD\h6.png")
        photo3 = ImageTk.PhotoImage(image3.resize((20, 20), Image.LANCZOS))
        self.search_button = tk.Button(self.search_frame, text="Tìm kiếm", compound="left", width=-10, background="white", image=photo3, command=self.search_and_highlight)
        self.search_button.pack(side=tk.RIGHT, padx=10)

        self.search_entry = tk.Entry(self.search_frame, font=("Arial", 12), width=30)
        self.search_entry.pack(side=tk.RIGHT, padx=10, pady=10, ipady=5)

    def search_and_highlight(self):
        search_str = self.search_entry.get().lower()  # Chuyển tất cả thành chữ thường để không phân biệt chữ hoa chữ thường
        self.code_text.tag_remove("highlight", '1.0', tk.END)  # Xóa các tag highlight hiện có trước đó
        if len(search_str) > 0:
            start_pos = '1.0'
            while True:
                start_pos = self.code_text.search(search_str, start_pos, stopindex=tk.END, nocase=True)  # Sử dụng tùy chọn 'nocase' để không phân biệt chữ hoa/chữ thường
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(search_str)}c"
                self.code_text.tag_add("highlight", start_pos, end_pos)
                start_pos = end_pos

        else:
            messagebox.showinfo("Thông báo", "Không có từ khóa cần tra")

    def restore_code_text(self):
        self.code_text.tag_remove("highlight", '1.0', tk.END)
