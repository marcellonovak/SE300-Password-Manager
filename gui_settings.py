import tkinter as tk

class SettingsGUI:
    def __init__(self, master):

        # Set master window conditions
        self.master = master
        master.title("Manager Settings")
        master.configure(bg="lightblue")
        master.iconbitmap("./icon_shield.ico") # Set the icon 
        master.geometry("250x100")  # Set the initial size


        ###############
        ### BUTTONS ###
        ###############

        # Frame to hold the buttons
        button_frame = tk.Frame(master, bg="lightblue")
        button_frame.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        # Change PIN Button
        change_pin_button = tk.Button(button_frame, text="Change PIN", bg="white")
        change_pin_button.pack(side=tk.LEFT, padx=(2.5, 2.5))

        # Delete All Button
        delete_all_button = tk.Button(button_frame, text="Delete All", bg="white")
        delete_all_button.pack(side=tk.LEFT, padx=(2.5, 2.5))


        ####################
        ### STORAGE PATH ###
        ####################

        # Password Storage Path Label
        path_label = tk.Label(master, text="Password Storage Path:", bg="lightblue")
        path_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=5)

        # Password Storage Path Entry
        path_entry = tk.Entry(master, bg="white")
        path_entry.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 2.5))  # Reduced pady


        # Configure grid columns to expand
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

def create_gui(master):
    settings_gui = SettingsGUI(master)
    return settings_gui

if __name__ == "__main__":
    root = tk.Tk()
    create_gui(root)
    root.mainloop()