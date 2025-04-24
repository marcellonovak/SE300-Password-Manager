import tkinter as tk
from tkinter import ttk, simpledialog
import gui_pass, gui_settings
import encryption

# Default PIN - will be checked against the file
PIN = "1111"



class PasswordManagerGUI:
    def __init__(self, master):
        # Try to open the password file, or create a new one if it doesn't exist
        try:
            with open("passwords", "r") as f:
                pass
        except FileNotFoundError:
            print("Password file not found. Creating a new file.")
            encryption.gen_file(PIN)

        # Set master window conditions
        self.master = master
        master.title("Password Manager")
        master.configure(bg="lightblue")
        master.iconbitmap("./icon_shield.ico")  # Set the icon
        master.geometry("500x400")  # Increased size for better visibility

        ########################
        ### BUTTON FUNCTIONS ###
        ########################

        def AddNewClicked():
            # Verify PIN before allowing new password creation
            entered_pin = self.verify_pin()
            if entered_pin:
                # Create and open password viewer window for a new entry
                password_viewer_window = tk.Toplevel(self.master)
                gui_pass.create_gui(password_viewer_window, entered_pin, None, self.refresh_password_list)

        def SettingsClicked():
            # Verify PIN before opening settings
            entered_pin = self.verify_pin()
            if entered_pin:
                # Create and open settings window
                settings_window = tk.Toplevel(self.master)
                gui_settings.create_gui(settings_window, entered_pin, self.refresh_password_list)

        def on_item_select(event):
            # Get the selected item
            selected_item = self.password_list.selection()
            if selected_item:  # If something is selected
                item_id = int(self.password_list.item(selected_item[0], "values")[0])
                
                # Verify PIN before allowing to view/edit
                entered_pin = self.verify_pin()
                if entered_pin:
                    # Open the password viewer with the selected entry
                    password_viewer_window = tk.Toplevel(self.master)
                    gui_pass.create_gui(password_viewer_window, entered_pin, item_id, self.refresh_password_list)

        ###############
        ### BUTTONS ###
        ###############

        # Frame to hold the buttons
        button_frame = tk.Frame(master, bg="lightblue")
        button_frame.pack(fill=tk.X, padx=5, pady=(5, 2.5))  # Add top padding

        # Add New button
        self.add_new_button = tk.Button(
            button_frame, text="Add New", bg="white", command=AddNewClicked
        )
        self.add_new_button.pack(side=tk.LEFT, padx=(2.5, 2.5))

        # Settings button
        self.settings_button = tk.Button(
            button_frame, text="Settings", bg="white", command=SettingsClicked
        )
        self.settings_button.pack(side=tk.LEFT, padx=(2.5, 2.5))

        # Refresh button
        self.refresh_button = tk.Button(
            button_frame, text="Refresh", bg="white", command=self.refresh_password_list
        )
        self.refresh_button.pack(side=tk.LEFT, padx=(2.5, 2.5))

        ##################
        ### PASSWORD LIST ###
        ##################

        # Create a Treeview widget for the password list
        self.password_list = ttk.Treeview(master, columns=("ID", "Service", "Notes"), show='headings')
        self.password_list.heading("ID", text="ID")
        self.password_list.heading("Service", text="Service Name")
        self.password_list.heading("Notes", text="Notes")
        
        # Configure column widths
        self.password_list.column("ID", width=30, anchor="center")
        self.password_list.column("Service", width=200)
        self.password_list.column("Notes", width=200)
        
        # Bind selection event
        self.password_list.bind("<<TreeviewSelect>>", on_item_select)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.password_list.yview)
        self.password_list.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.password_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5, side=tk.LEFT)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT, padx=(0, 5), pady=5)
        
        # Initial population of the password list
        self.refresh_password_list()

    def verify_pin(self):
        """Ask user for PIN and verify it"""
        entered_pin = simpledialog.askstring("PIN Required", 
                                          "Please enter your PIN:", 
                                          show='*')
        if entered_pin:
            # Verify the PIN against the stored hash
            try:
                with open("passwords", "r") as file:
                    stored_hash = file.readline().strip()
                    import base64, hashlib
                    entered_hash = base64.b64encode(
                        hashlib.sha512(entered_pin.encode("utf-8")).digest()
                    ).decode("utf-8")
                    
                    if entered_hash == stored_hash:
                        return entered_pin
                    else:
                        tk.messagebox.showerror("Error", "Incorrect PIN")
                        return None
            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not verify PIN: {e}")
                return None
        return None

    def refresh_password_list(self):
        """Refreshes the password list from the data file"""
        # Clear the current list
        for item in self.password_list.get_children():
            self.password_list.delete(item)
        
        try:
            # Get the services and info from the password file
            services, info = encryption.read_services(PIN)
            
            # Insert each service into the treeview
            for i, service in enumerate(services):
                # Get the username for this service entry
                self.password_list.insert("", "end", values=(i, service, info[i]))
        except Exception as e:
            print(f"Error refreshing password list: {e}")


# Function to create the GUI
def create_gui(master):
    password_manager = PasswordManagerGUI(master)
    return password_manager  # Return the GUI instance


# Only runs if this script is run directly, for testing
if __name__ == "__main__":
    root = tk.Tk()
    create_gui(root)
    root.mainloop()