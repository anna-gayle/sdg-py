
# sdg-py Code Documentation

## Project Overview

The `sdg-py` project is a Waste Management System built with Python and Tkinter. It serves as an academic project to demonstrate basic functionalities related to waste management.

The Waste Facility Management Application, developed in Python using Tkinter, offers an interface for creating, viewing, and deleting waste facility data. The application features a scrollable canvas, dynamic treeviews, and image icons for actions such as adding, removing, saving, and deleting facility data. Users can input essential information, including facility name, area, operating hours, address, facility type, and waste disposal methods. The data is stored in JSON format, providing portability and structure. The application's functionality encompasses new facility creation, and facility deletion. The code structure revolves around the WasteFacilityFrame class, with methods handling data input, saving/loading from JSON, and table updates. Dependencies include Python 3.x, Tkinter and Pillow. To run the application, execute the provided Python script.

## File Structure

- `main.py`: Main application file.
- `app.py`: Application structure and layout.
- `manage_waste.py`: Manages waste profile
- `facility_waste.py`: Manages facility and disposal data.
- `waste_c_t.py`: Manages collection and transportation protocols.

## How to Run the Application

Ensure that Python is installed on your system.

1. Clone the repository: `git clone https://github.com/anna-gayle/sdg-py.git`
2. Navigate to the project directory: `cd sdg-py`
3. Run the application: `python main.py`

## Code Explanation

### `main.py`

In `main.py`, the entry point for the Waste Management System application, the Tkinter library is imported for graphical user interface (GUI) creation. The script creates the main Tkinter window and instantiates the `WasteManagementApp` class from the `app` module, passing the window as an argument. The application's main event loop is initiated, ensuring responsiveness to user interactions and facilitating the seamless execution of the waste management functionalities encapsulated within the `WasteManagementApp` class.

### `app.py`

The `app.py` module defines the `WasteManagementApp` class, which serves as the core of the Waste Management System application. The class is responsible for initializing the main Tkinter window, setting its properties, and creating a menu bar with navigation buttons. It manages different frames for managing waste data, waste collection and transportation, and waste facilities. The class also includes functionality to generate reports by opening a file dialog for selecting a JSON file, converting the data, and saving it as a text file. The file also contains the `create_menu_bar` function for building the application's menu bar with toggleable buttons for different functionalities. The main block instantiates the `WasteManagementApp` class, creating an instance of the application, and starts the Tkinter main loop for user interaction.

### `manage_waste.py`

The `ManageWasteDataFrame` class, defined in the `manage_waste.py` module, extends the Tkinter `Frame` class to create a scrollable frame for managing waste data within the Waste Management System application. The frame incorporates various widgets for input, display, and manipulation of waste-related information. It utilizes the `Treeview` widget for presenting waste data in a tabular format. The class includes functions for adding, removing, and saving waste data, as well as methods for refreshing the displayed data, handling row selection, and deleting entries. The module also provides an entry point for testing the frame within a Tkinter window when executed independently.

### `facility_waste.py`

The `WasteFacilityFrame` class, located in the `facility_waste.py` module, extends Tkinter's `Frame` class to construct a scrollable frame dedicated to managing waste facility data. The frame encompasses a variety of widgets for data input, presentation, and manipulation, including labels, entry fields, comboboxes, listboxes, buttons, and a treeview. Utilizing the `Treeview` widget, the class organizes facility data in tabular form. Key functionalities include adding, removing, and saving facility data, along with methods for refreshing the displayed information, managing row selection, and deleting entries. The module serves as a standalone executable, creating an instance of the `WasteFacilityFrame` class within a Tkinter window, providing a user interface for waste facility management operations.

### `waste_c_t.py`

The `WasteCATFrame` class, located in the `waste_c_t.py` module, defines a Tkinter frame for managing waste collection and transportation protocols within the Waste Collection and Transportation System application. The frame includes a scrollable canvas with various widgets, such as labels, separators, entry fields, listboxes, buttons, and a treeview for tabular data display. Functionality encompasses creating, viewing, and deleting waste collection and transportation protocols. Users can input data such as city/town/barangay name, area, frequency, waste collection methods, and transportation modes. Icons are incorporated for actions like adding, removing, saving, and deleting data. The class handles dynamic resizing, data validation, and persistence through JSON files. The module also provides an entry point for testing the frame within a Tkinter window when executed independently.

### `waste_data.json`, `facility_data.json`, and `c_t_data.json`

.json files that stores data.

> Feel free to open source code to view comments.

## Dependencies

- Python 3.x
- Tkinter (usually included with Python, used for UI)
- Pillow (used for Icons)

## Contributing

If you wish to contribute to the project, follow these guidelines:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`
3. Make your changes and commit them: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request.

## Troubleshooting

- The delete function works for at least one frame, though in some cases, you may have to manually remove the data from the json file.
- Weird screen tearing, but not severe.

## Contact Information

For questions or support, you can reach out at: 
https://github.com/anna-gayle


