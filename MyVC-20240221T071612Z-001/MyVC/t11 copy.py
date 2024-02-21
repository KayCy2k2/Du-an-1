import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import os, ast
from PIL import ImageTk, Image
import to11_5, to12, to13, to15

def choose_file():
    filename = filedialog.askopenfilename(initialdir="/", title="Chọn file",
                                          filetypes=(("Python files", "*.py"), ("All files", "*.*")))
    if filename:
        file_path.set(filename)
        with open(filename, "r", encoding="utf-8") as file:
            dram_text.delete(1.0, tk.END)
            code_text.delete('1.0', tk.END)
            code_text.insert(tk.END, file.read())

        code_text.event_generate("<<LoadNewFile>>")

        # Update the file path label
        file_path_label.config(text=filename)

def run_file():
    filename = file_path.get()
    if filename:
        def run_process():
            process = subprocess.Popen(["python", filename], shell=True, stderr=subprocess.STDOUT, universal_newlines=True, stdout=subprocess.PIPE)

            # Đợi quá trình hoàn thành và lấy output
            output, _ = process.communicate()

            # Kiểm tra mã trạng thái của quá trình
            returncode = process.returncode

            # Hiển thị kết quả trong khung DRAM
            dram_text.delete(1.0, tk.END)
            dram_text.insert(tk.END, output)

        # Hiển thị phần draw_text
        show_dram_text()
            
        # Tạo một luồng mới để chạy quá trình
        thread = threading.Thread(target=run_process)
        thread.start()
    else:
        messagebox.showwarning("Thông báo", "Lỗi tệp không chạy được")

def search_and_highlight():
    search_str = search_entry.get().lower()  # Chuyển tất cả thành chữ thường để không phân biệt chữ hoa chữ thường
    code_text.tag_remove("highlight", '1.0', tk.END)  # Xóa các tag highlight hiện có trước đó
    if len(search_str) > 0:
        if search_str:
            start_pos = '1.0'
            while True:
                start_pos = code_text.search(search_str, start_pos, stopindex=tk.END, nocase=True)  # Sử dụng tùy chọn 'nocase' để không phân biệt chữ hoa/chữ thường
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(search_str)}c"
                code_text.tag_add("highlight", start_pos, end_pos)
                start_pos = end_pos

    else:
        messagebox.showinfo("Thông báo", "Không có từ khóa cần tra")

def restore_code_text():
    code_text.tag_remove("highlight", '1.0', tk.END)
    
def new_code_text():
    code_text.delete('1.0', tk.END)
    clear_file_path_label()   
    dram_text.delete(1.0, tk.END)  # Xóa nội dung hiện tại trong khung DRAM
    dram_frame.pack_forget()  # Đóng phần draw_text lại
    
def create_new_tab():
    new_tab = tk.Toplevel(window)
    new_tab.title("Tab Mới")
    
    # Tạo một khung Scrollbar cho khung Text
    scrollbar = tk.Scrollbar(new_tab)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Tạo một khung Text để viết ghi chú
    text_area = tk.Text(new_tab, font=("Arial", 13), yscrollcommand=scrollbar.set)
    text_area.pack(side=tk.LEFT, fill=tk.BOTH)
    
    # Kết nối Scrollbar với khung Text
    scrollbar.config(command=text_area.yview)
    
    # Thêm nội dung mặc định vào khung Text (nếu muốn)
    default_note = "Viết ghi chú ở đây..."
    text_area.insert(tk.END, default_note)
    
    # Xóa nội dung mặc định khi người dùng nhập kí tự
    def clear_default_text(event):
        if text_area.get(1.0, "end-1c") == default_note:
            text_area.delete(1.0, tk.END)
            
    # Hiển thị nội dung mặc định khi không có kí tự
    def show_default_text(event):
        if not text_area.get(1.0, "end-1c"):
            text_area.insert(tk.END, default_note)
    
    # Gắn các hàm xử lý sự kiện vào khung Text
    text_area.bind("<KeyPress>", clear_default_text)
    text_area.bind("<FocusOut>", show_default_text)
    
