import tkinter as tk
import gui_main
import gui_pass
import gui_settings

if __name__ == "__main__":
    root = tk.Tk()
    gui_main.create_gui(root)  # Create the main GUI
    
    password_viewer_window = tk.Toplevel(root)
    gui_pass.create_gui(password_viewer_window)

    settings_window = tk.Toplevel(root)
    gui_settings.create_gui(settings_window)

    root.mainloop()  # Run the main event loop