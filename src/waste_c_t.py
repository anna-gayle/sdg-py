import os
import random
import json
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class WasteCATFrame(tk.Frame):
    """
    WasteCATFrame is a class representing the main frame of the Waste Collection and Transportation application.

    Attributes:
    - canvas: Canvas widget for scrolling functionality.
    - scrollbar: Vertical scrollbar for the canvas.
    - scrollable_frame: Frame inside the canvas to hold widgets.
    - add_icon, remove_icon, save_icon, delete_icon: Icons for buttons.
    - city_entry, area_entry, frequency_entry: Entry widgets for user input.
    - method_listbox, stored_methods_listbox: Listboxes for displaying and storing selected waste collection methods.
    - transportation_listbox, stored_transportation_listbox: Listboxes for displaying and storing selected transportation methods.
    - delete_button: Button to delete selected data from the Treeview.
    - table_view: Treeview widget to display waste collection and transportation data.

    Methods:
    - on_frame_configure: Adjusts the canvas scroll region when the frame is configured.
    - on_canvas_configure: Adjusts the canvas item when the canvas is configured.
    - create_widgets: Creates and organizes all widgets in the main frame.
    - add_method, remove_method, add_transportation, remove_transportation: Methods to handle listbox operations.
    - save_data: Saves user input data to a JSON file.
    - save_to_json: Saves data to a JSON file.
    - load_from_json: Loads data from a JSON file and populates the Treeview.
    - refresh_table: Clears and reloads data into the Treeview.
    - clear_treeview: Clears data from the Treeview.
    - on_treeview_select: Enables delete button when a row is selected.
    - generate_random_id: Generates a random ID for data entries.
    - delete_data, delete_from_json: Handles deletion of data from the Treeview and JSON file.

    """
    def __init__(self, master=None):
        """
        Initializes the WasteCATFrame.

        Args:
        - master: Parent widget.
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
        Adjusts the canvas scroll region when the frame is configured.

        Args:
        - event: Event triggering the method.
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """
        Adjusts the canvas item when the canvas is configured.

        Args:
        - event: Event triggering the method.
        """
        canvas_width = event.width
        self.canvas.itemconfig(self.scrollable_frame_id, width=canvas_width)

    def create_widgets(self):
        """
        Creates and organizes all widgets in the main frame.
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

        # Section 1: Waste CnT
        manage_label = ttk.Label(self.scrollable_frame, text="Waste Collection and Transportation", font=("Calibri", 18, "bold"))
        manage_label.grid(row=0, column=0, pady=10, columnspan=2, sticky="w")

        # Separator Line below Manage Label
        separator = ttk.Separator(self.scrollable_frame, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=5, sticky='ew', pady=(0, 10))

        # Section 2: Retrieve City, Frequency, and Area
        create_data_frame = ttk.Frame(self.scrollable_frame)
        create_data_frame.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        create_label = ttk.Label(create_data_frame, text="Create Protocol", font=("Calibri", 12, "bold"))
        create_label.grid(row=0, column=0, columnspan=5, pady=10, padx=(0, 10), sticky="w")

        # City/Town/Barangay Name
        city_label = ttk.Label(create_data_frame, text="City/Town/Barangay Name:")
        city_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.city_entry = ttk.Entry(create_data_frame, width=30)
        self.city_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Area (sq m)
        area_label = ttk.Label(create_data_frame, text="Area (sq m):")
        area_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.area_entry = ttk.Entry(create_data_frame, width=30)
        self.area_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Frequency
        frequency_label = ttk.Label(create_data_frame, text="Frequency:")
        frequency_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.frequency_entry = ttk.Entry(create_data_frame, width=30)
        self.frequency_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Add space between the Method and Transportation listboxes
        tk.Label(create_data_frame, text=" ").grid(row=6, column=0)  # Adding an empty label for space

        # Define the width for the list boxes
        listbox_width = 30

        # Methods Listbox with Scrollbar
        method_label = ttk.Label(create_data_frame, text="Methods:")
        method_label.grid(row=7, column=0, sticky="w", padx=10, pady=(10, 0))

        self.method_listbox = tk.Listbox(create_data_frame, selectmode=tk.MULTIPLE, width=listbox_width)
        self.method_listbox.grid(row=7, column=1, padx=10, pady=(10, 0), sticky="w")

        # Define available methods
        available_methods = [
            "Curbside Pickup", "Container-based Collection", "Drop-off Centers",
            "Roll-off Containers", "Compactor Trucks", "Manual Sorting Stations",
            "Automated Sorting Systems", "Source Separation", "Specialized Collection",
            "Mobile Collection Units"
        ]

        for method in available_methods:
            self.method_listbox.insert(tk.END, method)

        method_scrollbar = tk.Scrollbar(create_data_frame, orient=tk.VERTICAL, command=self.method_listbox.yview)
        method_scrollbar.grid(row=7, column=2, pady=(10, 0), sticky="nse")

        self.method_listbox.config(yscrollcommand=method_scrollbar.set)

        # Add Button for Methods
        add_method_button = tk.Button(create_data_frame, text="Add Method", command=self.add_method, image=self.add_icon, bg="#000080", fg="white", relief="flat")
        add_method_button.grid(row=7, column=3, padx=5, pady=(10, 0), sticky="w")

        # Stored Methods Listbox with Scrollbar
        self.stored_methods_listbox = tk.Listbox(create_data_frame, selectmode=tk.MULTIPLE, width=listbox_width)
        self.stored_methods_listbox.grid(row=7, column=4, padx=5, pady=(10, 0), sticky="w")

        # Scrollbar for Stored Methods Listbox
        stored_methods_scrollbar = tk.Scrollbar(create_data_frame, orient=tk.VERTICAL, command=self.stored_methods_listbox.yview)
        stored_methods_scrollbar.grid(row=7, column=5, pady=(10, 0), sticky="nse")

        self.stored_methods_listbox.config(yscrollcommand=stored_methods_scrollbar.set)

        # Remove Button for Methods
        remove_method_button = tk.Button(create_data_frame, text="Remove Method", command=self.remove_method, image=self.remove_icon, bg="#000080", fg="white", relief="flat")
        remove_method_button.grid(row=7, column=6, padx=5, pady=(10, 0), sticky="w")

        # Add space between the Method and Transportation listboxes
        tk.Label(create_data_frame, text=" ").grid(row=8, column=0)  # Adding an empty label for space

        # Transportation Listbox with Scrollbar
        transportation_label = ttk.Label(create_data_frame, text="Transportation:")
        transportation_label.grid(row=9, column=0, sticky="w", padx=10, pady=5)

        self.transportation_listbox = tk.Listbox(create_data_frame, selectmode=tk.MULTIPLE, width=listbox_width)
        self.transportation_listbox.grid(row=9, column=1, padx=10, pady=5, sticky="w")

        # Define available transportation options
        available_transportation = [
            "Garbage Trucks", "Recycling Trucks", "Roll-off Trucks", "Front-Loaders",
            "Rear-Loaders", "Side-Loaders", "Transfer Trucks", "Rail Transport",
            "Barge or Ship Transport", "Pipeline Transport", "Cycling and Pedestrian Transport"
        ]

        for mode in available_transportation:
            self.transportation_listbox.insert(tk.END, mode)

        transportation_scrollbar = tk.Scrollbar(create_data_frame, orient=tk.VERTICAL, command=self.transportation_listbox.yview)
        transportation_scrollbar.grid(row=9, column=2, pady=5, sticky="nse")

        self.transportation_listbox.config(yscrollcommand=transportation_scrollbar.set)

        # Add Button for Transportation
        add_transportation_button = tk.Button(create_data_frame, text="Add Transportation", command=self.add_transportation, image=self.add_icon, bg="#000080", fg="white", relief="flat")
        add_transportation_button.grid(row=9, column=3, padx=5, pady=5, sticky="w")

        # Stored Transportation Listbox with Scrollbar
        self.stored_transportation_listbox = tk.Listbox(create_data_frame, selectmode=tk.MULTIPLE, width=listbox_width)
        self.stored_transportation_listbox.grid(row=9, column=4, padx=5, pady=5, sticky="w")

        # Scrollbar for Stored Transportation Listbox
        stored_transportation_scrollbar = tk.Scrollbar(create_data_frame, orient=tk.VERTICAL, command=self.stored_transportation_listbox.yview)
        stored_transportation_scrollbar.grid(row=9, column=5, pady=5, sticky="nse")

        self.stored_transportation_listbox.config(yscrollcommand=stored_transportation_scrollbar.set)

        # Remove Button for Transportation
        remove_transportation_button = tk.Button(create_data_frame, text="Remove Transportation", command=self.remove_transportation, image=self.remove_icon, bg="#000080", fg="white", relief="flat")
        remove_transportation_button.grid(row=9, column=6, padx=5, pady=5, sticky="w")

        # Save Button
        save_button = tk.Button(create_data_frame, text="Save", command=self.save_data, image=self.save_icon, bg="#000080", fg="white", relief="flat")
        save_button.grid(row=11, column=0, padx=5, pady=5, sticky="w")  # Adjusted row to 11

        # Section 3: Edit/View Waste Data
        table_view_frame = ttk.Frame(self.scrollable_frame)
        table_view_frame.grid(row=3, column=0, pady=10, padx=10, sticky="w")

        table_label = ttk.Label(table_view_frame, text="View Protocol Data", font=("Calibri", 12, "bold"))
        table_label.grid(row=0, column=0, columnspan=6, pady=10, padx=(0, 10), sticky="w")

        # Delete Button (moved to the right)
        self.delete_button = tk.Button(table_view_frame, text="Delete", image=self.delete_icon, command=self.delete_data, state=tk.DISABLED, bg="#000080", fg="white", relief="flat")
        self.delete_button.grid(row=0, column=6, pady=10, padx=(30, 5), sticky="w")  # Adjusted column to 7

        # Columns
        columns = ("City/Town/Barangay", "Area", "Frequency", "Method", "Transportation")
        self.table_view = ttk.Treeview(table_view_frame, columns=columns, show="headings", selectmode="browse")

        # Adjust the width of each column as needed
        column_widths = [150, 100, 80, 150, 150]
        for col, width in zip(columns, column_widths):
            self.table_view.column(col, width=width)

        for col in columns:
            self.table_view.heading(col, text=col)

        self.table_view.grid(row=1, column=0, pady=5, padx=5, columnspan=6, sticky="w")
        self.table_view.bind("<ButtonRelease-1>", self.on_treeview_select)

        # Vertical scrollbar for the Treeview
        table_view_scrollbar_y = ttk.Scrollbar(table_view_frame, orient="vertical", command=self.table_view.yview)
        table_view_scrollbar_y.grid(row=1, column=6, pady=5, sticky="nse")  
        self.table_view.configure(yscrollcommand=table_view_scrollbar_y.set)

        # Horizontal scrollbar for the Treeview
        table_view_scrollbar_x = ttk.Scrollbar(table_view_frame, orient="horizontal", command=self.table_view.xview)
        table_view_scrollbar_x.grid(row=2, column=0, pady=5, columnspan=6, sticky="ew")
        self.table_view.configure(xscrollcommand=table_view_scrollbar_x.set)

    def add_method(self):
        """
        Adds selected methods to the stored methods listbox.
        """
        selected_methods = self.method_listbox.curselection()
        available_methods = [self.method_listbox.get(idx) for idx in selected_methods]

        # Add selected methods to the stored methods listbox
        for method in available_methods:
            self.stored_methods_listbox.insert(tk.END, method)

        # Clear the selection in the methods listbox
        self.method_listbox.selection_clear(0, tk.END)

    def remove_method(self):
        """
        Removes selected stored methods from the listbox.
        """
        selected_stored_methods = self.stored_methods_listbox.curselection()

        # Remove selected stored methods
        for idx in reversed(selected_stored_methods):
            self.stored_methods_listbox.delete(idx)
        
    def add_transportation(self):
        """
        Adds selected transportation modes to the stored transportation listbox.
        """
        selected_transportation = self.transportation_listbox.curselection()
        available_transportation = [self.transportation_listbox.get(idx) for idx in selected_transportation]

        # Add selected transportation to the stored transportation listbox
        for mode in available_transportation:
            self.stored_transportation_listbox.insert(tk.END, mode)

        # Clear the selection in the transportation listbox
        self.transportation_listbox.selection_clear(0, tk.END)

    def remove_transportation(self):
        """
        Removes selected stored transportation modes from the listbox.
        """
        selected_stored_transportation = self.stored_transportation_listbox.curselection()

        # Remove selected stored transportation
        for idx in reversed(selected_stored_transportation):
            self.stored_transportation_listbox.delete(idx)

    def save_data(self):
        """
        Saves user input data to a JSON file.
        """
        try:
            # Get values from entry fields and listboxes
            city = self.city_entry.get().strip()
            area = self.area_entry.get().strip()
            frequency = self.frequency_entry.get().strip()
            selected_methods = self.stored_methods_listbox.get(0, tk.END)
            selected_transportation = self.stored_transportation_listbox.get(0, tk.END)

            # Check if any of the required fields are empty
            if not city or not area or not frequency or not selected_methods or not selected_transportation:
                # Display an error message
                error_message = "Please fill in all required fields."
                messagebox.showerror(error_message)
                return

            # Optional: You can perform additional validation if needed

            # Generate a random ID (you may need to implement your own logic)
            random_id = self.generate_random_id()

            # Create a data dictionary with the collected information
            data = {
                "ID": random_id,
                "City": city,
                "Area": area,
                "Frequency": frequency,
                "Methods": selected_methods,
                "Transportation": selected_transportation,
            }

            # Determine the path to the "src" folder
            src_folder_path = os.path.join("src", "data")

            # Save data to a JSON file ("c_t_data.json") inside the "src" folder
            save_path = os.path.join(src_folder_path, "c_t_data.json")

            success = self.save_to_json(data, save_path)

            # Simulate an error condition
            if not success:
                raise ValueError("Simulated error: Failed to save data.")

            # Provide feedback through a message box
            if success:
                # Clear fields after successful save
                self.city_entry.delete(0, tk.END)
                self.area_entry.delete(0, tk.END)
                self.frequency_entry.delete(0, tk.END)
                self.stored_methods_listbox.delete(0, tk.END)
                self.stored_transportation_listbox.delete(0, tk.END)

                self.refresh_table()
                messagebox.showinfo("Success", "Data saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save data. Please try again.")
        except Exception as e:
            print(f"Exception: {e}")

    def save_to_json(self, data, file_path):
        """
        Saves data to a JSON file.

        Args:
        - data: Data to be saved.
        - file_path: Path to the JSON file.
        """
        try:
            import json

            # Read existing data from the file, if any
            existing_data = []
            if os.path.exists(file_path):
                with open(file_path, "r") as json_file:
                    existing_data = json.load(json_file)

            # Ensure that existing_data is a list
            if not isinstance(existing_data, list):
                existing_data = [existing_data]

            # Ensure that data is a list of dictionaries
            if not isinstance(data, list):
                data = [data]

            # Append the new data to the existing data
            existing_data.extend(data)

            # Write the updated data back to the file
            with open(file_path, "w") as json_file:
                json.dump(existing_data, json_file, indent=4)

            return True
        except Exception as e:
            print(f"Error in save_to_json: {e}")
            return False


    def load_from_json(self):
        """
        Loads data from a JSON file and populates the Treeview.
        """
        try:
            # Determine the path to the "src" folder
            src_folder_path = os.path.join("src", "data")

            # Load data from the "c_t_data.json" file inside the "src" folder
            load_path = os.path.join(src_folder_path, "c_t_data.json")

            if os.path.exists(load_path):
                with open(load_path, "r") as json_file:
                    data = json.loads(json_file.read())

                # Clear existing data in the Treeview
                self.clear_treeview()

                if isinstance(data, list):
                    # Populate the Treeview with loaded data (list of dictionaries)
                    for item in data:
                        self.table_view.insert("", "end", values=(item.get("ID", ""), item.get("City", ""), item.get("Area", ""), item.get("Frequency", ""), ", ".join(item.get("Methods", [])), ", ".join(item.get("Transportation", []))))
                elif isinstance(data, dict):
                    # Populate the Treeview with loaded data (single dictionary)
                    self.table_view.insert("", "end", values=(data.get("ID", ""), data.get("City", ""), data.get("Area", ""), data.get("Frequency", ""), ", ".join(data.get("Methods", [])), ", ".join(data.get("Transportation", []))))
                else:
                    return

            else:
                return

        except Exception as e:
            print(e)

    def refresh_table(self):
        """
        Clears and reloads data into the Treeview.
        """
        # Clear existing data in the Treeview
        self.clear_treeview()

        # Load and display updated data from the JSON file
        self.load_from_json()

    def clear_treeview(self):
        """
        Clears data from the Treeview.
        """
        # Implement logic to clear existing data in the Treeview
        for item in self.table_view.get_children():
            self.table_view.delete(item)

    def on_treeview_select(self, event):
        """
        Enables delete button when a row is selected.

        Args:
        - event: Event triggering the method.
        """
        # Enable buttons when a row is selected
        selected_item = self.table_view.selection()

        if selected_item:
            self.delete_button.config(state=tk.NORMAL)
        else:
            # Disable buttons if no row is selected
            self.delete_button.config(state=tk.DISABLED)

    def generate_random_id(self):
        """
        Generates a random ID for data entries.

        Returns:
        - str: Randomly generated ID.
        """
        return str(random.randint(1000, 9999))

    def delete_data(self):
        """
        Handles deletion of data from the Treeview and JSON file.
        """
        # Your delete data logic goes here
        selected_item = self.table_view.selection()

        if selected_item:
            # Ask for confirmation before deletion
            confirmation = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this entry?")

            if confirmation:
                # Get the ID of the selected item
                selected_id = self.table_view.item(selected_item, 'values')[0]

                # Delete the selected item from the Treeview
                self.table_view.delete(selected_item)

                # Delete the selected item from the JSON file
                self.delete_from_json(selected_id)

                # Clear entry fields
                self.city_entry.delete(0, tk.END)
                self.area_entry.delete(0, tk.END)  # Assuming Area is in the second column
                self.frequency_entry.delete(0, tk.END)  # Assuming Frequency is in the third column
                self.stored_methods_listbox.delete(0, tk.END)
                self.stored_transportation_listbox.delete(0, tk.END)

                # Disable buttons after deletion
                self.delete_button.config(state=tk.DISABLED)


    def delete_from_json(self, selected_id):
        """
        Deletes selected data entry from the JSON file.

        Args:
        - selected_id: ID of the selected data entry.
        """
        try:
            # Determine the path to the "src" folder
            src_folder_path = os.path.join("src", "data")

            # Load existing data from the JSON file
            load_path = os.path.join(src_folder_path, "c_t_data.json")

            if os.path.exists(load_path):
                with open(load_path, "r") as json_file:
                    data = json.load(json_file)

                # Remove the entry with the selected ID
                data = [entry for entry in data if entry["ID"] != selected_id]

                # Save the updated data back to the JSON file
                with open(load_path, "w") as json_file:
                    json.dump(data, json_file, indent=4)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete entry. {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('800x600')

    waste_cat_frame = WasteCATFrame(root)
    root.mainloop()
