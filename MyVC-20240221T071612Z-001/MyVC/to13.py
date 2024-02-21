import tkinter as tk

class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Đăng nhập")
        self.geometry("300x150")

        # Tạo các widget
        self.label_username = tk.Label(self, text="Tên đăng nhập:")
        self.label_password = tk.Label(self, text="Mật khẩu:")
        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.button_login = tk.Button(self, text="Đăng nhập", command=self.login)

        # Sắp xếp các widget trên giao diện
        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.button_login.pack()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Kiểm tra tài khoản và mật khẩu
        if username == "admin" and password == "password":
            print("Đăng nhập thành công!")
            # Thực hiện các hành động sau khi đăng nhập thành công
        else:
            print("Đăng nhập thất bại!")

# Tạo một instance của lớp LoginApp và chạy ứng dụng
#app = LoginApp()
#app.mainloop()
