import tkinter as tk
from src.page_manager import PageManager


if __name__ == "__main__":
    root = tk.Tk()
    app = PageManager(root)
    root.mainloop()