def save_file():
    filename = file_path.get()
    if filename:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(code_text.get('1.0', tk.END))
        messagebox.showinfo("Thông báo", "Tệp đã được lưu: {}".format(filename))  # Thông báo đường dẫn đã được lưu
    else:
        messagebox.showwarning("Thông báo", "Không có tệp để lưu")

def save_file_as():
    filename = filedialog.asksaveasfilename(initialdir="/", title="Lưu file",
                                            filetypes=(("Python files", "*.py"), ("All files", "*.*")))
    if filename:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(code_text.get('1.0', tk.END))
        messagebox.showinfo("Thông báo", "Tệp đã được lưu: {}".format(filename))  # Thông báo đường dẫn đã được lưu

def clear_file_path_label():
    file_path_label.config(text="")

def close_app():
    window.destroy()

def show_about():
    messagebox.showinfo("About", "Thông tin ứng dụng ViewsCode 1.0")

def show_guide():
    guide_text = '''
    Hướng dẫn sử dụng:
    - Bước 1: Nhập mã vào ô văn bản.
    - Bước 2: Chọn tệp tin cần chạy hoặc lưu tệp tin.
    - Bước 3: Nhấn Run để chạy mã hoặc Save để lưu tệp tin.
    
    Lưu ý: DRAM sẽ hiển thị kết quả của quá trình chạy mã.
    '''
    messagebox.showinfo("Hướng dẫn sử dụng", guide_text)

def open_notes_tab():
    notes_tab = tk.Toplevel(window)
    notes_tab.title("Tab Ghi Chú")
    # Thêm các thành phần cho tab ghi chú ở đây
    
def show_dram_text():
    dram_frame.pack(fill=tk.BOTH, expand=True)

window = tk.Tk()
window.title("ViewsCode")
window.geometry("600x400")
image1 = Image.open(r"C:\Users\KayCy\OneDrive\Desktop\VSCode\Python\TD\logovkc.png")
photo1 = ImageTk.PhotoImage(image1.resize((100, 100), Image.LANCZOS))
window.iconphoto(True, photo1)

file_path = tk.StringVar()
#----------------------------------------------------------------------------------------------------------------------------
def check_syntax():
    code = code_text.get("1.0", tk.END)
    try:
        ast.parse(code)
        error_label.config(text="Không có lỗi cú pháp.", fg="green")
    except SyntaxError as e:
        error_message = f"Lỗi cú pháp: {e}"
        error_label.config(text=error_message, fg="red")
        
# Tạo frame cho phần tìm kiếm
search_frame = tk.Frame(window, background='lightblue')
search_frame.pack(fill=tk.X)

image5 = Image.open(r"C:\Users\KayCy\OneDrive\Desktop\VSCode\Python\TD\k3.png")
photo5 = ImageTk.PhotoImage(image5.resize((21, 21), Image.LANCZOS))
restore_button = tk.Button(search_frame, compound="left", width=-10, background="white", image=photo5, command=restore_code_text)
restore_button.pack(side=tk.RIGHT, padx=10)

image3 = Image.open(r"C:\Users\KayCy\OneDrive\Desktop\VSCode\Python\TD\h6.png")
photo3 = ImageTk.PhotoImage(image3.resize((20, 20), Image.LANCZOS))
search_button = tk.Button(search_frame, text="Tìm kiếm", compound="left", width=-10, background="white", image=photo3, command=search_and_highlight)
search_button.pack(side=tk.RIGHT, padx=10)

search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)
search_entry.pack(side=tk.RIGHT, padx=10, pady=10, ipady=5)

# Tạo nút "Kiểm tra" để kiểm tra lỗi cú pháp
image6 = Image.open(r"C:\Users\KayCy\OneDrive\Desktop\VSCode\Python\TD\d2.png")
photo6 = ImageTk.PhotoImage(image6.resize((30, 30), Image.LANCZOS))
check_button = tk.Button(search_frame, compound="left", width=-10, background="white", image=photo6, command=check_syntax)
check_button.pack(side=tk.LEFT, padx=10)

