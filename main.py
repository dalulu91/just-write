import tkinter as tk
from tkinter import font
from datetime import datetime


def main():
    app = MainWindow()
    head = HeadFrame(app)
    text = TextFrame(app)
    controller = Controller(app, head, text)

    controller.run()


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Document settings
        self.filename: str
        self.dateCreated: datetime
        self.dateModified: datetime

        # Colors
        self.DARK = "#121319"
        self.LIGHT = "#d5ae88"
        self.FONT = "AGaramond"

        # Window settings
        self.title("My Writing App")
        self.geometry("700x800+1100+100")
        self.overrideredirect(True)
        self.saved_geometry = self.geometry()
        self.is_fullscreen = False
        self.config(bg=self.DARK)

        # Layout
        self.headFrame = HeadFrame(self)
        self.textFrame = TextFrame(self)

        # Header
        self.headFrame.config(bg=self.DARK)
        self.headFrame.pack(fill="x", pady=10, padx=20, anchor="n")

        # Textframe
        self.textFrame.config(width=600, bg=self.DARK)
        self.textFrame.pack(fill="y", padx=100, expand=True, anchor="n")


class Controller:
    def __init__(self, MainWindow, HeadFrame, TextFrame):
        self.mainwindow = MainWindow
        self.headframe = HeadFrame
        self.textframe = TextFrame

        #  WARN: Exit on <Escape> is developer mode only.
        #        Must remove before deployment.
        self.mainwindow.bind("<Escape>", lambda _e: self.mainwindow.destroy())

        self.mainwindow.bind("<ButtonPress-3>", self.start_drag)
        self.mainwindow.bind("<B3-Motion>", self.drag_window)
        self.mainwindow.bind("<Double-Button-1>", self.toggleFullscreen)

    def apply_tag(self, tag_name):
        try:
            # Sjekker om det er markert tekst
            if not self.textframe.textarea.tag_ranges(tk.SEL):
                print("Ingen tekst markert for tagging.")
                return  # Hvis ingen tekst er markert, stopper vi her.

            start, end = self.textframe.textarea.tag_ranges(tk.SEL)
            print(f"Tagging fra {start} til {
                  end} med {tag_name}")  # Debug output
            self.textframe.textarea.tag_add(tag_name, start, end)
        except Exception as e:
            print(e)

    def make_bold(self, _event=None):
        self.apply_tag("bold")

    def make_italic(self, _event=None):
        self.apply_tag("italic")

    def make_underline(self, _event=None):
        self.apply_tag("underline")

    def make_title(self, _event=None):
        self.apply_tag("title")

    def make_subtitle(self, _event=None):
        self.apply_tag("subtitle")

    def toggleFullscreen(self, _event=None):
        if self.mainwindow.is_fullscreen:
            self.mainwindow.geometry(self.mainwindow.saved_geometry)
        else:
            self.mainwindow.saved_geometry = self.mainwindow.geometry()
            self.mainwindow.geometry(
                f"{self.mainwindow.winfo_screenwidth()}x{
                    self.mainwindow.winfo_screenheight()}+0+0"
            )

        self.mainwindow.is_fullscreen = not self.mainwindow.is_fullscreen

    def run(self):
        self.mainwindow.mainloop()

    def drag_window(self, event):
        if not self.mainwindow.is_fullscreen:
            deltax = event.x - self.mainwindow.x
            deltay = event.y - self.mainwindow.y
            x = self.mainwindow.winfo_x() + deltax
            y = self.mainwindow.winfo_y() + deltay
            self.mainwindow.geometry(f"+{x}+{y}")

    def start_drag(self, event):
        if not self.mainwindow.is_fullscreen:
            self.mainwindow.x = event.x
            self.mainwindow.y = event.y


class HeadFrame(tk.Frame):
    def __init__(self, mainwindow):
        super().__init__(mainwindow)

        self.mainwindow = mainwindow
        self.FONT_SIZE = 12
        self.Title()

    def Title(self):
        title = tk.Label(
            self, text="just write", fg=self.mainwindow.LIGHT, bg=self.mainwindow.DARK
        )
        title.pack(pady=20)
        title.configure(font=(self.mainwindow.FONT, self.FONT_SIZE, "italic"))


class TextFrame(tk.Frame):
    def __init__(self, mainwindow):
        super().__init__(mainwindow)

        self.mainwindow = mainwindow

        self.FONT_COLOR = "#d5d5d5"
        self.FONT_SIZE_NORMAL = 12
        self.FONT_SIZE_TITLE = 24
        self.FONT_SIZE_SUBTITLE = 18

        self.textarea = tk.Text(self)
        self.textarea.pack(fill="both", expand=True, pady=30)
        self.textarea.config(
            bg=self.mainwindow.DARK,
            fg=self.FONT_COLOR,
            borderwidth=0,
            insertbackground=self.FONT_COLOR,
            wrap="word",
            tabs=(30),
            undo=True,
            font=(self.mainwindow.FONT, self.FONT_SIZE_NORMAL),
        )

        self.textarea.tag_configure(
            "bold", font=(self.mainwindow.FONT, self.FONT_SIZE_NORMAL, "bold")
        )
        self.textarea.tag_configure(
            "italic", font=(self.mainwindow.FONT, self.FONT_SIZE_NORMAL, "italic")
        )
        self.textarea.tag_configure(
            "underline",
            font=(self.mainwindow.FONT, self.FONT_SIZE_NORMAL),
            underline=True,
        )
        self.textarea.tag_configure(
            "title", font=(self.mainwindow.FONT, self.FONT_SIZE_TITLE, "bold")
        )
        self.textarea.tag_configure(
            "subtitle", font=(self.mainwindow.FONT, self.FONT_SIZE_SUBTITLE, "italic")
        )


if __name__ == "__main__":
    main()
