import tkinter as tk
import os
import subprocess
import threading
from tkinter import messagebox

class CodeViewer:
    def __init__(self, code_frame):
        self.code_frame = code_frame
        self.framed = None
        self.upper_frame = None
        self.lower_frame = None
        self.moving_out = False

        self.frame_width = 230
        self.frame_height = self.code_frame.winfo_screenheight() // 2

    def move_in(self):
        x = self.framed.winfo_x()
        if x > self.code_frame.winfo_screenwidth() - self.frame_width:
            self.framed.place(x=x - 10, y=0)
            self.framed.after(10, self.move_in)

    def move_out(self):
        x = self.framed.winfo_x()
        if x < self.code_frame.winfo_screenwidth():
            self.framed.place(x=x + 10, y=0)
            self.framed.after(10, self.move_out)
        else:
            self.framed.place_forget()

    def on_arrow_click(self, direction):
        if self.moving_out:
            self.moving_out = False
            self.move_out()
        else:
            self.moving_out = True
            self.move_in()

    def load_folders(self, folders, a):
        # Tạo khung trên để lưu trữ thư mục
        self.upper_frame = tk.Frame(self.framed, bg='white')
        self.upper_frame.grid(row=0, column=1, sticky="nsew")  # Sử dụng grid()

        self.upper_frame.rowconfigure(0, weight=60)  # Thêm cấu hình để cho phép khung tự mở rộng chiều cao

        scrollbar_upper_frame = tk.Scrollbar(self.upper_frame)  # Thêm thanh cuộn cho khung trên
        scrollbar_upper_frame.pack(side=tk.RIGHT, fill=tk.Y)

        folder_listbox = tk.Listbox(self.upper_frame, yscrollcommand=scrollbar_upper_frame.set)
        folder_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for folder, i in zip(folders, a):
            folder_name = os.path.basename(folder)
            folder_label = tk.Label(folder_listbox, text=i, width=25, bg='white')
            folder_label.pack()

            def on_folder_click(event, f=folder):
                self.load_files(f)

            folder_label.bind('<Button-1>', on_folder_click)

        scrollbar_upper_frame.config(command=folder_listbox.yview)

        # Tạo khung dưới để hiển thị các tệp trong thư mục
        self.lower_frame = tk.Frame(self.framed, bg='white')
        self.lower_frame.grid(row=1, column=1, sticky="nsew")  # Sử dụng grid()

        lower_frame1 = tk.Frame(self.lower_frame, bg='red')
        lower_frame1.pack(fill=tk.BOTH, expand=True)

        scrollbar_lower_frame = tk.Scrollbar(lower_frame1)  # Thêm thanh cuộn
        scrollbar_lower_frame.pack(side=tk.RIGHT, fill=tk.Y)

        file_listbox = tk.Listbox(lower_frame1, width=30, yscrollcommand=scrollbar_lower_frame.set)
        file_listbox.pack(fill=tk.BOTH, expand=True)

        scrollbar_lower_frame.config(command=file_listbox.yview)

        def get_selected_file():
            selected_file_index = file_listbox.curselection()[0]  # Lấy chỉ mục của tệp được chọn
            selected_file = self.files[selected_file_index]
            file_path = os.path.join(folder, selected_file)  # Tạo đường dẫn của tệp

            with open(file_path, "r", encoding="utf-8") as file:
                self.dram_text.delete(1.0, tk.END)
                self.code_text.delete('1.0', tk.END)
                self.code_text.insert(tk.END, file.read())

            self.code_text.event_generate("<<LoadNewFile>>")

            # Update the file path label
            self.file_path_label.config(text=file_path)

            filename = file_path
            if filename:
                def run_process():
                    process = subprocess.Popen(["python", filename], shell=True, stderr=subprocess.STDOUT,
                                               universal_newlines=True, stdout=subprocess.PIPE)
                    output, _ = process.communicate()
                    returncode = process.returncode

                thread = threading.Thread(target=run_process)
                thread.start()
            else:
                messagebox.showwarning("Thông báo", "Lỗi tệp không chạy được")

        select_button = tk.Button(self.lower_frame, text="Select", command=get_selected_file)
        select_button.pack(side=tk.LEFT, pady=5)  # Đặt select_button sang trái

    def create_code_viewer(self, dram_text, code_text, file_path_label):
        self.framed = tk.Frame(self.code_frame, width=self.frame_width, height=self.frame_height, bg='red', bd=3)
        self.framed.place(x=self.code_frame.winfo_screenwidth(), y=0)

        close_button1 = tk.Button(self.framed, text=">", command=lambda: self.on_arrow_click('left'))
        close_button1.grid(row=0, column=0, padx=2, sticky="nsew")

        self.moving_out = False

        # Lưu trữ các đối tượng để sử dụng trong phương thức khác.
        self.dram_text = dram_text
        self.code_text = code_text
        self.file_path_label = file_path_label

        # Tạo khung trên để lưu trữ thư mục
        self.upper_frame = tk.Frame(self.framed, bg='white')
        self.upper_frame.grid(row=0, column=1, sticky="nsew")  # Sử dụng grid()

        self.load_folders()  # Nạp các thư mục vào khung trên

        # Tạo khung dưới để hiển thị các tệp trong thư mục
        self.lower_frame = tk.Frame(self.framed, bg='white')
        self.lower_frame.grid(row=1, column=1, sticky="nsew")  # Sử dụng grid()

        self.framed.grid_rowconfigure(0, weight=1)
        self.framed.grid_rowconfigure(1, weight=1)


# Example usage:
root = tk.Tk()
code_frame = tk.Frame(root)
code_frame.pack()

dram_text = tk.Text(code_frame)  # Tạo đối tượng dram_text
code_text = tk.Text(code_frame)  # Tạo đối tượng code_text
file_path_label = tk.Label(code_frame)  # Tạo đối tượng file_path_label

viewer = CodeViewer(code_frame)
viewer.create_code_viewer(dram_text, code_text, file_path_label)

root.mainloop()
