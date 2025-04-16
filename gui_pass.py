import tkinter as tk


class PasswordViewerGUI:
    def __init__(self, master):

        # Set master window conditions
        self.master = master
        master.title("Password Viewer")
        master.configure(bg="lightblue")
        master.iconbitmap("./icon_shield.ico")  # Set the icon
        master.geometry("300x300")  # Set the initial size

        #######################
        ### PASSWORD FIELDS ###
        #######################

        # Username
        tk.Label(master, text="Username:", bg="lightblue").grid(
            row=0, column=0, sticky="w", padx=5
        )
        self.username_entry = tk.Entry(master)
        self.username_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 2.5))

        # Site
        tk.Label(master, text="Site:", bg="lightblue").grid(
            row=0, column=1, sticky="w", padx=5
        )
        self.site_entry = tk.Entry(master)
        self.site_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 2.5))

        # Password
        tk.Label(master, text="Password:", bg="lightblue").grid(
            row=2, column=0, sticky="w", padx=5
        )
        self.password_entry = tk.Entry(master, show="•")  # Mask the password
        self.password_entry.grid(row=3, column=0, sticky="ew", padx=5, pady=(0, 2.5))

        # Custom Name
        tk.Label(master, text="Custom Name:", bg="lightblue").grid(
            row=2, column=1, sticky="w", padx=5
        )
        self.custom_name_entry = tk.Entry(master)
        self.custom_name_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=(0, 2.5))

        # Notes
        tk.Label(master, text="Notes:", bg="lightblue").grid(
            row=4, column=0, sticky="w", padx=5
        )
        self.notes_text = tk.Text(master, height=5)
        self.notes_text.grid(
            row=5, column=0, columnspan=4, sticky="nsew", padx=5, pady=(0, 2.5)
        )

        ########################
        ### BUTTON FUNCTIONS ###
        ########################

        def SaveClicked():
            # TODO JN
            print("Save!")

        def DeleteClicked():
            # TODO JN
            print("Deleted!")

        ###############
        ### BUTTONS ###
        ###############

        # Frame to hold the buttons
        button_frame = tk.Frame(master, bg="lightblue")
        button_frame.grid(row=6, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        # Save Button
        self.save_button = tk.Button(
            button_frame, text="Save", bg="white", command=SaveClicked
        )
        self.save_button.pack(side=tk.LEFT, padx=(2.5, 2.5))

        # Delete Button
        self.delete_button = tk.Button(
            button_frame, text="Delete", bg="white", command=DeleteClicked
        )
        self.delete_button.pack(side=tk.LEFT, padx=(2.5, 2.5))

        # Configure grid rows and columns to expand
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_rowconfigure(5, weight=1)


# Function to create the GUI
def create_gui(master):  # Changed function name
    password_manager = PasswordViewerGUI(master)
    return password_manager  # Return the GUI instance


# Only runs if this script is run directly, for testing
if __name__ == "__main__":
    root = tk.Tk()
    create_gui(root)
    root.mainloop()
