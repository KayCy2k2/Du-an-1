import tkinter as tk

class CodeEditor:
    def __init__(self, window):
        self.window = window
        self.line_numbers = None
        self.code_text = None 
        
        self.create_code_editor()
        self.update_line_numbers()
        self.update_line_numbers_scroll()
        
    def update_line_numbers(self, *args):
        self.code_text.update_idletasks()
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', tk.END)
        self.line_numbers.insert(tk.END, '\n'.join(str(i) for i in range(1, int(self.code_text.index(tk.END).split('.')[0]) - 1)))
        self.line_numbers.config(state='disabled')

    def update_line_numbers_scroll(self, *args):
        self.line_numbers.yview_moveto(self.code_text.yview()[0])

    def load_new_file(self, event):
        self.update_line_numbers()
        self.update_line_numbers_scroll()

    def create_code_editor(self):
        code_frame = tk.Frame(self.window, background='lightblue', bd=5)
        code_frame.pack(fill=tk.BOTH, expand=True)

        self.line_numbers = tk.Text(code_frame, font=("Arial", 12), width=4, padx=3, pady=2, takefocus=0, border=1,
                               background='lightgrey', foreground='black', state='disabled')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.code_text = tk.Text(code_frame, wrap=tk.WORD, bd=3, font=("Arial", 12))
        self.code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        code_scrollbar = tk.Scrollbar(code_frame, orient=tk.VERTICAL, command=self.code_text.yview)
        code_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.code_text.config(yscrollcommand=code_scrollbar.set)
        self.code_text.tag_configure("Code", background="white")  # Định dạng cho mã code

        self.code_text.bind("<<LoadNewFile>>", self.load_new_file)
        self.code_text.bind('<<Modified>>', self.update_line_numbers)
        self.code_text.bind("<MouseWheel>", self.update_line_numbers_scroll)
