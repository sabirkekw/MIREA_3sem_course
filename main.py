import tkinter as tk
from gui.gui import SystemInfoApp

def main():
    try:
        root = tk.Tk()
        app = SystemInfoApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Ошибка запуска приложения: {e}")
        import traceback
        traceback.print_exc()
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()