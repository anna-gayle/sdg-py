import tkinter as tk
import json
from tkinter import PhotoImage, filedialog
from src.manage_waste import ManageWasteDataFrame
from src.waste_c_t import WasteCATFrame
from src.facility_waste import WasteFacilityFrame

class WasteManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('800x600')
        self.root.title('Waste Management System')
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        create_menu_bar(root, self)

        # Define frames
        self.frames = {
            'Manage Waste Data': ManageWasteDataFrame(root),
            'Waste C&T': WasteCATFrame(root),
            'Waste Facilities': WasteFacilityFrame(root),
        }

        # Set the default frame
        self.current_frame = self.frames['Manage Waste Data']
        self.current_frame.pack(expand=True, fill="both")

    def generate_report(self):
        # Open a file dialog for selecting a JSON file
        json_file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])

        # Check if a file was selected
        if json_file_path:
            # Read the JSON data from the selected file
            try:
                with open(json_file_path, 'r') as json_file:
                    json_data = json.load(json_file)
            except Exception as e:
                print(f"Error reading JSON file: {str(e)}")
                return

            # Open a file dialog for saving the text file
            txt_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

            # Check if a file was selected for saving
            if txt_file_path:
                # Save the JSON data as a text file
                try:
                    with open(txt_file_path, 'w') as txt_file:
                        json.dump(json_data, txt_file, indent=4)
                    print(f"JSON data converted and saved to {txt_file_path} successfully.")
                except Exception as e:
                    print(f"Error saving text file: {str(e)}")

def create_menu_bar(root, app):
    def toggle_menu():
        def collapse_toggle_menu():
            toggle_menu_fm.destroy()
            toggle_btn.config(image=open_icon, command=toggle_menu)

        toggle_menu_fm = tk.Frame(root, bg='#000080')

        def create_button(frame, text, y_position, icon_path, frame_name):
            btn_icon = PhotoImage(file=icon_path)
            btn = tk.Button(frame, text=text, compound=tk.LEFT,
                            image=btn_icon, font=('Calibri', 12), bd=0,
                            bg='#000080', fg='white', anchor="w",
                            padx=10, pady=10,
                            activebackground='#000080', activeforeground='white',
                            command=lambda fn=frame_name: switch_frame(fn))
            btn.image = btn_icon
            btn.place(x=20, y=y_position)

            if text == 'Generate Reports':
                btn.config(command=app.generate_report)

        def switch_frame(frame_name):
            app.current_frame.pack_forget()
            app.current_frame = app.frames[frame_name]
            app.current_frame.pack(expand=True, fill="both")

        create_button(toggle_menu_fm, 'Manage Waste Data', 20, 'assets/icons/folder-icon.png', 'Manage Waste Data')
        create_button(toggle_menu_fm, 'Waste C&T', 80, 'assets/icons/waste-icon.png', 'Waste C&T')
        create_button(toggle_menu_fm, 'Waste Facilities', 140, 'assets/icons/facilities-icon.png', 'Waste Facilities')
        create_button(toggle_menu_fm, 'Generate Reports', 200, 'assets/icons/report-icon.png', 'Waste Reports')

        window_height = root.winfo_height()
        toggle_menu_fm.place(x=0, y=50, height=window_height, width=270)
        toggle_btn.config(image=close_icon, command=collapse_toggle_menu)

    open_icon = PhotoImage(file='assets/icons/menu-icon.png')
    close_icon = PhotoImage(file='assets/icons/close-icon.png')

    head_frame = tk.Frame(root, bg='#000080', highlightbackground='white', highlightthickness=1)

    toggle_btn = tk.Button(head_frame, image=open_icon, bd=0, bg='#000080', command=toggle_menu)
    toggle_btn.place(x=10, y=10)

    title_icon = PhotoImage(file='assets/icons/title-icon.png')

    title_lb = tk.Label(head_frame, text='Waste Management System', bg='#000080',
                        fg='white', font=('Bold', 15), compound=tk.LEFT, image=title_icon, padx=10)
    title_lb.image = title_icon
    title_lb.place(relx=0.05, rely=0.5, anchor=tk.W)

    head_frame.pack(side=tk.TOP, fill=tk.X)
    head_frame.pack_propagate(False)
    head_frame.configure(height=50)

if __name__ == "__main__":
    root = tk.Tk()
    app = WasteManagementApp(root)
    root.mainloop()
