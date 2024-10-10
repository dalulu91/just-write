import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from datetime import datetime


def main():
    app = MainWindow()
    head = HeadFrame(app)
    text = TextFrame(app)
    controller = Controller(app, head, text)

    controller.run()


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Document settings
        self.filename: str
        self.dateCreated: datetime
        self.dateModified: datetime

        # Window settings
        self.title("My Writing App")
        self.geometry("700x800+1200+100")

        self.headFrame = HeadFrame(self)
        self.textFrame = TextFrame(self)

        self.headFrame.pack()
        self.textFrame.pack()


class Controller:
    def __init__(self, MainWindow, HeadFrame, TextFrame):
        self.mainWindow = MainWindow
        self.headFrame = HeadFrame
        self.textFrame = TextFrame

        self.mainWindow.bind("<Escape>", lambda _e: self.mainWindow.destroy())

    def run(self):
        self.mainWindow.mainloop()


class HeadFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.documentMenu()
        self.Title()
        self.textMenu()

    def documentMenu(self):
        pass

    def Title(self):
        ctk.CTkLabel(self, text="Header").pack()

    def textMenu(self):
        pass


class TextFrame(ctk.CTkFrame):
    def __init_(self, parent):
        super().__init__(parent)

        self.textArea = ctk.CTkTextbox(self)
        self.textAreaConfig()

    def textAreaConfig(self):
        self.textArea.pack()


if __name__ == "__main__":
    main()
