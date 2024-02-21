import tkinter as tk
from tkinter import filedialog, messagebox
from ChFile import FileChooser
from to15 import TranslationApp
from to11_5 import LibraryDisplayApp
from to12 import PythonInstallerApp
 
class MyMenuBar:
    def __init__(self,window): 
        self.window = window
        self.menu_bar = tk.Menu(self.window)
        
        self.create_file_menu()
        self.create_edit_menu()
        self.create_help_menu()



    def create_file_menu(self):
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_code_text)
        file_menu.add_command(label="Chọn file", command=self.choose_file)
        file_menu.add_command(label="Tab ghi chú", command=self.create_new_tab)
        file_menu.add_command(label="Terminal", command=self.show_dram_text)
        file_menu.add_command(label="Lưu file", command=self.save_file)
        file_menu.add_command(label="Lưu file as", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self.close_app)
        
        # Add the File menu to the menu bar
        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def create_edit_menu(self):
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Run Code", command=self.run_file)
        edit_menu.add_separator()
        edit_menu.add_command(label="Code mẫu", command=lambda: self.on_arrow_click('left'))
        edit_menu.add_command(label="Cài code", command=self.app2)
        
        # Add the Edit menu to the menu bar
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
    
    def create_help_menu(self):
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Dịch EN-VI", command=self.app3)
        help_menu.add_command(label="Thư viện đã cài đặt", command=self.app1)
        help_menu.add_command(label="Hướng dẫn sử dụng", command=self.show_guide)
        help_menu.add_command(label="Hỗ trợ", command=self.show_about)
        
        # Add the Help menu to the menu bar
        self.menu_bar.add_cascade(label="Trợ giúp", menu=help_menu)
    
    def new_code_text(self):
        pass
    
    def choose_file(self):
        pass
    
    def create_new_tab(self):
        new_tab = tk.Toplevel(self.window)
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

    
    def show_dram_text(self):
        pass
    
    def save_file(self):
        pass
    
    def save_file_as(self):
        filename = filedialog.asksaveasfilename(initialdir="/", title="Lưu file",
                                                filetypes=(("Python files", "*.py"), ("All files", "*.*")))
        if filename:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(self.code_text.get('1.0', tk.END))
            messagebox.showinfo("Thông báo", "Tệp đã được lưu: {}".format(filename))  # Thông báo đường dẫn đã được lưu
    
    def close_app(self):
        self.window.destroy()
    
    def run_file(self):
        pass
    
    def on_arrow_click(self, direction):
        pass
    
    def app2(self):
        app = PythonInstallerApp()
        app.run()
    
    def app3(self):        
        app = TranslationApp()
        app.run()
        
    def app1(self):
        app = LibraryDisplayApp()
        app.run()
    
    def show_guide(self):
        guide_text = '''
        Hướng dẫn sử dụng:
        - Bước 1: Nhập mã vào ô văn bản.
        - Bước 2: Chọn tệp tin cần chạy hoặc lưu tệp tin.
        - Bước 3: Nhấn Run để chạy mã hoặc Save để lưu tệp tin.
        
        Lưu ý: DRAM sẽ hiển thị kết quả của quá trình chạy mã.
        '''
        messagebox.showinfo("Hướng dẫn sử dụng", guide_text)
    def show_about(self):
        messagebox.showinfo("About", "Thông tin ứng dụng ViewsCode 1.0")
        


# Create an instance of the MyApp class
#app = MyApp()
