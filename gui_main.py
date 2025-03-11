import tkinter as tk

class PasswordManagerGUI:
    def __init__(self, master):

        # Set master window conditions
        self.master = master
        master.title("Password Manager")
        master.configure(bg="lightblue")
        master.iconbitmap("./icon_shield.ico") # Set the icon
        master.geometry("300x300")  # Set the initial size
        

        ###############
        ### BUTTONS ###
        ###############

        # Frame to hold the buttons
        button_frame = tk.Frame(master, bg="lightblue")
        button_frame.pack(fill=tk.X, padx=5, pady=(5, 2.5))  # Add top padding

        # Add New button
        self.add_new_button = tk.Button(button_frame, text="Add New", bg="white")
        self.add_new_button.pack(side=tk.LEFT, padx=(0, 5))

        # Settings button
        self.settings_button = tk.Button(button_frame, text="Settings", bg="white")
        self.settings_button.pack(side=tk.LEFT)


        # Empty box for password list
        self.password_list_label = tk.Label(master, text="", relief=tk.SUNKEN, width=50, height=20, bg="white")
        self.password_list_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=0)


# Function to create the GUI
def create_gui(master):  # Changed function name
    password_manager = PasswordManagerGUI(master)
    return password_manager  # Return the GUI instance