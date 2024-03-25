import tkinter as tk

from settings import Settings
from launcher import Launcher


if __name__ == "__main__":
    settings = Settings()
    root = tk.Tk()
    root.title("Контур.Змейка")
    root.iconbitmap("./snake.ico")

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    launcher = Launcher(root, settings)
    launcher.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_coordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_coordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_coordinate, y_coordinate-20))

    root.mainloop()
