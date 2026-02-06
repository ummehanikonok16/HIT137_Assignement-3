

import tkinter as tk
from img_editor import ImageEditor


def main():
    root = tk.Tk()
    app = ImageEditor(root)
    app.run()


if __name__ == "__main__":
    main()