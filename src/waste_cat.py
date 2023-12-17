import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import uuid

class WasteCatFrame(tk.Frame):
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
        columns = ("ID", "City/Town/Barangay", "Area", "Frequency", "Method", "Transportation", "Notes")
        self.table_view = ttk.Treeview(self.scrollable_frame, columns=columns, show="headings", selectmode=tk.BROWSE)
        table_scrollbar_y = ttk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.table_view.yview)
        table_scrollbar_x = ttk.Scrollbar(self.scrollable_frame, orient="horizontal", command=self.table_view.xview)

        self.table_view.config(yscrollcommand=table_scrollbar_y.set, xscrollcommand=table_scrollbar_x.set)

        table_scrollbar_y.grid(row=8, column=1, sticky="ns")
        table_scrollbar_x.grid(row=9, column=0, sticky="ew")

        for col in columns:
            self.table_view.heading(col, text=col)
            self.table_view.column(col, anchor="center", width=100)

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
        # Section 1: Waste Collection and Transportation
        self.create_section_label("Manage Protocol Data", 18, row=0)

        # Separator Line below Label
        self.create_separator(row=0, columnspan=5, pady=(50, 0))

        # Section 2: Data Entry
        data_entry_frame = ttk.Frame(self.scrollable_frame)
        data_entry_frame.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        # City/Town/Barangay Label and Entry
        city_label = ttk.Label(data_entry_frame, text="City/Town/Barangay:")
        city_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.city_entry = ttk.Entry(data_entry_frame, width=30)
        self.city_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Area (sq m) Label and Entry
        area_label = ttk.Label(data_entry_frame, text="Area (sq m):")
        area_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.area_entry = ttk.Entry(data_entry_frame, width=30)
        self.area_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Frequency Label and Entry
        frequency_label = ttk.Label(data_entry_frame, text="Frequency:")
        frequency_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.frequency_entry = ttk.Entry(data_entry_frame, width=30)
        self.frequency_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Categories Label and Listbox (Method)
        categories_label_method = ttk.Label(data_entry_frame, text="Collection Method:")
        categories_label_method.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        category_options_method = [
            "Curbside Pickup", "Container-based Collection", "Drop-off Centers",
            "Roll-off Containers", "Compactor Trucks", "Manual Sorting Stations",
            "Automated Sorting Systems", "Source Separation", "Specialized Collection",
            "Mobile Collection Units"
        ]

        self.categories_listbox_method = tk.Listbox(data_entry_frame, selectmode=tk.MULTIPLE, height=5, width=50)
        for option in category_options_method:
            self.categories_listbox_method.insert(tk.END, option)

        self.categories_listbox_method.grid(row=4, column=1, pady=5, sticky="w")

        categories_scrollbar_method = ttk.Scrollbar(data_entry_frame, orient="vertical", command=self.categories_listbox_method.yview)
        categories_scrollbar_method.grid(row=4, column=2, pady=5, sticky="nse")
        self.categories_listbox_method.config(yscrollcommand=categories_scrollbar_method.set)

        # Add Button for Method Categories
        add_button_method = self.create_button(data_entry_frame, text="Add Method", command=self.add_method, row=4, column=3, padx=5)

        # Stored Categories Label, Listbox, and Scrollbar
        stored_categories_label_method = ttk.Label(data_entry_frame, text="Stored Collection Method:")
        stored_categories_label_method.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        self.stored_categories_listbox_method = tk.Listbox(data_entry_frame, selectmode=tk.MULTIPLE, height=5, width=50)
        self.stored_categories_listbox_method.grid(row=5, column=1, pady=5, sticky="w")

        stored_categories_scrollbar_method = ttk.Scrollbar(data_entry_frame, orient="vertical", command=self.stored_categories_listbox_method.yview)
        stored_categories_scrollbar_method.grid(row=5, column=2, pady=5, sticky="nse")
        self.stored_categories_listbox_method.config(yscrollcommand=stored_categories_scrollbar_method.set)

        # Remove Button for Method Categories
        remove_button_method = self.create_button(data_entry_frame, text="Remove Method", command=self.remove_method, row=5, column=3, padx=5)

        # Categories Label and Listbox (Transportation)
        categories_label_transportation = ttk.Label(data_entry_frame, text="Transportation Method:")
        categories_label_transportation.grid(row=6, column=0, padx=5, pady=5, sticky="w")

        category_options_transportation = [
            "Garbage Trucks", "Recycling Trucks", "Roll-off Trucks", "Front-Loaders",
            "Rear-Loaders", "Side-Loaders", "Transfer Trucks", "Rail Transport",
            "Barge or Ship Transport", "Pipeline Transport", "Cycling and Pedestrian Transport"
        ]

        self.categories_listbox_transportation = tk.Listbox(data_entry_frame, selectmode=tk.MULTIPLE, height=5, width=50)
        for option in category_options_transportation:
            self.categories_listbox_transportation.insert(tk.END, option)

        self.categories_listbox_transportation.grid(row=6, column=1, pady=5, sticky="w")

        categories_scrollbar_transportation = ttk.Scrollbar(data_entry_frame, orient="vertical", command=self.categories_listbox_transportation.yview)
        categories_scrollbar_transportation.grid(row=6, column=2, pady=5, sticky="nse")
        self.categories_listbox_transportation.config(yscrollcommand=categories_scrollbar_transportation.set)

        # Add Button for Transportation Categories
        add_button_transportation = self.create_button(data_entry_frame, text="Add Transportation Type", command=self.add_transportation, row=6, column=3, padx=5)

        # Stored Categories Label, Listbox, and Scrollbar
        stored_categories_label_transportation = ttk.Label(data_entry_frame, text="Stored Transportation Meth:")
        stored_categories_label_transportation.grid(row=7, column=0, padx=5, pady=5, sticky="w")

        self.stored_categories_listbox_transportation = tk.Listbox(data_entry_frame, selectmode=tk.MULTIPLE, height=5, width=50)
        self.stored_categories_listbox_transportation.grid(row=7, column=1, pady=5, sticky="w")

        stored_categories_scrollbar_transportation = ttk.Scrollbar(data_entry_frame, orient="vertical", command=self.stored_categories_listbox_transportation.yview)
        stored_categories_scrollbar_transportation.grid(row=7, column=2, pady=5, sticky="nse")
        self.stored_categories_listbox_transportation.config(yscrollcommand=stored_categories_scrollbar_transportation.set)

        # Remove Button for Transportation Categories
        remove_button_transportation = self.create_button(data_entry_frame, text="Remove Transportation Type", command=self.remove_transportation, row=7, column=3, padx=5)

        # Note(s) Label and Text Box
        notes_label = ttk.Label(data_entry_frame, text="Note(s):")
        notes_label.grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.notes_entry = tk.Text(data_entry_frame, wrap=tk.WORD, height=4, width=30)
        self.notes_entry.grid(row=9, column=1, padx=5, pady=5, sticky="w")

        # Add, Clear, and Save Buttons
        self.create_button(data_entry_frame, text="Add Data", command=self.add_data, row=10, column=0, pady=10)
        self.create_button(data_entry_frame, text="Clear Input", command=self.clear_input, row=10, column=1, pady=10)
        self.save_button = self.create_button(data_entry_frame, text="Update Data", command=self.save_data, state=tk.DISABLED, row=10, column=2, pady=10)

        # Section 3: View/Edit Protocol Data
        table_view_frame = ttk.Frame(self.scrollable_frame)
        table_view_frame.grid(row=11, column=0, pady=10, padx=10, sticky="w")  # Updated row parameter

        # Call create_tree_view to generate the table view
        self.create_tree_view()

        # Buttons for View/Edit Protocol Data section
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
    
    def add_method(self):
        selected_items = self.categories_listbox_method.curselection()
        for index in selected_items:
            category = self.categories_listbox_method.get(index)
            if category not in self.stored_categories_listbox_method.get(0, tk.END):
                self.stored_categories_listbox_method.insert(tk.END, category)

    def remove_method(self):
        selected_items = self.stored_categories_listbox_method.curselection()
        for index in selected_items:
            self.stored_categories_listbox_method.delete(index)

    def add_transportation(self):
        selected_items = self.categories_listbox_transportation.curselection()
        for index in selected_items:
            category = self.categories_listbox_transportation.get(index)
            if category not in self.stored_categories_listbox_transportation.get(0, tk.END):
                self.stored_categories_listbox_transportation.insert(tk.END, category)

    def remove_transportation(self):
        selected_items = self.stored_categories_listbox_transportation.curselection()
        for index in selected_items:
            self.stored_categories_listbox_transportation.delete(index)

    def add_data(self):
        # Get values from input fields
        city = self.city_entry.get()
        area = self.area_entry.get()
        frequency = self.frequency_entry.get()

        # Validate non-empty fields
        if not city or not area or not frequency:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Get selected method categories from the listbox
        selected_method_categories = self.stored_categories_listbox_method.get(0, tk.END)

        # Validate that at least one method category is selected
        if not selected_method_categories:
            messagebox.showerror("Error", "Please select at least one method category.")
            return

        # Combine selected method categories into a comma-separated string
        method_categories_str = ", ".join(selected_method_categories)

        # Get selected transportation categories from the listbox
        selected_transportation_categories = self.stored_categories_listbox_transportation.get(0, tk.END)

        # Validate that at least one transportation category is selected
        if not selected_transportation_categories:
            messagebox.showerror("Error", "Please select at least one transportation category.")
            return

        # Combine selected transportation categories into a comma-separated string
        transportation_categories_str = ", ".join(selected_transportation_categories)

        # Get notes
        notes = self.notes_entry.get("1.0", tk.END).strip()  # Use strip to remove leading/trailing whitespace

        # Generate a random ID
        random_id = self.generate_random_id()

        # Example: Insert data into the Treeview with a random ID
        self.table_view.insert("", "end", values=(random_id, city, area, frequency, method_categories_str, transportation_categories_str, notes), tags=("multiline",))

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
                    "City": city,
                    "Area": area,
                    "Frequency": frequency,
                    "Method Categories": selected_method_categories,
                    "Transportation Categories": selected_transportation_categories,
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
        self.city_entry.delete(0, tk.END)
        self.area_entry.delete(0, tk.END)
        self.frequency_entry.delete(0, tk.END)
        self.stored_categories_listbox_method.delete(0, tk.END)
        self.stored_categories_listbox_transportation.delete(0, tk.END)

        # Show success message
        messagebox.showinfo("Success", "Data added successfully.")

    def get_next_row(self):
        return len(self.scrollable_frame.grid_slaves()) + 1

    def clear_input(self):
        # Clear input fields
        self.city_entry.delete(0, tk.END)
        self.area_entry.delete(0, tk.END)
        self.frequency_entry.delete(0, tk.END)
        self.stored_categories_listbox_method.delete(0, tk.END)
        self.stored_categories_listbox_transportation.delete(0, tk.END)
        self.notes_entry.delete("1.0", tk.END)

        # Disable Save button
        self.save_button.config(state=tk.DISABLED)

    def save_data(self):
        # Get selected item from the Treeview
        selected_item = self.table_view.selection()

        if selected_item:
            # Get values from input fields
            city = self.city_entry.get()
            area = self.area_entry.get()
            frequency = self.frequency_entry.get()

            # Validate non-empty fields
            if not city or not area or not frequency:
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            # Get selected method categories from the listbox
            selected_method_categories = self.stored_categories_listbox_method.get(0, tk.END)

            # Validate that at least one method category is selected
            if not selected_method_categories:
                messagebox.showerror("Error", "Please select at least one method category.")
                return

            # Combine selected method categories into a comma-separated string
            method_categories_str = ", ".join(selected_method_categories)

            # Get selected transportation categories from the listbox
            selected_transportation_categories = self.stored_categories_listbox_transportation.get(0, tk.END)

            # Validate that at least one transportation category is selected
            if not selected_transportation_categories:
                messagebox.showerror("Error", "Please select at least one transportation category.")
                return

            # Combine selected transportation categories into a comma-separated string
            transportation_categories_str = ", ".join(selected_transportation_categories)

            # Get notes
            notes = self.notes_entry.get("1.0", tk.END).strip()  # Use strip to remove leading/trailing whitespace

            # Update the Treeview with edited values
            current_values = self.table_view.item(selected_item, 'values')
            updated_values = (
                current_values[0],  # ID
                city,
                area,
                frequency,
                method_categories_str,
                transportation_categories_str,
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
                                "City": city,
                                "Area": area,
                                "Frequency": frequency,
                                "Method": selected_method_categories,
                                "Transportation": selected_transportation_categories,
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
            messagebox.showinfo("Information", "Please select a protocol data to edit.")

    def delete_data(self):
        # Get selected item from the Treeview
        selected_item = self.table_view.selection()
        if selected_item:
            # Ask for confirmation before deleting
            confirm_delete = messagebox.askokcancel("Confirm Deletion", "Are you sure you want to delete the selected waste data?")

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
            messagebox.showinfo("Information", "Please select a waste data to delete.")


    def create_json(self):
        # Get data from the Treeview
        data_to_save = []

        # Iterate through the items in the Treeview
        for item_id in self.table_view.get_children():
            values = self.table_view.item(item_id, option='values')  # Use option keyword

            # Extract values from the Treeview item
            row_data = {
                "ID": values[0],  # Assuming ID is the first column in the Treeview
                "City": values[1],
                "Area": values[2],
                "Frequency": values[3],
                "Method": values[4].split(", "),  # Assuming Method is the fifth column
                "Transportation": values[5].split(", "),  # Assuming Transportation is the sixth column
                "Notes": values[6]
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

                # Clear existing data in the Treeview
                self.clear_treeview()

                # Set the file path attribute
                self.json_file_path = file_path

                # Iterate over the loaded data and insert it into the Treeview
                for item in data:
                    # Check if "Method" and "Transportation" are lists before splitting
                    if isinstance(item.get("Method"), list):
                        method = ", ".join(item["Method"])
                    else:
                        method = item.get("Method", "")

                    if isinstance(item.get("Transportation"), list):
                        transportation = ", ".join(item["Transportation"])
                    else:
                        transportation = item.get("Transportation", "")

                    # Insert data into the Treeview
                    self.table_view.insert("", "end", values=(
                        item.get("ID", ""),  # Assuming ID is the first key in the dictionary
                        item.get("City", ""),
                        item.get("Area", ""),
                        item.get("Frequency", ""),
                        method,
                        transportation,
                        item.get("Notes", "")
                    ))

                # Show success message
                messagebox.showinfo("Success", f"Data loaded from {file_path}.")

            except Exception as e:
                # Display an error message if there's an issue with reading the file
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

            # Retrieve the ID of the selected row
            selected_id = values[0]

            # Populate input fields
            self.city_entry.delete(0, tk.END)
            self.city_entry.insert(0, values[1])  # Assuming City is the second column

            self.area_entry.delete(0, tk.END)
            self.area_entry.insert(0, values[2])  # Assuming Area is the third column

            self.frequency_entry.delete(0, tk.END)
            self.frequency_entry.insert(0, values[3])  # Assuming Frequency is the fourth column

            # Clear and insert categories into the stored_categories_listbox_method
            self.stored_categories_listbox_method.delete(0, tk.END)
            categories_method = values[4].split(", ")  # Assuming Method is the fifth column
            for category in categories_method:
                self.stored_categories_listbox_method.insert(tk.END, category)

            # Clear and insert categories into the stored_categories_listbox_transportation
            self.stored_categories_listbox_transportation.delete(0, tk.END)
            categories_transportation = values[5].split(", ")  # Assuming Transportation is the sixth column
            for category in categories_transportation:
                self.stored_categories_listbox_transportation.insert(tk.END, category)

            self.notes_entry.delete("1.0", tk.END)
            self.notes_entry.insert(tk.END, values[6])  # Assuming Notes is the eighth column

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
    waste_cat_frame = WasteCatFrame(root)
    root.mainloop()
