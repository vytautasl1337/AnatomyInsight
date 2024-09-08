"""
Simple nilearn extension to analyze statistical map clusters and output anatomical regions    
"""


import tkinter as tk
from tkinter import filedialog, messagebox, StringVar, OptionMenu
import os
from functions.get_Atlas import load_atlas
from functions.get_regions import get_anatomical_regions
from functions.image_to_clusters import image_to_clusters
from functions.create_report import to_reporter


# Global variable to store the list of selected NIfTI file paths
selected_files = []
selected_atlas = None
atlases = ["DiFUMO", "Brainnetome"]

def select_nifti_files():
    global selected_files
    # Open a file dialog to select multiple NIfTI files
    file_paths = filedialog.askopenfilenames(
        title="Select NIfTI files",
        filetypes=[("NIfTI files", "*.nii *.nii.gz")]
    )
    # Update the global variable with the selected file paths
    if file_paths:
        selected_files = list(file_paths)
        # Clear the current contents of the Listbox
        listbox.delete(0, tk.END)
        # Insert each filename into the Listbox
        for file in selected_files:
            filename = os.path.basename(file)
            listbox.insert(tk.END, filename)
        # Adjust the height of the Listbox based on the number of selected files
        adjust_listbox_height()

def adjust_listbox_height():
    # Set the height of the Listbox to the number of files, with a minimum of 1 and a maximum of 20 rows visible
    max_height = 20  # Maximum number of rows visible in the Listbox
    min_height = 1   # Minimum height to start with
    num_files = len(selected_files)
    listbox_height = min(max_height, max(min_height, num_files))
    listbox.config(height=listbox_height)
    listbox.update_idletasks()  # Update the listbox to reflect size changes

def process_selected_files():
    if selected_files:
        # Load the selected atlas
        atlas_data = load_atlas(selected_atlas)
        
        # Get cluster tables from the selected files
        cluster_tables = image_to_clusters(selected_files)
        
        # Get anatomical regions for each cluster
        cluster_tables = get_anatomical_regions(cluster_tables, atlas_data)
        
        to_reporter(cluster_tables)
        

    else:
        print("No files were selected!")

def clear_selection():
    global selected_files
    # Get selected indices from the Listbox
    selected_indices = listbox.curselection()
    
    # Remove selected files from the `selected_files` list
    for index in reversed(selected_indices):  # Reverse to avoid index shifting issues
        selected_files.pop(index)
        listbox.delete(index)
    
    # Adjust the height after removing items
    adjust_listbox_height()
    
def update_atlas_selection(*args):
    global selected_atlas
    # Update the selected atlas and the text on the atlas button
    selected_atlas = atlas_var.get()
    atlas_button.config(text=f"Atlas to Use: {selected_atlas}")

# Set up the main application window
root = tk.Tk()
root.title("Clusters 2 MNI")

# Create a frame to hold the Listbox and Scrollbar
frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a Scrollbar and attach it to the frame
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a Listbox to display the selected file names
listbox = tk.Listbox(
    frame,
    selectmode=tk.MULTIPLE,  # Allows multiple selection in the Listbox
    width=80,
    height=1,  # Start with height that fits only one file
    yscrollcommand=scrollbar.set
)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Configure the scrollbar to work with the Listbox
scrollbar.config(command=listbox.yview)

# Create a Button to open the file dialog for selecting files
select_button = tk.Button(root, text="Select images", command=select_nifti_files)
select_button.pack(pady=5)

# Create a Button to process the selected files
process_button = tk.Button(root, text="Analyze images", command=process_selected_files)
process_button.pack(pady=5)

# Create a Button to clear the selected files
clear_button = tk.Button(root, text="Clear Selected Files", command=clear_selection)
clear_button.pack(pady=5)

# StringVar to hold the selected atlas name
atlas_var = StringVar(root)
atlas_var.set(atlases[0])  # Set the default atlas

# Initialize the selected_atlas with the default selection
selected_atlas = atlas_var.get()

# Create a Button that will change based on the selected atlas
atlas_button = tk.Button(root, text=f"Atlas to Use: {selected_atlas}", command=None)
atlas_button.pack(pady=5)

# Create an OptionMenu for selecting an atlas
atlas_menu = OptionMenu(root, atlas_var, *atlases, command=update_atlas_selection)
atlas_menu.pack(pady=5)

# Start the Tkinter event loop
root.mainloop()
