import tkinter as tk
from tkinter import messagebox as mb
import encryption
import os


class SettingsGUI:
    def __init__(self, master, pin, refresh_callback=None):
        # Store parameters
        self.pin = pin
        self.refresh_callback = refresh_callback

        # Set master window conditions
        self.master = master
        master.title("Manager Settings")
        master.configure(bg="lightblue")
        master.iconbitmap("./icon_shield.ico")  # Set the icon
        master.geometry("300x100")  # Adjusted size

        ########################
        ### BUTTON FUNCTIONS ###
        ########################

        def ChangePINClicked():
            # Get current PIN for verification
            current_pin = tk.simpledialog.askstring(
                "Verify Current PIN", 
                "Please enter your current PIN:", 
                show='*',
                parent=self.master
            )
            
            if not current_pin or current_pin != self.pin:
                mb.showerror("Error", "Incorrect PIN")
                return
                
            # Get new PIN
            new_pin = tk.simpledialog.askstring(
                "New PIN", 
                "Please enter your new PIN:", 
                show='*',
                parent=self.master
            )
            
            if not new_pin:
                return
                
            # Confirm new PIN
            confirm_pin = tk.simpledialog.askstring(
                "Confirm New PIN", 
                "Please confirm your new PIN:", 
                show='*',
                parent=self.master
            )
            
            if not confirm_pin or new_pin != confirm_pin:
                mb.showerror("Error", "PINs do not match")
                return
                
            # Change the PIN
            try:
                self.change_pin(new_pin)
                mb.showinfo("Success", "PIN changed successfully")
                self.master.destroy()
            except Exception as e:
                mb.showerror("Error", f"Failed to change PIN: {e}")

        def DeleteAllClicked():
            # Get current PIN for verification
            current_pin = tk.simpledialog.askstring(
                "Verify PIN", 
                "Please enter your PIN to confirm deletion:", 
                show='*',
                parent=self.master
            )
            
            if not current_pin or current_pin != self.pin:
                mb.showerror("Error", "Incorrect PIN")
                return
                
            # Confirm deletion
            confirm = mb.askyesno(
                "Confirm Delete All",
                "WARNING: This will delete all your saved passwords!\n\nAre you sure you want to continue?"
            )
            if confirm:
                try:
                    # Create a new empty file with the same PIN
                    encryption.gen_file(self.pin)
                    mb.showinfo("Success", "All passwords have been deleted")
                    
                    # Update the list in the main window
                    if self.refresh_callback:
                        self.refresh_callback()
                        
                    self.master.destroy()
                except Exception as e:
                    mb.showerror("Error", f"Failed to delete passwords: {e}")

        ###############
        ### BUTTONS ###
        ###############

        # Frame to hold the buttons
        button_frame = tk.Frame(master, bg="lightblue")
        button_frame.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        # Change PIN Button
        change_pin_button = tk.Button(
            button_frame, text="Change PIN", bg="white", command=ChangePINClicked
        )
        change_pin_button.pack(side=tk.LEFT, padx=(2.5, 2.5))

        # Delete All Button
        delete_all_button = tk.Button(
            button_frame, text="Delete All Passwords", bg="white", command=DeleteAllClicked
        )
        delete_all_button.pack(side=tk.LEFT, padx=(2.5, 2.5))

        ####################
        ### STORAGE PATH ###
        ####################

        # Password Storage Path Label
        path_label = tk.Label(master, text="Password Storage Path:", bg="lightblue")
        path_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=5)

        # Get current path
        current_path = os.path.abspath("passwords")
        
        # Password Storage Path Display
        path_entry = tk.Entry(master, bg="white")
        path_entry.insert(0, current_path)
        path_entry.config(state="readonly")  # Make it read-only
        path_entry.grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 2.5)
        )  # Reduced pady

        # Configure grid columns to expand
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

    def change_pin(self, new_pin):
        """Change the PIN and re-encrypt all passwords"""
        try:
            # Read all current data
            services, info = encryption.read_services(self.pin)
            
            # Prepare data for migration
            data = []
            for i in range(len(services)):
                entry_data = encryption.read_data_by_ID(self.pin, i)
                data.append(entry_data)
            
            # Create new file with new PIN
            encryption.gen_file(new_pin)
            
            # Add all services back with the new PIN
            for i, entry in enumerate(data):
                service_name = entry[0]
                username = entry[1]
                password = entry[2]
                note = info[i] if i < len(info) else ""
                
                encryption.add_service(new_pin, service_name, username, password, note)
                
            # Update main module PIN if it exists
            import gui_main
            gui_main.PIN = new_pin
            
            # Update the list in the main window
            if self.refresh_callback:
                self.refresh_callback()
                
        except Exception as e:
            raise Exception(f"Failed to change PIN: {e}")


def create_gui(master, pin, refresh_callback=None):
    # Need to import here to avoid circular imports
    import tkinter.simpledialog
    settings_gui = SettingsGUI(master, pin, refresh_callback)
    return settings_gui


# Only runs if this script is run directly, for testing
if __name__ == "__main__":
    root = tk.Tk()
    create_gui(root, "1111")
    root.mainloop()