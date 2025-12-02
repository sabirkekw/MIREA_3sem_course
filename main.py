import tkinter as tk
from gui.gui import SystemInfoApp

def main():
    """Запуск приложения"""
    root = tk.Tk()
    app = SystemInfoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()