image2 = Image.open(r"C:\Users\KayCy\OneDrive\Desktop\VSCode\Python\TD\p8.png")
photo2 = ImageTk.PhotoImage(image2.resize((30, 30), Image.LANCZOS))
run_button = tk.Button(search_frame, text="Run", compound="left", width=-10, background="white", image=photo2, command=run_file)
run_button.pack(side=tk.LEFT, padx=10, pady=10)

# Create the file path label
image4 = Image.open(r"C:\Users\KayCy\OneDrive\Desktop\VSCode\Python\TD\r1.png")
photo4 = ImageTk.PhotoImage(image4.resize((20, 20), Image.LANCZOS))
file_path_label = tk.Label(search_frame, compound="left", width=-10, background="white", image=photo4, anchor="w")
file_path_label.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=10)

def update_line_numbers(*args):
    code_text.update_idletasks()
    line_numbers.config(state='normal')
    line_numbers.delete('1.0', tk.END)
    line_numbers.insert(tk.END, '\n'.join(str(i) for i in range(1, int(code_text.index(tk.END).split('.')[0]) - 1)))
    line_numbers.config(state='disabled')

def update_line_numbers_scroll(*args):
    line_numbers.yview_moveto(code_text.yview()[0])

def load_new_file(event):
    update_line_numbers()
    update_line_numbers_scroll()
      
code_frame = tk.Frame(window, background='lightblue', bd=5)
code_frame.pack(fill=tk.BOTH, expand=True)

line_numbers = tk.Text(code_frame, font=("Arial", 12), width=4, padx=3, pady=2, takefocus=0, border=1,
                       background='lightgrey', foreground='black', state='disabled')
line_numbers.pack(side=tk.LEFT, fill=tk.Y)

code_text = tk.Text(code_frame, wrap=tk.WORD, bd=3, font=("Arial", 12))
code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

code_scrollbar = tk.Scrollbar(code_frame, orient=tk.VERTICAL, command=code_text.yview)
code_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

code_text.config(yscrollcommand=code_scrollbar.set)
code_text.tag_configure("Code", background="white")  # Định dạng cho mã code
code_text.tag_configure("highlight", background="red")  # Định dạng cho việc highlight kết quả tìm kiếm

#----------------------------------------------------------------------------------------------------------------------------
# Tạo frame cho phần DRAM
dram_frame = tk.Frame(window, background='lightblue', bd=5)
dram_frame.pack(fill=tk.BOTH, expand=True)
dram_frame.pack_forget()  # Đóng phần draw_text lại

# Tạo khung DRAM
dram_text = tk.Text(dram_frame, wrap=tk.WORD, bd=3, font=("Arial", 12))
dram_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Tạo thanh cuộn cho khung DRAM
dram_scrollbar = tk.Scrollbar(dram_frame, orient=tk.VERTICAL, command=dram_text.yview)
dram_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Thiết lập cho khung DRAM có thanh cuộn
dram_text.config(yscrollcommand=dram_scrollbar.set)

# Tạo nút x nhỏ để đóng lại phần DRAM
close_button = tk.Button(dram_frame, text="x", width=2, command=dram_frame.pack_forget)
close_button.pack(anchor='ne', padx=5, pady=5)

code_text.bind("<<LoadNewFile>>", load_new_file)
code_text.bind('<<Modified>>', update_line_numbers)
code_text.bind("<MouseWheel>", update_line_numbers_scroll)
update_line_numbers()
update_line_numbers_scroll()
#----------------------------------------------------------------------------------------------------------------------------
def move_in():
    x = framed.winfo_x()
    if x > code_frame.winfo_screenwidth() - frame_width:
        framed.place(x=x -10, y=0)
        framed.after(10, move_in)

def move_out():
    x = framed.winfo_x()
    if x < code_frame.winfo_screenwidth():
        framed.place(x=x +10, y=0)
        framed.after(10, move_out)
    else:
        framed.place_forget()

