import tkinter as tk
import gui_main
import gui_pass

if __name__ == "__main__":
    root = tk.Tk()
    gui_main.create_gui(root)  # Create the main GUI
    
    # Create a new Toplevel window for the password viewer
    password_viewer_window = tk.Toplevel(root)  
    gui_pass.create_gui(password_viewer_window)  # Create the password viewer GUI

    root.mainloop()  # Run the main event loop