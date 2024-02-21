import tkinter as tk
from PIL import ImageTk, Image
from MenuBar import MyMenuBar
from CoEd import CodeEditor
from ECF import MouseCoordinates

class ViewsCodeApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ViewsCode")
        self.window.geometry("600x400")
        image1 = Image.open(r"C:\Users\KayCy\OneDrive\Desktop\VSCode\Python\TD\logovkc.png")
        photo1 = ImageTk.PhotoImage(image1.resize((100, 100), Image.LANCZOS))
        self.window.iconphoto(True, photo1)

        self.menu = MyMenuBar(self.window)
        self.window.config(menu=self.menu.menu_bar)

    
        self.coed = CodeEditor(self.window)

        self.mouse_coordinates = MouseCoordinates(self.window)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ViewsCodeApp()
    app.run()
