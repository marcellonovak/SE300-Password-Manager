import tkinter as tk
from tkinter import messagebox as mb
import encryption


class PasswordViewerGUI:
    def __init__(self, master, pin, entry_id=None, refresh_callback=None):
        # Store parameters
        self.pin = pin
        self.entry_id = entry_id
        self.refresh_callback = refresh_callback
        self.is_editing = entry_id is not None
        
        # Set master window conditions
        self.master = master
        if self.is_editing:
            master.title("Edit Password")
        else:
            master.title("Add New Password")
        master.configure(bg="lightblue")
        master.iconbitmap("./icon_shield.ico")  # Set the icon
        master.geometry("300x320")  # Adjusted size after removing custom name field

        # Set up the fields
        self.setup_fields()
        
        # If editing, populate fields with existing data
        if self.is_editing:
            self.populate_fields()

    def setup_fields(self):
        #######################
        ### PASSWORD FIELDS ###
        #######################

        # Username
        tk.Label(self.master, text="Username:", bg="lightblue").grid(
            row=0, column=0, sticky="w", padx=5
        )
        self.username_entry = tk.Entry(self.master)
        self.username_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 2.5))

        # Service Name
        tk.Label(self.master, text="Service Name:", bg="lightblue").grid(
            row=0, column=1, sticky="w", padx=5
        )
        self.service_entry = tk.Entry(self.master)
        self.service_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 2.5))

        # Password
        tk.Label(self.master, text="Password:", bg="lightblue").grid(
            row=2, column=0, sticky="w", padx=5
        )
        self.password_entry = tk.Entry(self.master, show="•")  # Mask the password
        self.password_entry.grid(row=3, column=0, sticky="ew", padx=5, pady=(0, 2.5))

        # Show/Hide Password button
        self.password_visible = False
        self.show_password_button = tk.Button(
            self.master, text="Show Password", bg="white", command=self.toggle_password_visibility
        )
        self.show_password_button.grid(row=3, column=1, sticky="w", padx=5, pady=(0, 2.5))

        # Notes
        tk.Label(self.master, text="Notes:", bg="lightblue").grid(
            row=4, column=0, sticky="w", padx=5
        )
        self.notes_text = tk.Text(self.master, height=5)
        self.notes_text.grid(
            row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=(0, 2.5)
        )

        ########################
        ### BUTTON FUNCTIONS ###
        ########################

        # Frame to hold the buttons
        button_frame = tk.Frame(self.master, bg="lightblue")
        button_frame.grid(row=6, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        # Save Button
        self.save_button = tk.Button(
            button_frame, text="Save", bg="white", command=self.save_clicked
        )
        self.save_button.pack(side=tk.LEFT, padx=(2.5, 2.5))

        # Delete Button (for editing)
        if self.is_editing:
            self.delete_button = tk.Button(
                button_frame, text="Delete", bg="white", command=self.delete_clicked
            )
            self.delete_button.pack(side=tk.LEFT, padx=(2.5, 2.5))
        
        # Cancel Button
        self.cancel_button = tk.Button(
            button_frame, text="Cancel", bg="white", command=self.cancel_clicked
        )
        self.cancel_button.pack(side=tk.LEFT, padx=(2.5, 2.5))

        # Configure grid rows and columns to expand
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(5, weight=1)

    def populate_fields(self):
        """Populate fields with data from existing entry"""
        try:
            # Get data for this entry
            data = encryption.read_data_by_ID(self.pin, self.entry_id)
            
            # Fill in the fields
            self.service_entry.insert(0, data[0])  # Service name
            self.username_entry.insert(0, data[1])  # Username
            self.password_entry.insert(0, data[2])  # Password
            
            # Try to get notes if they exist
            try:
                services, info = encryption.read_services(self.pin)
                if self.entry_id < len(info):
                    self.notes_text.insert("1.0", info[self.entry_id])
            except Exception as e:
                print(f"Error loading notes: {e}")
        except Exception as e:
            mb.showerror("Error", f"Failed to load password data: {e}")

    def toggle_password_visibility(self):
        """Toggle password visibility"""
        # Verify PIN again before showing password
        if not self.password_visible:
            pin_dialog = tk.simpledialog.askstring(
                "PIN Required", 
                "Please enter your PIN to view password:", 
                show='*',
                parent=self.master
            )
            
            if not pin_dialog or pin_dialog != self.pin:
                mb.showerror("Error", "Incorrect PIN")
                return
                
        # Toggle visibility
        if self.password_visible:
            self.password_entry.config(show="•")
            self.show_password_button.config(text="Show Password")
            self.password_visible = False
        else:
            self.password_entry.config(show="")
            self.show_password_button.config(text="Hide Password")
            self.password_visible = True

    def save_clicked(self):
        """Save the current data"""
        if (
            self.username_entry.get() == ""
            or self.service_entry.get() == ""
            or self.password_entry.get() == ""
        ):
            mb.showwarning(
                "Incomplete Entry",
                "The username, service name, and password fields must be filled to proceed. Please try again.",
            )
        else:
            try:
                service = self.service_entry.get()
                username = self.username_entry.get()
                password = self.password_entry.get()
                notes = self.notes_text.get("1.0", "end-1c")  # Get text without the final newline
                
                if self.is_editing:
                    # For editing, we need to remove the old entry and add the new one
                    encryption.remove_service(self.pin, self.entry_id)
                
                # Add the new or updated entry
                encryption.add_service(self.pin, service, username, password, notes)
                
                # Call the refresh callback if provided
                if self.refresh_callback:
                    self.refresh_callback()
                
                self.master.destroy()
            except Exception as e:
                mb.showerror("Error", f"Failed to save password: {e}")

    def delete_clicked(self):
        """Delete the current entry"""
        if self.is_editing:
            # Verify PIN again before deleting
            pin_dialog = tk.simpledialog.askstring(
                "PIN Required", 
                "Please enter your PIN to delete this entry:", 
                show='*',
                parent=self.master
            )
            
            if not pin_dialog or pin_dialog != self.pin:
                mb.showerror("Error", "Incorrect PIN")
                return
                
            confirm = mb.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete this password entry?"
            )
            if confirm:
                try:
                    encryption.remove_service(self.pin, self.entry_id)
                    
                    # Call the refresh callback if provided
                    if self.refresh_callback:
                        self.refresh_callback()
                    
                    self.master.destroy()
                except Exception as e:
                    mb.showerror("Error", f"Failed to delete password: {e}")

    def cancel_clicked(self):
        """Close without saving"""
        self.master.destroy()


# Function to create the GUI
def create_gui(master, pin, entry_id=None, refresh_callback=None):
    # Need to import here to avoid circular imports
    import tkinter.simpledialog
    password_viewer = PasswordViewerGUI(master, pin, entry_id, refresh_callback)
    return password_viewer  # Return the GUI instance


# Only runs if this script is run directly, for testing
if __name__ == "__main__":
    root = tk.Tk()
    create_gui(root, "1111")
    root.mainloop()