def on_arrow_click(direction):
    global moving_out
    if moving_out:
        moving_out = False
        move_out()
        #framed.place(x=code_frame.winfo_screenwidth()-frame_width, y=0)
    else:
        moving_out = True
        move_in()

def load_folders():
    global upper_frame
    folders = [
        r"C:\Users\KayCy\OneDrive\Desktop\VSCode\Python\TD",
        r"C:\Users\KayCy\OneDrive\Desktop\VSCode\Python\TTCN",
        r"C:\Users\KayCy\OneDrive\Desktop\VSCode\Python\MY",
        r"C:\Users\KayCy\OneDrive\Desktop\VSCode\Python\CA",
        ]  # Danh sách thư mục cần nạp
    a = ["a", "b", "c", "d"]

    # Tạo khung trên để lưu trữ thư mục
    upper_frame = tk.Frame(framed, bg='white')
    upper_frame.grid(row=0, column=1, sticky="nsew")  # Sử dụng grid()

    upper_frame.rowconfigure(0, weight=60)  # Thêm cấu hình để cho phép khung tự mở rộng chiều cao

    scrollbar_upper_frame = tk.Scrollbar(upper_frame)  # Thêm thanh cuộn cho khung trên
    scrollbar_upper_frame.pack(side=tk.RIGHT, fill=tk.Y)

    folder_listbox = tk.Listbox(upper_frame, yscrollcommand=scrollbar_upper_frame.set)
    folder_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    for folder, i in zip(folders, a):
        folder_name = os.path.basename(folder)
        folder_label = tk.Label(folder_listbox, text=i, width=25, bg='white')
        folder_label.pack()

        def on_folder_click(event, f=folder):
            load_files(f)

        folder_label.bind('<Button-1>', on_folder_click)

    scrollbar_upper_frame.config(command=folder_listbox.yview)

    # Tạo khung dưới để hiển thị các tệp trong thư mục
    lower_frame = tk.Frame(framed, bg='white')
    lower_frame.grid(row=1, column=1, sticky="nsew")  # Sử dụng grid()

    lower_frame1 = tk.Frame(lower_frame, bg='red')
    lower_frame1.pack(fill=tk.BOTH, expand=True)

    scrollbar_lower_frame = tk.Scrollbar(lower_frame1)  # Thêm thanh cuộn
    scrollbar_lower_frame.pack(side=tk.RIGHT, fill=tk.Y)

    file_listbox = tk.Listbox(lower_frame1, width=30, yscrollcommand=scrollbar_lower_frame.set)
    file_listbox.pack(fill=tk.BOTH, expand=True)

    def load_files(folder):
        global lower_frame  # Khai báo lower_frame là biến toàn cục
        lower_frame.destroy()  # Xóa các widget trong khung dưới
        lower_frame = tk.Frame(framed, bg='red')
        lower_frame.grid(row=1, column=1, sticky="nsew")  # Sử dụng grid()

        lower_frame1 = tk.Frame(lower_frame, bg='red')
        lower_frame1.pack(fill=tk.BOTH, expand=True)

        scrollbar_lower_frame = tk.Scrollbar(lower_frame1)  # Thêm thanh cuộn
        scrollbar_lower_frame.pack(side=tk.RIGHT, fill=tk.Y)

        file_listbox = tk.Listbox(lower_frame1, width=30, yscrollcommand=scrollbar_lower_frame.set)
        file_listbox.pack(fill=tk.BOTH, expand=True)

        files = os.listdir(folder)  # Lấy danh sách các tệp trong thư mục được chọn
        for file in files:
            file_listbox.insert(tk.END, file)

        scrollbar_lower_frame.config(command=file_listbox.yview)

        def get_selected_file():
            global file_path
            selected_file_index = file_listbox.curselection()[0]  # Lấy chỉ mục của tệp được chọn
            selected_file = files[selected_file_index]
            file_path = os.path.join(folder, selected_file)  # Tạo đường dẫn của tệp

            with open(file_path, "r", encoding="utf-8") as file:
                dram_text.delete(1.0, tk.END)
                code_text.delete('1.0', tk.END)
                code_text.insert(tk.END, file.read())

            code_text.event_generate("<<LoadNewFile>>")

            # Update the file path label
            file_path_label.config(text=file_path)

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

        select_button = tk.Button(lower_frame, text="Select", command=get_selected_file)
        select_button.pack(side=tk.LEFT, pady=5)  # Đặt select_button sang trái

