import os
import random
import json
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class WasteFacilityFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.create_widgets()

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.load_from_json()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.scrollable_frame_id, width=canvas_width)

    def create_widgets(self):
        # Load the icon image using PIL
        self.add_icon = Image.open("assets/icons/add-icon.png")
        self.add_icon = ImageTk.PhotoImage(self.add_icon)
        self.remove_icon = Image.open("assets/icons/remove-icon.png")
        self.remove_icon = ImageTk.PhotoImage(self.remove_icon)
        self.save_icon = Image.open("assets/icons/save-icon.png")
        self.save_icon = ImageTk.PhotoImage(self.save_icon)
        self.edit_icon = Image.open("assets/icons/edit-icon.png")
        self.edit_icon = ImageTk.PhotoImage(self.edit_icon)
        self.delete_icon = Image.open("assets/icons/delete-icon.png")
        self.delete_icon = ImageTk.PhotoImage(self.delete_icon)

        # Section 1: Waste Facility
        manage_label = ttk.Label(self.scrollable_frame, text="Waste Facility Management", font=("Calibri", 18, "bold"))
        manage_label.grid(row=0, column=0, pady=10, columnspan=2, sticky="w")

        # Separator Line below Manage Label
        separator = ttk.Separator(self.scrollable_frame, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=5, sticky='ew', pady=(0, 10))

        # Section 2: Facility Information
        create_data_frame = ttk.Frame(self.scrollable_frame)
        create_data_frame.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        create_label = ttk.Label(create_data_frame, text="Create Facility", font=("Calibri", 12, "bold"))
        create_label.grid(row=0, column=0, columnspan=5, pady=10, padx=(0, 10), sticky="w")

        # Facility Name
        facility_name_label = ttk.Label(create_data_frame, text="Facility Name:")
        facility_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.facility_name_entry = ttk.Entry(create_data_frame, width=30)
        self.facility_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Facility Area (sq m)
        facility_area_label = ttk.Label(create_data_frame, text="Facility Area (sq m):")
        facility_area_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.facility_area_entry = ttk.Entry(create_data_frame, width=30)
        self.facility_area_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Operating Hours
        operating_hours_label = ttk.Label(create_data_frame, text="Operating Hours:")
        operating_hours_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.operating_hours_entry = ttk.Entry(create_data_frame, width=30)
        self.operating_hours_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Address
        address_label = ttk.Label(create_data_frame, text="Address:")
        address_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.address_entry = ttk.Entry(create_data_frame, width=30)
        self.address_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        # Facility Type
        facility_type_label = ttk.Label(create_data_frame, text="Facility Type:")
        facility_type_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        facility_type_values = [
            "Landfills", "Recycling Centers", "Waste-To-Energy Plants",
            "Composting Facilities", "Transfer Stations", "Hazardous Waste Treatment Centers",
            "Material Recovery Facilities", "Incineration Plants", "Biogas Plants",
            "C&D Waste Recycling Centers", "E-Waste Recycling Facilities", "Drop-off Centers"
        ]
        self.facility_type_combobox = ttk.Combobox(create_data_frame, values=facility_type_values, state="readonly")
        self.facility_type_combobox.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        self.facility_type_combobox.set("Landfills")  # Set default value

        # Waste Disposal Methods
        disposal_methods_label = ttk.Label(create_data_frame, text="Waste Disposal Methods:")
        disposal_methods_label.grid(row=6, column=0, padx=5, pady=10, sticky="w")

        # Listbox for available methods
        self.available_methods_listbox = tk.Listbox(create_data_frame, selectmode=tk.MULTIPLE, width=30)
        self.available_methods_listbox.grid(row=6, column=1, padx=5, pady=10, sticky="w")

        # Scrollbar for available methods listbox
        available_methods_scrollbar = tk.Scrollbar(create_data_frame, orient=tk.VERTICAL, command=self.available_methods_listbox.yview)
        available_methods_scrollbar.grid(row=6, column=2, pady=10, sticky="nse")
        self.available_methods_listbox.config(yscrollcommand=available_methods_scrollbar.set)

        # Populate available methods listbox
        for method in ["Landfilling", "Recycling", "Incineration", "Composting", "Waste-to-Energy", "Anaerobic Digestion", "Hazardous Waste Treatment", "Pyrolysis", "Shredding and Grinding", "Land Application", "Reuse/Repurposing", "Deep Well Injection", "Ocean Dumping"]:
            self.available_methods_listbox.insert(tk.END, method)

        # Buttons for adding and removing methods
        add_method_button = tk.Button(create_data_frame, text="Add Method", command=self.add_disposal_method, image=self.add_icon, bg="#000080", fg="white", relief="flat")
        add_method_button.grid(row=6, column=3, padx=5, pady=10, sticky="w")

        # Listbox for selected methods
        self.selected_methods_listbox = tk.Listbox(create_data_frame, selectmode=tk.MULTIPLE, width=30)
        self.selected_methods_listbox.grid(row=6, column=4, padx=5, pady=10, sticky="w")

        # Scrollbar for selected methods listbox
        selected_methods_scrollbar = tk.Scrollbar(create_data_frame, orient=tk.VERTICAL, command=self.selected_methods_listbox.yview)
        selected_methods_scrollbar.grid(row=6, column=5, pady=10, sticky="nse")
        self.selected_methods_listbox.config(yscrollcommand=selected_methods_scrollbar.set)

        # Buttons for adding and removing methods
        remove_method_button = tk.Button(create_data_frame, text="Remove Method", command=self.remove_disposal_method, image=self.remove_icon, bg="#000080", fg="white", relief="flat")
        remove_method_button.grid(row=6, column=6, padx=5, pady=10, sticky="e")

        # Save Button
        save_button = tk.Button(create_data_frame, text="Save", command=self.save_facility_data, image=self.save_icon, bg="#000080", fg="white", relief="flat")
        save_button.grid(row=7, column=0, padx=5, pady=5, sticky="w")

        # Section 3: Display Facilities Table
        facility_table_frame = ttk.Frame(self.scrollable_frame)
        facility_table_frame.grid(row=3, column=0, pady=10, padx=10, sticky="w")

        table_label = ttk.Label(facility_table_frame, text="Edit/View Facility Data", font=("Calibri", 12, "bold"))
        table_label.grid(row=0, column=0, columnspan=6, pady=10, padx=(0, 10), sticky="w")

        # Create Treeview widget
        columns = ("Facility Name", "Area (sq m)", "Operating Hours", "Address", "Type", "Methods")
        self.facility_tree = ttk.Treeview(facility_table_frame, columns=columns, show="headings", selectmode="browse")

        # Set column headings
        for col in columns:
            self.facility_tree.heading(col, text=col)
            self.facility_tree.column(col, width=100)  # Adjust width as needed

        # Add Treeview to layout
        self.facility_tree.grid(row=1, column=0, sticky="nsew")  # Adjusted row index

        # Add scrollbar
        tree_scroll = ttk.Scrollbar(facility_table_frame, orient="vertical", command=self.facility_tree.yview)
        tree_scroll.grid(row=1, column=1, sticky="ns")  # Adjusted row index
        self.facility_tree.configure(yscrollcommand=tree_scroll.set)

        # Bind the Treeview widget's selection event to a callback function
        self.facility_tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Delete Button
        self.delete_button = tk.Button(facility_table_frame, text="Delete", image=self.delete_icon, command=self.delete_data, state=tk.DISABLED, bg="#000080", fg="white", relief="flat")
        self.delete_button.grid(row=0, column=2, pady=(20, 0), padx=(5, 0), sticky="w")  # Adjusted pady value


    def add_disposal_method(self):
        selected_methods = self.available_methods_listbox.curselection()
        available_methods = [self.available_methods_listbox.get(idx) for idx in selected_methods]

        # Add selected methods to the stored methods listbox
        for method in available_methods:
            self.selected_methods_listbox.insert(tk.END, method)

        # Clear the selection in the available methods listbox
        self.available_methods_listbox.selection_clear(0, tk.END)

    def remove_disposal_method(self):
        selected_selected_methods = self.selected_methods_listbox.curselection()

        # Remove selected stored methods
        for idx in reversed(selected_selected_methods):
            self.selected_methods_listbox.delete(idx)

    def save_facility_data(self):
        try:
            # Get values from entry fields, combobox, and listbox
            facility_name = self.facility_name_entry.get().strip()
            facility_area = self.facility_area_entry.get().strip()
            operating_hours = self.operating_hours_entry.get().strip()
            address = self.address_entry.get().strip()

            # Retrieve facility type from the combobox
            facility_type = self.facility_type_combobox.get()

            selected_methods = self.selected_methods_listbox.get(0, tk.END)

            # Check if any of the required fields are empty
            if not facility_name or not facility_area or not operating_hours or not address or not facility_type or not selected_methods:
                # Display an error message
                messagebox.showerror("Error", "Please fill in all required fields.")
                return

            # Generate a random ID (you may need to implement your own logic)
            random_id = self.generate_random_id()

            # Create a data dictionary with the collected information
            data = {
                "ID": random_id,
                "FacilityName": facility_name,
                "FacilityArea": facility_area,
                "OperatingHours": operating_hours,
                "Address": address,
                "FacilityType": facility_type,
                "DisposalMethods": selected_methods,
            }

            # Determine the path to the "src" folder
            src_folder_path = os.path.join("src", "data")

            # Save data to a JSON file ("facility_data.json") inside the "src" folder
            save_path = os.path.join(src_folder_path, "facility_data.json")

            success = self.save_to_json(data, save_path)

            # Provide feedback through a message box
            if success:
                # Clear fields after successful save
                self.facility_name_entry.delete(0, tk.END)
                self.facility_area_entry.delete(0, tk.END)
                self.operating_hours_entry.delete(0, tk.END)
                self.address_entry.delete(0, tk.END)
                self.facility_type_combobox.set("Landfills")  # Set default value
                self.selected_methods_listbox.delete(0, tk.END)

                self.refresh_table()
                messagebox.showinfo("Success", "Facility data saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save facility data. Please try again.")
        except Exception as e:
            print(f"Exception: {e}")

    def load_from_json(self):
        try:
            # Determine the path to the "src" folder
            src_folder_path = os.path.join("src", "data")

            # Load data from the "facility_data.json" file inside the "src" folder
            load_path = os.path.join(src_folder_path, "facility_data.json")

            if os.path.exists(load_path):
                with open(load_path, "r") as json_file:
                    data = json.loads(json_file.read())

                # Clear existing data in the Treeview
                self.clear_treeview()

                if isinstance(data, list):
                    # Populate the Treeview with loaded data (list of dictionaries)
                    for item in data:
                        self.facility_tree.insert("", "end", values=(
                            item.get("FacilityName", ""),
                            item.get("FacilityArea", ""),
                            item.get("OperatingHours", ""),
                            item.get("Address", ""),
                            item.get("FacilityType", ""),
                            ", ".join(item.get("DisposalMethods", []))
                        ))
                elif isinstance(data, dict):
                    # Populate the Treeview with loaded data (single dictionary)
                    self.facility_tree.insert("", "end", values=(
                        data.get("FacilityName", ""),
                        data.get("FacilityArea", ""),
                        data.get("OperatingHours", ""),
                        data.get("Address", ""),
                        data.get("FacilityType", ""),
                        ", ".join(data.get("DisposalMethods", []))
                    ))
                else:
                    return

            else:
                return

        except Exception as e:
            return

    def save_to_json(self, data, save_path):
        try:
            with open(save_path, "w") as json_file:
                json.dump(data, json_file, indent=4)
            success = True
        except Exception as e:
            print(f"Exception: {e}")
            success = False
        return success
    
    def on_tree_select(self, event):
        selected_item = self.facility_tree.selection()
        if selected_item:
            self.edit_button["state"] = tk.NORMAL
            self.delete_button["state"] = tk.NORMAL
        else:
            self.edit_button["state"] = tk.DISABLED
            self.delete_button["state"] = tk.DISABLED

    def edit_data(self):
        # Get the selected item from the Treeview
        selected_item = self.facility_tree.selection()

        if selected_item:
            # Get the values from the selected item
            values = self.facility_tree.item(selected_item, 'values')

            # Check if the length of the values tuple is sufficient
            if len(values) >= 6:
                # Enable editing mode
                self.edit_mode = True

                # Populate the entry fields with selected data for editing
                self.facility_name_entry.delete(0, tk.END)
                self.facility_name_entry.insert(0, values[0])

                self.facility_area_entry.delete(0, tk.END)
                self.facility_area_entry.insert(0, values[1])

                self.operating_hours_entry.delete(0, tk.END)
                self.operating_hours_entry.insert(0, values[2])

                self.address_entry.delete(0, tk.END)
                self.address_entry.insert(0, values[3])

                # Set default value if facility type is not available in the loaded data
                facility_type = values[4] if len(values) > 4 else "Landfills"
                self.facility_type_combobox.set(facility_type)

                # Clear existing data in the selected methods listbox
                self.selected_methods_listbox.delete(0, tk.END)

                # Check if the disposal methods are available
                if len(values) > 5 and values[5]:
                    stored_methods = values[5].split(', ')
                    for method in stored_methods:
                        self.selected_methods_listbox.insert(tk.END, method)

                # Disable buttons during editing
                self.edit_button.config(state=tk.DISABLED)
                self.delete_button.config(state=tk.DISABLED)
            else:
                messagebox.showinfo("Information", "Selected item does not have sufficient data for editing.")
        else:
            messagebox.showinfo("Information", "Please select a facility to edit.")

    def delete_data(self):
        # Get the selected item from the Treeview
        selected_item = self.facility_tree.selection()

        if selected_item:
            # Ask for confirmation before deletion
            confirmation = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this entry?")

            if confirmation:
                # Get the ID of the selected item
                selected_id = self.facility_tree.item(selected_item, 'values')[0]

                # Delete the selected item from the Treeview
                self.facility_tree.delete(selected_item)

                # Delete the selected item from the JSON file
                self.delete_from_json(selected_id)

                # Clear entry fields
                self.facility_name_entry.delete(0, tk.END)
                self.facility_area_entry.delete(0, tk.END)
                self.operating_hours_entry.delete(0, tk.END)
                self.address_entry.delete(0, tk.END)
                self.facility_type_combobox.set("Landfills")  # Set default value
                self.selected_methods_listbox.delete(0, tk.END)

                # Disable buttons after deletion
                self.edit_button.config(state=tk.DISABLED)
                self.delete_button.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Information", "Please select a facility to delete.")


    def delete_from_json(self, selected_id):
        try:
            # Determine the path to the "src" folder
            src_folder_path = os.path.join("src", "data")

            # Load data from the "facility_data.json" file inside the "src" folder
            load_path = os.path.join(src_folder_path, "facility_data.json")

            if os.path.exists(load_path):
                with open(load_path, "r") as json_file:
                    data = json.loads(json_file.read())

                if isinstance(data, list):
                    # Remove the item with the specified ID from the list
                    data = [item for item in data if item.get("ID") != id]

                    # Save the updated data back to the JSON file
                    save_path = os.path.join(src_folder_path, "facility_data.json")
                    success = self.save_to_json(data, save_path)

                    if success:
                        messagebox.showinfo("Information", "Facility data deleted successfully.")
                    else:
                        messagebox.showerror("Error", "Failed to delete facility data. Please try again.")
                elif isinstance(data, dict):
                    # Clear the data in the JSON file since it's a single dictionary
                    success = self.save_to_json({}, load_path)

                    if success:
                        messagebox.showinfo("Information", "Facility data deleted successfully.")
                    else:
                        messagebox.showerror("Error", "Failed to delete facility data. Please try again.")
                else:
                    messagebox.showerror("Error", "Invalid data format in JSON file.")
            else:
                messagebox.showerror("Error", "JSON file not found.")

        except Exception as e:
            print(f"Exception: {e}")

    def generate_random_id(self):
        return str(random.randint(1000, 9999))
    
    def refresh_table(self):
        # Clear existing data in the Treeview
        self.clear_treeview()

        # Load and display updated data from the JSON file
        self.load_from_json()

    def clear_treeview(self):
        # Implement logic to clear existing data in the treeview
        for item in self.facility_tree.get_children():
            self.facility_tree.delete(item)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('800x600')
    
    manage_waste_data_frame = WasteFacilityFrame(root)
    root.mainloop()
