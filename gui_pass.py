import tkinter as tk

class PasswordViewerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Password Viewer")
        master.configure(bg="lightblue")


        #######################
        ### PASSWORD FIELDS ###
        #######################

        # Username
        tk.Label(master, text="Username:", bg="lightblue").grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))  # Adjusted pady
        self.username_entry = tk.Entry(master)
        self.username_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 2.5))  # Adjusted row and pady

        # Site
        tk.Label(master, text="Site:", bg="lightblue").grid(row=0, column=1, sticky="w", padx=5, pady=(5, 0))  # Adjusted pady
        self.site_entry = tk.Entry(master)
        self.site_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 2.5))  # Adjusted row and pady

        # Password
        tk.Label(master, text="Password:", bg="lightblue").grid(row=2, column=0, sticky="w", padx=5, pady=(5, 0))  # Adjusted row and pady
        self.password_entry = tk.Entry(master, show="•")  # Mask the password
        self.password_entry.grid(row=3, column=0, sticky="ew", padx=5, pady=(0, 2.5))  # Adjusted row and pady

        # Custom Name
        tk.Label(master, text="Custom Name:", bg="lightblue").grid(row=2, column=1, sticky="w", padx=5, pady=(5, 0))  # Adjusted row and pady
        self.custom_name_entry = tk.Entry(master)
        self.custom_name_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=(0, 2.5))  # Adjusted row and pady

        # Notes
        tk.Label(master, text="Notes:", bg="lightblue").grid(row=4, column=0, sticky="w", padx=5, pady=(5, 0))  # Adjusted row and pady
        self.notes_text = tk.Text(master, height=5)
        self.notes_text.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=(0, 2.5))  # Adjusted row and pady


        ###############
        ### BUTTONS ###
        ###############

        # Frame to hold the buttons
        button_frame = tk.Frame(master, bg="lightblue")
        button_frame.grid(row=6, column=0, columnspan=2, sticky="w", padx=5, pady=(5, 5))  # Adjusted row

        # Save Button
        self.save_button = tk.Button(button_frame, text="Save", bg="white")
        self.save_button.pack(side=tk.LEFT, padx=(0, 5))

        # Delete Button
        self.delete_button = tk.Button(button_frame, text="Delete", bg="white")
        self.delete_button.pack(side=tk.LEFT)


        # Configure grid rows and columns to expand
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_rowconfigure(5, weight=1)  # Adjusted row


# Function to create and run the GUI
def run_gui():
    root = tk.Tk()
    password_viewer = PasswordViewerGUI(root)
    root.geometry("300x300") # Set the initial window size
    root.mainloop()


# Runs only if this script is executed directly for testing
if __name__ == "__main__":
    run_gui()