def app0():
    app = to13.LoginApp()
    app.mainloop()

def app1():
    app = to11_5.LibraryDisplayApp()
    app.run()
    
def app2():
    app = to12.PythonInstallerApp()
    app.run()

def app3():
    app = to15.TranslationApp()
    app.run()

frame_width = 230
frame_height = code_frame.winfo_screenheight() // 2

framed = tk.Frame(code_frame, width=frame_width, height=frame_height, bg='red', bd=3)
framed.place(x=code_frame.winfo_screenwidth(), y=0)

close_button1 = tk.Button(framed, text=">", command=lambda: on_arrow_click('left'))
close_button1.grid(row=0, column=0, padx=2, sticky="nsew")

moving_out = False

# Tạo khung trên để lưu trữ thư mục
upper_frame = tk.Frame(framed, bg='white')
upper_frame.grid(row=0, column=1, sticky="nsew")  # Sử dụng grid()

load_folders()  # Nạp các thư mục vào khung trên

# Tạo khung dưới để hiển thị các tệp trong thư mục
lower_frame = tk.Frame(framed, bg='white')
lower_frame.grid(row=1, column=1, sticky="nsew")  # Sử dụng grid()

framed.grid_rowconfigure(0, weight=1)
framed.grid_rowconfigure(1, weight=1)
#----------------------------------------------------------------------------------------------------------------------------
# Create the menu bar
menu_bar = tk.Menu(window)

# Create the File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_code_text)
file_menu.add_command(label="Chọn file", command=choose_file)
file_menu.add_command(label="Tab ghi chú", command=create_new_tab)
file_menu.add_command(label="Terminal", command=show_dram_text)
file_menu.add_command(label="Lưu file", command=save_file)
file_menu.add_command(label="Lưu file as", command=save_file_as)
file_menu.add_separator()
file_menu.add_command(label="Thoát", command=close_app)

# Create the Edit menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Run Code", command=run_file)
edit_menu.add_separator()
edit_menu.add_command(label="Code mẫu", command=lambda: on_arrow_click('left'))
edit_menu.add_command(label="Cài code", command=app2)

# Create the Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Dịch EN-VI", command=app3)
help_menu.add_command(label="Thư viện đã cài đặt", command=app1)
help_menu.add_command(label="Hướng dẫn sử dụng", command=show_guide)
help_menu.add_command(label="Hỗ trợ", command=show_about)

# Add the File and Help menus to the menu bar
menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
menu_bar.add_cascade(label="Trợ giúp", menu=help_menu)

# Set the menu bar for the window
window.config(menu=menu_bar)
#----------------------------------------------------------------------------------------------------------------------------
# Tạo phần hiển thị lỗi cú pháp và tọa độ con trỏ chuột
error_coord_frame = tk.Frame(window)
error_coord_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(5, 0))

error_label = tk.Label(error_coord_frame, text="", fg="green")
error_label.pack(side=tk.LEFT)

coord_label = tk.Label(error_coord_frame)
coord_label.pack(side=tk.RIGHT, anchor='e')

# Hàm cập nhật tọa độ con trỏ chuột khi di chuyển con trỏ trong khung
def update_mouse_coordinates(event):
    # Lấy tọa độ con trỏ chuột từ sự kiện
    x, y = event.x, event.y
    # Cập nhật nội dung của Label để hiển thị tọa độ mới
    coord_label.config(text=f"X: {x}, Y: {y}")

# Gán hàm cập nhật vào sự kiện "Motion" của khung
window.bind("<Motion>", update_mouse_coordinates)
#----------------------------------------------------------------------------------------------------------------------------
window.mainloop()
