import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import uuid

class ManageWasteDataFrame(tk.Frame):
    def __init__(self, master=None):
        # Initialize the parent class
        super().__init__(master)

        # Create the main components for the scrollable frame
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Configure the canvas and create window
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Initialize widgets and load data from JSON
        self.create_widgets()

        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind events to their respective handlers
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Create the tree view
        self.create_tree_view()

        # Disable the Save button by default
        self.save_button.config(state=tk.DISABLED)

    def create_tree_view(self):
        # Place the tree view within the scrollable frame
        columns = ("ID", "City/Town/Barangay", "Categories", "Quantity (tonnes)", "Notes")
        self.table_view = ttk.Treeview(self.scrollable_frame, columns=columns, show="headings", selectmode=tk.BROWSE)
        table_scrollbar_y = ttk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.table_view.yview)
        table_scrollbar_x = ttk.Scrollbar(self.scrollable_frame, orient="horizontal", command=self.table_view.xview)

        self.table_view.config(yscrollcommand=table_scrollbar_y.set, xscrollcommand=table_scrollbar_x.set)

        table_scrollbar_y.grid(row=8, column=1, sticky="ns")
        table_scrollbar_x.grid(row=9, column=0, sticky="ew")

        for col in columns:
            self.table_view.heading(col, text=col)
            self.table_view.column(col, anchor="center", width=140)

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

        # Section 1: Manage Waste Data
        self.create_section_label("Manage Waste Data", 18, row=0)

        # Separator Line below Manage Label 
        self.create_separator(row=0, columnspan=5, pady=(50, 0))

        # Section 2: Create Waste Data
        create_data_frame = ttk.Frame(self.scrollable_frame)
        create_data_frame.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        # City/Town/Barangay Label and Entry
        city_label = ttk.Label(create_data_frame, text="City/Town/Barangay:")
        city_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.city_entry = ttk.Entry(create_data_frame, width=30)
        self.city_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Categories Label, Listbox, and Scrollbar
        categories_label = ttk.Label(create_data_frame, text="Categories:")
        categories_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Add options to the listbox
        category_options = ["Municipal Solid Waste", "Recyclables", "Organic Waste", "Hazardous Waste",
                            "Construction and Demolition Waste", "Biomedical Waste", "Electronic Waste",
                            "Agricultural Waste", "Radioactive Waste", "Textile Waste", "Plastic Waste",
                            "Rubber Waste", "Glass Waste", "Wood Waste", "Metal Waste", "Paper and Cardboard Waste",
                            "Non-Recyclable Plastics"]

        self.categories_listbox = tk.Listbox(create_data_frame, selectmode=tk.MULTIPLE, height=5, width=50)
        for option in category_options:
            self.categories_listbox.insert(tk.END, option)

        self.categories_listbox.grid(row=2, column=1, pady=5, sticky="w")

        categories_scrollbar = ttk.Scrollbar(create_data_frame, orient="vertical", command=self.categories_listbox.yview)
        categories_scrollbar.grid(row=2, column=2, pady=5, sticky="nse")
        self.categories_listbox.config(yscrollcommand=categories_scrollbar.set)

        # Add Button for Categories
        add_button = self.create_button(create_data_frame, text="Add Category", command=self.add_category, row=2, column=3, padx=5)

        # Stored Categories Label, Listbox, and Scrollbar
        stored_categories_label = ttk.Label(create_data_frame, text="Stored Categories:")
        stored_categories_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        # Update the stored_categories_listbox creation
        self.stored_categories_listbox = tk.Listbox(create_data_frame, selectmode=tk.MULTIPLE, height=5, width=50)
        self.stored_categories_listbox.grid(row=4, column=1, pady=5, sticky="w")

        stored_categories_scrollbar = ttk.Scrollbar(create_data_frame, orient="vertical", command=self.stored_categories_listbox.yview)
        stored_categories_scrollbar.grid(row=4, column=2, pady=5, sticky="nse")
        self.stored_categories_listbox.config(yscrollcommand=stored_categories_scrollbar.set)

        # Remove Button for Categories
        remove_button = self.create_button(create_data_frame, text="Remove Category", command=self.remove_category, row=4, column=3, padx=5)

        # Quantity (tonnes) Label and Entry
        quantity_label = ttk.Label(create_data_frame, text="Quantity (tonnes):")
        quantity_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.quantity_entry = ttk.Entry(create_data_frame, width=30)
        self.quantity_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Note(s) Label and Text Box
        notes_label = ttk.Label(create_data_frame, text="Note(s):")
        notes_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.notes_entry = tk.Text(create_data_frame, wrap=tk.WORD, height=4, width=30)
        self.notes_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # Add, Clear, and Save Buttons
        self.create_button(create_data_frame, text="Add Data", command=self.add_data, row=7, column=0, pady=10)
        self.create_button(create_data_frame, text="Clear Input", command=self.clear_input, row=7, column=1, pady=10)
        self.save_button = self.create_button(create_data_frame, text="Update Data", command=self.save_data, state=tk.DISABLED, row=7, column=2, pady=10)

        # Section 3: View/Edit Waste Data
        table_view_frame = ttk.Frame(self.scrollable_frame)
        table_view_frame.grid(row=10, column=0, pady=10, padx=10, sticky="w")  # Updated row parameter

        # Call create_tree_view to generate the table view
        self.create_tree_view()

        # Buttons for View/Edit Waste Data section
        self.create_button(table_view_frame, text="Delete Data", command=self.delete_data, row=2, column=0, pady=10)
        self.create_button(table_view_frame, text="Create .json", command=self.create_json, row=2, column=1, pady=10)
        self.create_button(table_view_frame, text="Open .json", command=self.open_json, row=2, column=2, pady=10)

    def create_section_label(self, text, font_size, row=None):
        # Helper function to create section labels
        label = ttk.Label(self.scrollable_frame, text=text, font=("Calibri", font_size, "bold"))
        label.grid(row=row if row is not None else self.get_next_row(), column=0, pady=10, columnspan=5, sticky="w")

    def create_separator(self, row, columnspan, pady):
        # Helper function to create separators
        separator = ttk.Separator(self.scrollable_frame, orient='horizontal')
        separator.grid(row=row, column=0, columnspan=columnspan, sticky='ew', pady=pady)

    def create_button(self, frame, **kwargs):
        # Helper function to create buttons
        row = kwargs.pop("row", None)
        column = kwargs.pop("column", None)
        columnspan = kwargs.pop("columnspan", 1)  # Default to 1 if not specified
        sticky = kwargs.pop("sticky", "e")  # Default to "e" if not specified

        button = tk.Button(frame, **kwargs)
        button.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)

        return button

    def get_next_row(self):
        # Helper function to get the next available row for widgets
        return len(self.scrollable_frame.grid_slaves()) + 1

    def add_category(self):
        selected_items = self.categories_listbox.curselection()
        for index in selected_items:
            category = self.categories_listbox.get(index)
            # Check if the category is not already in the stored listbox
            if category not in self.stored_categories_listbox.get(0, tk.END):
                self.stored_categories_listbox.insert(tk.END, category)

    def remove_category(self):
        # TODO: Implement logic for removing selected categories
        selected_items = self.stored_categories_listbox.curselection()
        for index in selected_items:
            self.stored_categories_listbox.delete(index)

    def add_data(self):
        # Get values from input fields
        city = self.city_entry.get()
        quantity = self.quantity_entry.get()
        notes = self.notes_entry.get("1.0", tk.END).strip()  # Use strip to remove leading/trailing whitespace

        # Validate non-empty fields
        if not city or not quantity or not notes:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Get selected categories from the listbox
        selected_categories = self.stored_categories_listbox.get(0, tk.END)

        # Validate that at least one category is selected
        if not selected_categories:
            messagebox.showerror("Error", "Please select at least one category.")
            return

        # Combine selected categories into a comma-separated string
        categories_str = ", ".join(selected_categories)

        # Generate a random ID
        random_id = self.generate_random_id()

        # Example: Insert data into the Treeview with a random ID
        self.table_view.insert("", "end", values=(random_id, city, categories_str, quantity, notes), tags=("multiline",))

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
                    "Category": selected_categories,
                    "Quantity": quantity,
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
        self.stored_categories_listbox.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.notes_entry.delete("1.0", tk.END)

        # Show success message
        messagebox.showinfo("Success", "Data added successfully.")

    def clear_input(self):
        # TODO: Implement logic for clearing input fields
        self.city_entry.delete(0, tk.END)
        self.stored_categories_listbox.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.notes_entry.delete("1.0", tk.END)

        # Disable Save button
        self.save_button.config(state=tk.DISABLED)

    def save_data(self):
        # TODO: Implement logic for saving data
        selected_item = self.table_view.selection()

        if selected_item:
            # Get values from input fields
            city = self.city_entry.get()
            quantity = self.quantity_entry.get()
            notes = self.notes_entry.get("1.0", tk.END).strip()  # Use strip to remove leading/trailing whitespace

            # Validate non-empty fields
            if not city or not quantity or not notes:
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            # Get selected categories from the listbox
            selected_categories = self.stored_categories_listbox.get(0, tk.END)

            # Validate that at least one category is selected
            if not selected_categories:
                messagebox.showerror("Error", "Please select at least one category.")
                return

            # Combine selected categories into a comma-separated string
            categories_str = ", ".join(selected_categories)

            # Update the Treeview with edited values
            current_values = self.table_view.item(selected_item, 'values')
            updated_values = (current_values[0], city, categories_str, quantity, notes)
            self.table_view.item(selected_item, values=updated_values)

            # Pass the file path to save_data_to_json if available
            file_path = getattr(self, 'json_file_path', None)  # Use the stored file path
            if file_path:
                # Load the existing data from the JSON file
                try:
                    with open(file_path, "r") as json_file:
                        data = json.load(json_file)

                    # Find and update the selected item data in the list
                    selected_item_id = current_values[0]

                    for item in data:
                        # Convert the ID from the JSON data to a string for comparison
                        item_id_str = str(item.get("ID"))

                        if item_id_str == selected_item_id:
                            item.update({"City": city, "Category": selected_categories, "Quantity": quantity, "Notes": notes})
                            break  # Break the loop after updating the item

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
                messagebox.showinfo("Information", "No file path available. Data saved only to the table.")

            # Show success message
            messagebox.showinfo("Success", "Data saved successfully.")

            # Clear input fields
            self.clear_input()
        else:
            messagebox.showinfo("Information", "Please select a waste data to edit.")

    def delete_data(self):
        # TODO: Implement logic for deleting selected data
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

                # Clear input fields
                self.clear_input()
        else:
            messagebox.showinfo("Information", "Please select a waste data to delete.")

    def create_json(self):
        # TODO: Implement logic for creating a .json file based on the table
        data_to_save = []

        # Iterate through the items in the Treeview
        for item_id in self.table_view.get_children():
            values = self.table_view.item(item_id, option='values')  # Use option keyword

            # Extract values from the Treeview item
            row_data = {
                "ID": values[0],  # Assuming ID is the first column in the Treeview
                "City": values[1],
                "Category": values[2].split(", "),
                "Quantity": values[3],
                "Notes": values[4]
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
                    # Check if "Category" is a list before splitting
                    if isinstance(item.get("Category"), list):
                        categories = ", ".join(item["Category"])
                    else:
                        categories = item.get("Category", "")

                    # Insert data into the Treeview
                    self.table_view.insert("", "end", values=(
                        item.get("ID", ""),  # Assuming ID is the first key in the dictionary
                        item.get("City", ""),
                        categories,
                        item.get("Quantity", ""),
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

            # Clear and insert categories into the stored_categories_listbox
            self.stored_categories_listbox.delete(0, tk.END)
            categories = values[2].split(", ")  # Assuming Categories is the third column
            for category in categories:
                self.stored_categories_listbox.insert(tk.END, category)

            self.quantity_entry.delete(0, tk.END)
            self.quantity_entry.insert(0, values[3])  # Assuming Quantity is the fourth column

            self.notes_entry.delete("1.0", tk.END)
            self.notes_entry.insert(tk.END, values[4])  # Assuming Notes is the fifth column

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
    manage_waste_data_frame = ManageWasteDataFrame(root)
    root.mainloop()
