import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import uuid

class WasteFacilityFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Create the main components for the scrollable frame
        self.canvas = tk.Canvas(self)
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Store the id of the scrollable frame window item
        self.scrollable_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")

        # Initialize widgets and load data from JSON
        self.create_widgets()

        # Bind events to their respective handlers
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Create the tree view
        self.create_tree_view()

        # Disable the Save button by default
        self.save_button.config(state=tk.DISABLED)

    def create_tree_view(self):
        # Place the tree view within the scrollable frame
        columns = ("ID", "Facility Name", "Area (sq m)", "Operating Hours", "Address", "Type", "Methods", "Notes")
        self.table_view = ttk.Treeview(self.scrollable_frame, columns=columns, show="headings", selectmode=tk.BROWSE)
        table_scrollbar_y = ttk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.table_view.yview)
        table_scrollbar_x = ttk.Scrollbar(self.scrollable_frame, orient="horizontal", command=self.table_view.xview)

        self.table_view.config(yscrollcommand=table_scrollbar_y.set, xscrollcommand=table_scrollbar_x.set)

        table_scrollbar_y.grid(row=8, column=1, sticky="ns")
        table_scrollbar_x.grid(row=9, column=0, sticky="ew")

        for col in columns:
            self.table_view.heading(col, text=col)
            self.table_view.column(col, anchor="center", width=90)

        self.table_view.grid(row=8, column=0, pady=10, padx=10, sticky="w")

        # Bind the Treeview to the item selection event
        self.table_view.bind("<ButtonRelease-1>", self.on_table_click)

    def on_frame_configure(self, event):
        # Adjust scroll region of the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        # Adjust the width of the scrollable frame when canvas size changes
        self.canvas.itemconfig(self.scrollable_frame_id, width=event.width)

    def create_widgets(self):
        # Section 1: Manage Facility Data
        self.create_section_label("Manage Facility Data", 18, row=0)

        # Separator Line below Label
        self.create_separator(row=0, columnspan=5, pady=(50, 0))

        # Section 2: Data Entry
        data_entry_frame = ttk.Frame(self.scrollable_frame)
        data_entry_frame.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        # Facility Name Label and Entry
        facility_name_label = ttk.Label(data_entry_frame, text="Facility Name:")
        facility_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.facility_name_entry = ttk.Entry(data_entry_frame, width=30)
        self.facility_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Facility Area (sq m) Label and Entry
        area_label = ttk.Label(data_entry_frame, text="Facility Area (sq m):")
        area_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.area_entry = ttk.Entry(data_entry_frame, width=30)
        self.area_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Operating Hours Label and Entry
        hours_label = ttk.Label(data_entry_frame, text="Operating Hours:")
        hours_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.hours_entry = ttk.Entry(data_entry_frame, width=30)
        self.hours_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Address Label and Entry
        address_label = ttk.Label(data_entry_frame, text="Address:")
        address_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.address_entry = ttk.Entry(data_entry_frame, width=30)
        self.address_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Facility Type Label and Menu Button
        type_label = ttk.Label(data_entry_frame, text="Facility Type:")
        type_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        facility_type_options = [
            "Landfills", "Recycling Centers", "Waste-To-Energy Plants",
            "Composting Facilities", "Transfer Stations", "Hazardous Waste Treatment Centers",
            "Material Recovery Facilities", "Incineration Plants", "Biogas Plants",
            "C&D Waste Recycling Centers", "E-Waste Recycling Facilities", "Drop-off Centers"
        ]

        # Set default text for the Combobox
        default_facility_type = "Select Facility Type:"
        self.facility_type_menu = ttk.Combobox(data_entry_frame, values=[default_facility_type] + facility_type_options, width=30)
        self.facility_type_menu.set(default_facility_type)  # Set the default text
        self.facility_type_menu.grid(row=5, column=1, pady=5, sticky="w")

        # Waste Disposal Methods Listbox and Buttons
        disposal_methods_label = ttk.Label(data_entry_frame, text="Waste Disposal Methods:")
        disposal_methods_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")

        disposal_options = [
            "Landfilling", "Recycling", "Incineration", "Composting", "Waste-to-Energy",
            "Anaerobic Digestion", "Hazardous Waste Treatment", "Pyrolysis", "Shredding and Grinding",
            "Land Application", "Reuse/Repurposing", "Deep Well Injection", "Regulated Ocean Dumping"
        ]

        self.disposal_listbox = tk.Listbox(data_entry_frame, selectmode=tk.MULTIPLE, height=5, width=50)
        for option in disposal_options:
            self.disposal_listbox.insert(tk.END, option)

        self.disposal_listbox.grid(row=6, column=1, pady=5, sticky="w")

        disposal_scrollbar = ttk.Scrollbar(data_entry_frame, orient="vertical", command=self.disposal_listbox.yview)
        disposal_scrollbar.grid(row=6, column=2, pady=5, sticky="nse")
        self.disposal_listbox.config(yscrollcommand=disposal_scrollbar.set)

        add_button_disposal = self.create_button(data_entry_frame, text="Add Method", command=self.add_disposal, row=6, column=3, padx=5)

        # Stored Disposal Methods Listbox and Buttons
        stored_disposal_label = ttk.Label(data_entry_frame, text="Stored Disposal Methods:")
        stored_disposal_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")

        self.stored_disposal_listbox = tk.Listbox(data_entry_frame, selectmode=tk.MULTIPLE, height=5, width=50)
        self.stored_disposal_listbox.grid(row=7, column=1, pady=5, sticky="w")

        stored_disposal_scrollbar = ttk.Scrollbar(data_entry_frame, orient="vertical", command=self.stored_disposal_listbox.yview)
        stored_disposal_scrollbar.grid(row=7, column=2, pady=5, sticky="nse")
        self.stored_disposal_listbox.config(yscrollcommand=stored_disposal_scrollbar.set)

        # Remove Button for Stored Disposal Methods
        remove_button_stored_disposal = self.create_button(data_entry_frame, text="Remove Stored Method", command=self.remove_disposal, row=7, column=3, padx=5)

        # Note(s) Label and Text Box
        notes_label = ttk.Label(data_entry_frame, text="Note(s):")
        notes_label.grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.notes_entry = tk.Text(data_entry_frame, wrap=tk.WORD, height=4, width=30)
        self.notes_entry.grid(row=9, column=1, padx=5, pady=5, sticky="w")

        # Add, Clear, and Save Buttons
        self.create_button(data_entry_frame, text="Add Data", command=self.add_data, row=10, column=0, pady=10)
        self.create_button(data_entry_frame, text="Clear Input", command=self.clear_input, row=10, column=1, pady=10)
        self.save_button = self.create_button(data_entry_frame, text="Update Data", command=self.save_data, state=tk.DISABLED, row=10, column=2, pady=10)

        # Section 3: View/Edit Waste Data
        table_view_frame = ttk.Frame(self.scrollable_frame)
        table_view_frame.grid(row=11, column=0, pady=10, padx=10, sticky="w")  # Updated row parameter

        # Call create_tree_view to generate the table view
        self.create_tree_view()

        # Buttons for View/Edit Waste Data section
        self.create_button(table_view_frame, text="Delete Data", command=self.delete_data, row=2, column=0, pady=10)
        self.create_button(table_view_frame, text="Create .json", command=self.create_json, row=2, column=1, pady=10)
        self.create_button(table_view_frame, text="Open .json", command=self.open_json, row=2, column=2, pady=10)

    def create_section_label(self, text, font_size, row=None):
        label = ttk.Label(self.scrollable_frame, text=text, font=("Calibri", font_size, "bold"))
        label.grid(row=row if row is not None else self.get_next_row(), column=0, pady=10, columnspan=5, sticky="w")

    def create_separator(self, row, columnspan, pady):
        separator = ttk.Separator(self.scrollable_frame, orient='horizontal')
        separator.grid(row=row, column=0, columnspan=columnspan, sticky='ew', pady=pady)

    def create_button(self, frame, **kwargs):
        row = kwargs.pop("row", None)
        column = kwargs.pop("column", None)
        columnspan = kwargs.pop("columnspan", 1)
        sticky = kwargs.pop("sticky", "e")

        button = tk.Button(frame, **kwargs)
        button.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)

        return button

    def get_next_row(self):
        # Get the next available row in the grid
        row = self.row_index
        self.row_index += 1
        return row

    def get_menu_item(self, menu, item_text):
        # Get menu item from the menu
        for item in menu.children.values():
            if item.cget("label") == item_text:
                return item
        return None

    def add_disposal(self):
        # Add selected disposal method to the Listbox
        selected_item = self.disposal_listbox.curselection()
        if selected_item:
            method = self.disposal_listbox.get(selected_item)
            self.stored_disposal_listbox.insert(tk.END, method)

    def remove_disposal(self):
        # Remove selected disposal method from the Listbox
        selected_item = self.stored_disposal_listbox.curselection()
        if selected_item:
            self.stored_disposal_listbox.delete(selected_item)

    def add_data(self):
        # Get values from input fields
        facility_name = self.facility_name_entry.get()
        area = self.area_entry.get()
        operating_hours = self.hours_entry.get()
        address = self.address_entry.get()
        facility_type = self.facility_type_menu.get()
        # Get selected disposal methods from the listbox
        selected_disposal_methods = self.stored_disposal_listbox.get(0, tk.END)


        # Validate non-empty fields
        if not facility_name or not area or not operating_hours or not address or not facility_type or not selected_disposal_methods:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Get notes
        notes = self.notes_entry.get("1.0", tk.END).strip()  # Use strip to remove leading/trailing whitespace

        # Generate a random ID
        random_id = self.generate_random_id()

        # Example: Insert data into the Treeview with a random ID
        self.table_view.insert("", "end", values=(random_id, facility_name, area, operating_hours, address, facility_type, selected_disposal_methods, notes), tags=("multiline",))

        # Pass the file path to add_data_to_json if available
        file_path = getattr(self, 'json_file_path', None)  # Use the stored file path
        if file_path:
            # Load the existing data from the JSON file
            try:
                with open(file_path, "r") as json_file:
                    data = json.load(json_file)

                # Add the new data to the list
                new_data = {
                    "ID": random_id,
                    "Facility Name": facility_name,
                    "Area": area,
                    "Operating Hours": operating_hours,
                    "Address": address,
                    "Facility Type": facility_type,
                    "Disposal Methods": selected_disposal_methods,
                    "Notes": notes
                }
                data.append(new_data)

                # Save the modified data back to the JSON file
                with open(file_path, "w") as json_file:
                    json.dump(data, json_file, indent=4)

            except FileNotFoundError:
                messagebox.showerror("Error", f"File not found: {file_path}")
            except json.JSONDecodeError as e:
                messagebox.showerror("Error", f"Error decoding JSON from {file_path}: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        else:
            # If file path is not available, display a message
            messagebox.showinfo("Information", "No file path available. Data added only to the table.")

        # Clear input fields
        self.clear_input()

        # Show success message
        messagebox.showinfo("Success", "Data added successfully.")

    def get_next_row(self):
        return len(self.scrollable_frame.grid_slaves()) + 1
    
    def clear_input(self):
        # Clear input fields
        self.facility_name_entry.delete(0, tk.END)
        self.area_entry.delete(0, tk.END)  # Updated the attribute name
        self.hours_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.facility_type_menu.set("Select Facility Type")
        self.stored_disposal_listbox.delete(0, tk.END)
        self.notes_entry.delete("1.0", tk.END)

    def save_data(self):
        # Get selected item from the Treeview
        selected_item = self.table_view.selection()

        if selected_item:
            # Get values from input fields
            facility_name = self.facility_name_entry.get()
            area = self.area_entry.get()
            operating_hours = self.hours_entry.get()
            address = self.address_entry.get()
            facility_type = self.facility_type_menu.get()
            disposal_methods = self.stored_disposal_listbox.get(0, tk.END)

            # Validate non-empty fields
            if not facility_name or not area or not operating_hours or not address or not facility_type or not disposal_methods:
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            # Get notes
            notes = self.notes_entry.get("1.0", tk.END).strip()  # Use strip to remove leading/trailing whitespace

            # Update the Treeview with edited values
            current_values = self.table_view.item(selected_item, 'values')
            updated_values = (
                current_values[0],  # ID
                facility_name,
                area,
                operating_hours,
                address,
                facility_type,
                disposal_methods,
                notes
            )
            self.table_view.item(selected_item, values=updated_values)

            # Update the corresponding data in the JSON file
            file_path = getattr(self, 'json_file_path', None)
            if file_path:
                try:
                    with open(file_path, "r") as json_file:
                        data = json.load(json_file)

                    # Find and update the selected item data in the list
                    selected_item_id = current_values[0]
                    for item in data:
                        if str(item.get("ID")) == selected_item_id:
                            item.update({
                                "Facility Name": facility_name,
                                "Area": area,
                                "Operating Hours": operating_hours,
                                "Address": address,
                                "Facility Type": facility_type,
                                "Disposal Methods": disposal_methods,
                                "Notes": notes
                            })

                    # Save the modified data back to the JSON file
                    with open(file_path, "w") as json_file:
                        json.dump(data, json_file, indent=4)

                    # Show success message
                    messagebox.showinfo("Success", "Data saved successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            else:
                messagebox.showinfo("Information", "No file path available. Data saved only to the table.")

            # Clear input fields
            self.clear_input()
        else:
            messagebox.showinfo("Information", "Please select a facility data to edit.")

    def delete_data(self):
        # Get selected item from the Treeview
        selected_item = self.table_view.selection()
        if selected_item:
            # Ask for confirmation before deleting
            confirm_delete = messagebox.askokcancel("Confirm Deletion", "Are you sure you want to delete the selected waste facility data?")

            if confirm_delete:
                # Pass the file path to delete_data_from_json if available
                file_path = getattr(self, 'json_file_path', None)  # Use the stored file path

                # User confirmed, proceed with deletion
                values = self.table_view.item(selected_item, 'values')
                self.table_view.delete(selected_item)

                if file_path:
                    # Load the existing data from the JSON file
                    try:
                        with open(file_path, "r") as json_file:
                            data = json.load(json_file)

                        # Find and remove the selected item data from the list
                        selected_item_id = values[0]  # Assuming ID is the first column
                        data = [item for item in data if str(item.get("ID")) != selected_item_id]

                        # Save the modified data back to the JSON file
                        with open(file_path, "w") as json_file:
                            json.dump(data, json_file, indent=4)

                    except FileNotFoundError:
                        messagebox.showerror("Error", f"File not found: {file_path}")
                    except json.JSONDecodeError as e:
                        messagebox.showerror("Error", f"Error decoding JSON from {file_path}: {str(e)}")
                    except Exception as e:
                        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
                else:
                    # If file path is not available, display a message
                    messagebox.showinfo("Information", "No file path available. Data deleted only from the table.")

                # Show success message
                messagebox.showinfo("Success", "Data deleted successfully.")
        else:
            messagebox.showinfo("Information", "Please select a waste facility data to delete.")

    def create_json(self):
        # Get data from the Treeview
        data_to_save = []

        # Iterate through the items in the Treeview
        for item_id in self.table_view.get_children():  # Fix the variable name here
            values = self.table_view.item(item_id, option='values')  # Use option keyword

            # Extract values from the Treeview item
            row_data = {
                "ID": values[0],  # Assuming ID is the first column in the Treeview
                "Facility Name": values[1],
                "Area": values[2],
                "Operating Hours": values[3],
                "Address": values[4],
                "Facility Type": values[5],
                "Disposal Methods": values[6].split(", "),  # Assuming Disposal Methods is the seventh column
                "Notes": values[7]
            }

            # Append the row data to the list
            data_to_save.append(row_data)

        # Specify the path for saving the JSON file
        save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

        if save_path:
            # Save the data to the JSON file
            with open(save_path, "w") as json_file:
                json.dump(data_to_save, json_file, indent=4)

            # Show success message
            messagebox.showinfo("Success", "JSON file created successfully.")

    def open_json(self):
        # Prompt the user to select a JSON file
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

        if file_path:
            try:
                # Read the JSON file
                with open(file_path, "r") as json_file:
                    data = json.load(json_file)

                # Clear existing data in the Treeview (named table_view)
                self.clear_treeview()

                # Set the file path attribute
                self.json_file_path = file_path

                # Iterate over the loaded data and insert it into the Treeview
                for item in data:
                    # Check if "Disposal Methods" is a list before joining
                    if isinstance(item.get("Disposal Methods"), list):
                        disposal_methods = ", ".join(item["Disposal Methods"])
                    else:
                        disposal_methods = item.get("Disposal Methods", "")

                    # Insert data into the Treeview
                    self.table_view.insert("", "end", values=(
                        item.get("ID", ""),  # Assuming ID is the first key in the dictionary
                        item.get("Facility Name", ""),
                        item.get("Area", ""),
                        item.get("Operating Hours", ""),
                        item.get("Address", ""),
                        item.get("Facility Type", ""),
                        disposal_methods,
                        item.get("Notes", "")
                    ))

                # Show success message
                messagebox.showinfo("Success", f"Data loaded from {file_path}.")

            except FileNotFoundError:
                messagebox.showerror("Error", f"File not found: {file_path}")
            except json.JSONDecodeError:
                messagebox.showerror("Error", f"Error decoding JSON in {file_path}. Please ensure it's a valid JSON file.")
            except Exception as e:
                # Display a generic error message for other exceptions
                messagebox.showerror("Error", f"Error loading data from {file_path}: {str(e)}")

    def clear_treeview(self):
        """
        Clear all items in the Treeview widget.
        """
        for item in self.table_view.get_children():
            self.table_view.delete(item)

    def on_table_click(self, event):
        # Retrieve the selected item from the Treeview
        selected_item = self.table_view.selection()

        # If an item is selected, populate the input fields with its data
        if selected_item:
            values = self.table_view.item(selected_item, 'values')

            # Clear the stored_disposal_listbox
            self.stored_disposal_listbox.delete(0, tk.END)

            # Retrieve the ID of the selected row
            selected_id = values[0]

            # Populate input fields
            self.facility_name_entry.delete(0, tk.END)
            self.facility_name_entry.insert(0, values[1])  # Assuming Facility Name is the second column

            self.area_entry.delete(0, tk.END)
            self.area_entry.insert(0, values[2])  # Assuming Area is the third column

            self.hours_entry.delete(0, tk.END)
            self.hours_entry.insert(0, values[3])  # Assuming Operating Hours is the fourth column

            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, values[4])  # Assuming Address is the fifth column

            # Clear and insert categories into the facility_type_menu
            self.facility_type_menu.set(values[5])  # Assuming Facility Type is the sixth column

            # Clear and insert disposal methods into the stored_disposal_listbox
            disposal_methods = values[6].split(", ")  # Assuming Disposal Methods is the seventh column
            for method in disposal_methods:
                self.stored_disposal_listbox.insert(tk.END, method)

            self.notes_entry.delete("1.0", tk.END)
            self.notes_entry.insert(tk.END, values[7])  # Assuming Notes is the eighth column

            # Enable Save button
            self.save_button.config(state=tk.NORMAL)

        else:
            # If no item is selected, disable the Save button
            self.save_button.config(state=tk.DISABLED)

    def generate_random_id(self):
        """
        Generate a random ID.
        """
        random_id = str(uuid.uuid4().hex)[:8]  # Extract the first 8 characters of the UUID
        return random_id

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('800x600')
    waste_facility_frame = WasteFacilityFrame(root)
    root.mainloop()


