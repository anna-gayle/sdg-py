import os
import random
import json
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class ManageWasteDataFrame(tk.Frame):
    """
    Frame for managing waste data through a graphical interface.

    Attributes:
    - canvas: Tkinter canvas for creating a scrollable frame.
    - scrollbar: Tkinter vertical scrollbar for the scrollable frame.
    - scrollable_frame: Tkinter frame that can be scrolled.
    - add_icon, remove_icon, save_icon, delete_icon: Icons for buttons in the frame.
    - city_entry, available_categories_listbox, stored_categories_listbox, quantity_entry, notes_entry: Input widgets.
    - delete_button: Button to delete selected waste data.
    - table_view: Tkinter Treeview for displaying waste data.

    Methods:
    - __init__: Initializes the ManageWasteDataFrame.
    - on_frame_configure: Configures the canvas to enable vertical scrolling.
    - on_canvas_configure: Configures the canvas width based on the window size.
    - create_widgets: Creates and configures widgets within the frame.
    - add_category: Adds selected categories to the stored categories listbox.
    - remove_category: Removes selected stored categories from the listbox.
    - save_data: Saves entered waste data to a JSON file.
    - generate_random_id: Generates a random ID for waste data.
    - save_to_json: Saves data to a JSON file.
    - load_from_json: Loads data from a JSON file to populate the table view.
    - refresh_table: Refreshes the table view by clearing and reloading data.
    - clear_treeview: Clears all entries from the table view.
    - on_treeview_select: Callback function when a row in the table view is selected.
    - delete_data: Deletes selected waste data from the table view and JSON file.
    - delete_from_json: Deletes waste data from the JSON file.
    """
    def __init__(self, master=None):
        """
        Initialize the ManageWasteDataFrame.

        Parameters:
        - master: Tkinter master window.
        """
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
         """
        Configure the canvas to enable vertical scrolling.

        Parameters:
        - event: Tkinter event triggering the method.
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """
        Configure the canvas width based on the window size.

        Parameters:
        - event: Tkinter event triggering the method.
        """
        canvas_width = event.width
        self.canvas.itemconfig(self.scrollable_frame_id, width=canvas_width)

    def create_widgets(self):
        """
        Create and configure widgets within the frame.
        """
        # Load the icon image using PIL
        self.add_icon = Image.open("assets/icons/add-icon.png")
        self.add_icon = ImageTk.PhotoImage(self.add_icon)
        self.remove_icon = Image.open("assets/icons/remove-icon.png")
        self.remove_icon = ImageTk.PhotoImage(self.remove_icon)
        self.save_icon = Image.open("assets/icons/save-icon.png")
        self.save_icon = ImageTk.PhotoImage(self.save_icon)
        self.delete_icon = Image.open("assets/icons/delete-icon.png")
        self.delete_icon = ImageTk.PhotoImage(self.delete_icon)

        # Section 1: Manage Waste Data
        manage_label = ttk.Label(self.scrollable_frame, text="Manage Waste Data", font=("Calibri", 18, "bold"))
        manage_label.grid(row=0, column=0, pady=10, columnspan=2, sticky="w")

        # Separator Line below Manage Label
        separator = ttk.Separator(self.scrollable_frame, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=5, sticky='ew', pady=(0, 10))

        # Section 2: Create Waste Data
        create_data_frame = ttk.Frame(self.scrollable_frame)
        create_data_frame.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        create_label = ttk.Label(create_data_frame, text="Create Waste Data", font=("Calibri", 12, "bold"))
        create_label.grid(row=0, column=0, columnspan=5, pady=10, padx=(0, 10), sticky="w")

        city_label = ttk.Label(create_data_frame, text="City/Town/Barangay:")
        city_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.city_entry = ttk.Entry(create_data_frame, width=30)
        self.city_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        categories_label = ttk.Label(create_data_frame, text="Categories:")
        categories_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        available_categories_listbox = tk.Listbox(create_data_frame, selectmode=tk.MULTIPLE, width=30, height=5)
        available_categories_listbox.grid(row=2, column=1, columnspan=2, padx=(5, 0), pady=5, sticky="w")
        available_categories = [
            "Municipal Solid Waste", "Recyclables", "Organic Waste", "Hazardous Waste",
            "Construction and Demolition Waste", "Biomedical Waste", "Electronic Waste",
            "Agricultural Waste", "Radioactive Waste", "Textile Waste", "Plastic Waste",
            "Rubber Waste", "Glass Waste", "Wood Waste", "Metal Waste", "Paper and Cardboard Waste",
            "Non-Recyclable Plastics"
        ]

        self.available_categories_listbox = tk.Listbox(create_data_frame, selectmode=tk.MULTIPLE, width=30, height=5)
        for category in available_categories:
            self.available_categories_listbox.insert(tk.END, category)

        self.available_categories_listbox.grid(row=2, column=1, columnspan=2, padx=(5, 0), pady=5, sticky="w")

        available_categories_scrollbar = tk.Scrollbar(create_data_frame, orient=tk.VERTICAL, command=self.available_categories_listbox.yview)
        available_categories_scrollbar.grid(row=2, column=2, pady=5, sticky="nse")
        
        self.available_categories_listbox.config(yscrollcommand=available_categories_scrollbar.set)

        add_category_button = tk.Button(create_data_frame, image=self.add_icon, command=self.add_category, bg="#000080", fg="white", relief="flat")
        add_category_button.grid(row=2, column=3, padx=(1, 0), pady=5, sticky="w")

        # Create stored_categories_listbox
        self.stored_categories_listbox = tk.Listbox(create_data_frame, selectmode=tk.MULTIPLE, width=30, height=5)
        self.stored_categories_listbox.grid(row=2, column=4, padx=(5, 0), pady=5, sticky="w")

        # Create scrollbar for stored_categories_listbox with the same style
        stored_categories_scrollbar = tk.Scrollbar(create_data_frame, orient=tk.VERTICAL, command=self.stored_categories_listbox.yview, bg="#000080")
        stored_categories_scrollbar.grid(row=2, column=4, pady=5, sticky="nse")
        
        # Configure stored_categories_listbox
        self.stored_categories_listbox.config(yscrollcommand=stored_categories_scrollbar.set)

        # Create remove_category_button and move it to the right
        remove_category_button = tk.Button(create_data_frame, image=self.remove_icon, command=self.remove_category, bg="#000080", fg="white", relief="flat")
        remove_category_button.grid(row=2, column=5, padx=5, pady=5, sticky="e")

        quantity_label = ttk.Label(create_data_frame, text="Quantity (tonnes):")
        quantity_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.quantity_entry = ttk.Entry(create_data_frame, width=30)
        self.quantity_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        notes_label = ttk.Label(create_data_frame, text="Notes:")
        notes_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.notes_entry = ttk.Entry(create_data_frame, width=30)
        self.notes_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        save_button = tk.Button(create_data_frame, image=self.save_icon, command=self.save_data, bg="#000080", fg="white", relief="flat")
        save_button.grid(row=5, column=0, columnspan=5, pady=10, sticky="w")

        # Section 3: Edit/View Waste Data
        table_view_frame = ttk.Frame(self.scrollable_frame)
        table_view_frame.grid(row=3, column=0, pady=10, padx=10, sticky="w")

        table_label = ttk.Label(table_view_frame, text="View Waste Data", font=("Calibri", 12, "bold"))
        table_label.grid(row=0, column=0, columnspan=3, pady=10, padx=(0, 10), sticky="w")

        # Delete Button (beside the table label)
        self.delete_button = tk.Button(table_view_frame, image=self.delete_icon, command=self.delete_data, state=tk.DISABLED, bg="#000080", fg="white", relief="flat")
        self.delete_button.image = self.delete_icon
        self.delete_button.grid(row=0, column=5, pady=10, padx=(5, 1), sticky="w")  # Adjusted row and column

        columns = ("City/Town/Barangay", "Categories", "Quantity (tonnes)", "Notes")
        self.table_view = ttk.Treeview(table_view_frame, columns=columns, show="headings", selectmode="browse")

        # Adjust the width of each column as needed
        column_widths = [150, 150, 100, 200]
        for col, width in zip(columns, column_widths):
            self.table_view.column(col, width=width)

        for col in columns:
            self.table_view.heading(col, text=col)

        self.table_view.grid(row=1, column=0, pady=5, padx=5, columnspan=3, sticky="w")

        # Enable editing buttons when a row is selected
        self.table_view.bind("<ButtonRelease-1>", self.on_treeview_select)

        # Vertical scrollbar for the Treeview
        table_view_scrollbar = ttk.Scrollbar(table_view_frame, orient="vertical", command=self.table_view.yview)
        table_view_scrollbar.grid(row=1, column=3, pady=5, sticky="nse")
        self.table_view.configure(yscrollcommand=table_view_scrollbar.set)

        # Configure row and column weights
        self.scrollable_frame.grid_rowconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

    def add_category(self):
        """
        Adds selected categories to the stored categories listbox.
        """
        selected_categories = self.available_categories_listbox.curselection()
        categories_to_add = [self.available_categories_listbox.get(idx) for idx in selected_categories]

        # Add selected categories to the stored categories listbox
        for category in categories_to_add:
            self.stored_categories_listbox.insert(tk.END, category)

        # Clear the selection in the available categories listbox
        self.available_categories_listbox.selection_clear(0, tk.END)

    def remove_category(self):
        """
        Removes selected stored categories from the listbox.
        """
        selected_stored_categories = self.stored_categories_listbox.curselection()

        # Remove selected stored categories
        for idx in reversed(selected_stored_categories):
            self.stored_categories_listbox.delete(idx)

    def save_data(self):
        """
        Saves entered waste data to a JSON file.
        """
        try:
            city = self.city_entry.get().strip()
            selected_categories = self.stored_categories_listbox.get(0, tk.END)
            quantity = self.quantity_entry.get().strip()
            note = self.notes_entry.get().strip()

            if not city or not selected_categories or not quantity:
                messagebox.showerror("Error", "Please fill in all required fields.")
                return

            random_id = self.generate_random_id()

            data = {
                "ID": random_id,
                "City": city,
                "Category": selected_categories,
                "Quantity": quantity,
                "Notes": note,
            }

            src_folder_path = os.path.join("src", "data")
            save_path = os.path.join(src_folder_path, "waste_data.json")
            success = self.save_to_json(data, save_path)

            if success:
                self.city_entry.delete(0, tk.END)
                self.stored_categories_listbox.delete(0, tk.END)
                self.quantity_entry.delete(0, tk.END)
                self.notes_entry.delete(0, tk.END)

                self.refresh_table()
                messagebox.showinfo("Success", "Data saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save data. Please try again.")
        except Exception as e:
            print(f"Exception: {e}")

    def generate_random_id(self):
        """
        Generates a random ID for waste data.

        Returns:
        - Random ID (string).
        """
        return str(random.randint(1000, 9999))
    
    def save_to_json(self, data, save_path):
        """
        Saves data to a JSON file.

        Parameters:
        - data: Data to be saved.
        - save_path: Path to the JSON file.

        Returns:
        - True if successful, False otherwise.
        """
        try:
            existing_data = []

            if os.path.exists(save_path):
                with open(save_path, "r") as json_file:
                    existing_data = json.load(json_file)

            if not isinstance(existing_data, list):
                existing_data = [existing_data]

            if not isinstance(data, list):
                data = [data]

            identifier_key = "ID"
            for i, existing_item in enumerate(existing_data):
                if identifier_key in existing_item and existing_item[identifier_key] == data[0].get(identifier_key):
                    existing_data[i] = data[0]
                    break
            else:
                # Join categories into a string
                data[0]["Category"] = ", ".join(data[0]["Category"])
                existing_data.extend(data)

            with open(save_path, "w") as json_file:
                json.dump(existing_data, json_file, indent=4)

            success = True
        except Exception as e:
            print(f"Exception: {e}")
            success = False

        return success

    def load_from_json(self):
        """
        Loads data from a JSON file to populate the table view.
        """
        try:
            src_folder_path = os.path.join("src", "data")
            load_path = os.path.join(src_folder_path, "waste_data.json")

            if os.path.exists(load_path):
                with open(load_path, "r") as json_file:
                    data = json.loads(json_file.read())

                self.clear_treeview()

                if isinstance(data, list):
                    for item in data:
                        # Check if "Category" is a list before splitting
                        if isinstance(item.get("Category"), list):
                            categories = ", ".join(item["Category"])
                        else:
                            categories = item.get("Category", "")
                        
                        self.table_view.insert("", "end", values=(
                            item.get("City", ""),
                            categories,
                            item.get("Quantity", ""),
                            item.get("Notes", "")
                        ))
                elif isinstance(data, dict):
                    # Check if "Category" is a list before splitting
                    if isinstance(data.get("Category"), list):
                        categories = ", ".join(data["Category"])
                    else:
                        categories = data.get("Category", "")
                    
                    self.table_view.insert("", "end", values=(
                        data.get("City", ""),
                        categories,
                        data.get("Quantity", ""),
                        data.get("Notes", "")
                    ))
                else:
                    return
            else:
                return
        except Exception as e:
            print(f"Exception: {e}")

    def refresh_table(self):
        """
        Refreshes the table view by clearing and reloading data.
        """
        self.clear_treeview()
        self.load_from_json()

    def clear_treeview(self):
        """
        Clears all entries from the table view.
        """
        for item in self.table_view.get_children():
            self.table_view.delete(item)

    def on_treeview_select(self, event):
        """
        Callback function when a row in the table view is selected.

        Parameters:
        - event: Tkinter event triggering the method.
        """
        selected_item = self.table_view.selection()

        if selected_item:
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.delete_button.config(state=tk.DISABLED)

    def delete_data(self):
        """
        Deletes selected waste data from the table view and JSON file.
        """
        selected_item = self.table_view.selection()

        if selected_item:
            confirmation = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this entry?")

            if confirmation:
                # Get selected item values
                selected_values = self.table_view.item(selected_item, 'values')

                # Check if values exist
                if selected_values:
                    # Extract selected ID
                    selected_id = selected_values[0]

                    # Delete selected item from the treeview
                    self.table_view.delete(selected_item)

                    # Delete selected data from JSON file
                    self.delete_from_json(selected_id)

                    # Clear input fields
                    self.city_entry.delete(0, tk.END)
                    self.stored_categories_listbox.delete(0, tk.END)
                    self.quantity_entry.delete(0, tk.END)
                    self.notes_entry.delete(0, tk.END)

                    # Disable delete button
                    self.delete_button.config(state=tk.DISABLED)
            else:
                messagebox.showinfo("Information", "Please select a waste data to delete.")

    def delete_from_json(self, selected_id):
        """
        Deletes waste data from the JSON file.

        Parameters:
        - selected_id: ID of the data to be deleted.
        """
        try:
            src_folder_path = os.path.join("src", "data")
            load_path = os.path.join(src_folder_path, "waste_data.json")

            # Load data as a list
            if os.path.exists(load_path):
                with open(load_path, "r") as json_file:
                    data = json.loads(json_file.read())
            else:
                data = []

            # Update list based on ID
            updated_data = [item for item in data if item["ID"] != selected_id]

            # Save updated list
            save_path = os.path.join(src_folder_path, "waste_data.json")
            with open(save_path, "w") as json_file:
                json.dump(updated_data, json_file, indent=4)

            # Show success message
            messagebox.showinfo("Information", "Waste data deleted successfully.")

        except Exception as e:
            print(f"Exception: {e}")
            messagebox.showerror("Error", "Failed to delete waste data. Please try again.")

# Uncomment the following lines for testing the module
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('800x600')
    manage_waste_data_frame = ManageWasteDataFrame(root)
    root.mainloop()
