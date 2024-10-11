import tkinter as tk
from tkinter import font
from datetime import datetime


def main():
    app = MainWindow()
    controller = Controller(app)

    controller.run()


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        style = Style()

        # Window settings
        self.title("My Writing App")
        self.geometry(f"{style.windowWidth}x{style.windowHeight}+608+62")
        self.overrideredirect(True)
        self.saved_geometry = self.geometry()
        self.is_fullscreen = False
        self.config(bg=style.background)

        # Layout
        self.headFrame = HeadFrame()
        self.textFrame = TextFrame()

        # Header
        self.headFrame.config(bg=style.background)
        self.headFrame.pack(fill="x", pady=10, padx=20, anchor="n")

        # Textframe
        self.textFrame.config(width=style.textWidth, bg=style.background)
        self.textFrame.pack(fill="y", padx=100, expand=True, anchor="n")


class HeadFrame(tk.Frame):
    def __init__(self):
        super().__init__()

        style = Style()

        title = tk.Label(
            self, text="just write", fg=style.fontColor2, bg=style.background
        )
        title.pack(pady=20)
        title.configure(font=(style.font, 12, "italic"))


class TextFrame(tk.Frame):
    def __init__(self):
        super().__init__()

        style = Style()

        with open("placeholdertext.txt", "r", encoding="utf-8") as file:
            placeholdertext = file.read()

        self.textarea = tk.Text(self)
        self.textarea.pack(fill="both", expand=True, pady=30)
        self.textarea.config(
            bg=style.background,
            fg=style.fontColor1,
            borderwidth=0,
            insertbackground=style.fontColor1,
            wrap="word",
            tabs=(30),
            spacing1=(8),
            spacing2=(5),
            spacing3=(5),
            undo=True,
            font=(style.font, style.fontSize),
        )

        self.textarea.insert("1.0", placeholdertext)
        self.textarea.tag_configure("bold", font=(style.font, style.fontSize, "bold"))
        self.textarea.tag_configure(
            "italic", font=(style.font, style.fontSize, "italic")
        )
        self.textarea.tag_configure("underline", underline=True)
        self.textarea.tag_configure("h1", font=(style.font, style.h1))
        self.textarea.tag_configure("h2", font=(style.font, style.h2))
        self.textarea.tag_configure("h3", font=(style.font, style.h3))
        self.textarea.tag_configure("center", justify="center")
        self.textarea.tag_configure("left", justify="left")
        self.textarea.tag_configure("right", justify="right")
        self.textarea.tag_configure("color1", foreground=style.fontColor1)
        self.textarea.tag_configure("color2", foreground=style.fontColor2)
        self.textarea.tag_configure("color3", foreground=style.fontColor3)


class Controller:
    def __init__(self, MainWindow):
        self.mainwindow = MainWindow
        self.headframe = self.mainwindow.headFrame
        self.textframe = self.mainwindow.textFrame

        #  WARN: Exit on <Escape> is developer mode only.
        #        Must remove before deployment.
        self.mainwindow.bind("<Escape>", lambda _e: self.mainwindow.destroy())

        self.headframe.bind("<ButtonPress-1>", self.start_drag)
        self.headframe.bind("<B1-Motion>", self.drag_window)
        self.headframe.bind("<Double-Button-1>", self.toggleFullscreen)

        #  TODO: Find out how to reset/unbind default binding.
        #        Ctrl+[1, 2, 3...] doesn't work.

        #  TODO: Idea: Change fontsize of selected text with scrollwheel?
        self.textframe.textarea.bind("<Control-b>", self.make_bold)
        self.textframe.textarea.bind("<Control-e>", self.make_italic)
        self.textframe.textarea.bind("<Control-u>", self.make_underline)
        self.textframe.textarea.bind("<F1>", self.make_h1)
        self.textframe.textarea.bind("<F2>", self.make_h2)
        self.textframe.textarea.bind("<F3>", self.make_h3)
        self.textframe.textarea.bind("<F4>", self.make_center)
        self.textframe.textarea.bind("<F5>", self.make_left)
        self.textframe.textarea.bind("<F6>", self.make_right)
        self.textframe.textarea.bind("<Button-2>", self.make_color1)
        self.textframe.textarea.bind("<Button-4>", self.make_color2)
        self.textframe.textarea.bind("<Button-5>", self.make_color3)

    def make_bold(self, _event=None):
        self.toggle_tag("bold")

    def make_italic(self, _event=None):
        self.toggle_tag("italic")

    def make_underline(self, _event=None):
        self.toggle_tag("underline")

    def make_h1(self, _event=None):
        self.toggle_tag("h1")

    def make_h2(self, _event=None):
        self.toggle_tag("h2")

    def make_h3(self, _event=None):
        self.toggle_tag("h3")

    def make_center(self, _event=None):
        self.toggle_tag("center")

    def make_left(self, _event=None):
        self.toggle_tag("left")

    def make_right(self, _event=None):
        self.toggle_tag("right")

    def make_color1(self, _event=None):
        self.toggle_tag("color1")

    def make_color2(self, _event=None):
        self.toggle_tag("color2")

    def make_color3(self, _event=None):
        self.toggle_tag("color3")

    def toggle_tag(self, tag_name):
        try:
            start = self.textframe.textarea.index(tk.SEL_FIRST)
            end = self.textframe.textarea.index(tk.SEL_LAST)
        except tk.TclError as e:
            print(e)
            return

        current_tags = self.textframe.textarea.tag_names(tk.SEL_FIRST)

        if tag_name in current_tags:
            self.textframe.textarea.tag_remove(tag_name, start, end)
        else:
            self.textframe.textarea.tag_add(tag_name, start, end)

        # Oppdater SEL-taggen for å reflektere den nåværende markeringen
        self.textframe.textarea.tag_remove(
            tk.SEL, "1.0", tk.END
        )  # Fjern tidligere SEL-markering
        # Legg til SEL for den nye markeringen
        self.textframe.textarea.tag_add(tk.SEL, start, end)

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


class Style:
    def __init__(self):
        self.windowWidth = "800"
        self.windowHeight = "950"
        self.textWidth = 600
        self.background = "#121319"
        self.fontColor1 = "#d5d5d5"
        self.fontColor2 = "#d5ae88"
        self.fontColor3 = "#0eb6d4"
        self.font = "AGaramond"
        self.fontSize = 14
        self.h1 = 36
        self.h2 = 24
        self.h3 = 18

        #  TODO: Set 3 font sizes: size1, size2, and size3.
        #        The user can multiply these sizes relatively.


class Document:
    def __init__(self):
        self.filename: str
        self.dateCreated: datetime
        self.dateModified: datetime


if __name__ == "__main__":
    main()
