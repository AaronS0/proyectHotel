import tkinter as tk
from tkinter import ttk
from sistema_hotel import SistemaHotel

def main():
    root = tk.Tk()
    app = SistemaHotel(root)
    root.mainloop()

if __name__ == "__main__":
    main()