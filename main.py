import tkinter as tk
import gui_main

if __name__ == "__main__":
    root = tk.Tk()
    gui_main.create_gui(root)  # Create only the main GUI initially
    root.mainloop()  # Run the main event loop