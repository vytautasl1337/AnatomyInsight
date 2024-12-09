"""
Simple nilearn extension to analyze statistical map clusters and output anatomical regions    
"""


import tkinter as tk
from tkinter import filedialog, StringVar, OptionMenu
import os
from functions.get_Atlas import load_atlas
from functions.get_regions import get_anatomical_regions
from functions.image_to_clusters import image_to_clusters
from functions.create_report import to_reporter

# Global variable to store the list of selected NIfTI file paths
selected_files = []
selected_atlas = None
atlases = ["DiFuMo", "Juelich", "AAL3"]


def select_nifti_files():
    global selected_files
    file_paths = filedialog.askopenfilenames(
        title="Select NIfTI files",
        filetypes=[("NIfTI files", "*.nii *.nii.gz")]
    )
    if file_paths:
        selected_files = list(file_paths)
        listbox.delete(0, tk.END)
        for file in selected_files:
            filename = os.path.basename(file)
            listbox.insert(tk.END, filename)
        adjust_listbox_height()

def adjust_listbox_height():
    max_height = 20
    min_height = 1
    num_files = len(selected_files)
    listbox_height = min(max_height, max(min_height, num_files))
    listbox.config(height=listbox_height)
    listbox.update_idletasks()

def process_selected_files():
    if selected_files:
        threshold = float(threshold_var.get())
        atlas_data = load_atlas(selected_atlas)
        cluster_tables_unc, cluster_tables_corr = image_to_clusters(selected_files,threshold)
        cluster_tables_unc, cluster_tables_corr = get_anatomical_regions(cluster_tables_unc, cluster_tables_corr, atlas_data)
        to_reporter(selected_atlas, cluster_tables_unc, cluster_tables_corr, selected_files, threshold)
    else:
        print("No files were selected!")

def clear_selection():
    global selected_files
    selected_indices = listbox.curselection()
    for index in reversed(selected_indices):
        selected_files.pop(index)
        listbox.delete(index)
    adjust_listbox_height()

def update_atlas_selection(*args):
    global selected_atlas
    selected_atlas = atlas_var.get()

# Set up the main application window
root = tk.Tk()
root.title("AnatomyInsight")

threshold_var = StringVar()
threshold_var.set("0.001") # default threshold value for the given image(s)

# Create a frame to hold the Listbox and Scrollbar
frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a Scrollbar and attach it to the frame
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a Listbox to display the selected file names
listbox = tk.Listbox(
    frame,
    selectmode=tk.MULTIPLE,
    width=80,
    height=1,
    yscrollcommand=scrollbar.set
)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Configure the scrollbar to work with the Listbox
scrollbar.config(command=listbox.yview)

# Create a horizontal frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(padx=10, pady=10)

# Create a Button to open the file dialog for selecting files
select_button = tk.Button(button_frame, text="Select images", command=select_nifti_files)
select_button.pack(side=tk.LEFT, padx=5)

# Create a Button to process the selected files
process_button = tk.Button(button_frame, text="Get reports", command=process_selected_files)
process_button.pack(side=tk.LEFT, padx=5)

# Create a Button to clear the selected files
clear_button = tk.Button(button_frame, text="Clear selected files", command=clear_selection)
clear_button.pack(side=tk.LEFT, padx=5)

# StringVar to hold the selected atlas name
atlas_var = StringVar(root)
atlas_var.set(atlases[0])  # Set the default atlas (DiFuMo)

# Initialize the selected_atlas with the default selection
selected_atlas = atlas_var.get()

# Create a label to display the selected atlas
atlas_label = tk.Label(root, text="Atlas selected:")
atlas_label.pack(pady=5)

# Create an OptionMenu for selecting an atlas
atlas_menu = OptionMenu(root, atlas_var, *atlases, command=update_atlas_selection)
atlas_menu.pack(pady=5)

# Add a label and entry for the desired threshold
threshold_label = tk.Label(root, text="Image threshold:")
threshold_label.pack(pady=5)

threshold_entry = tk.Entry(root, textvariable=threshold_var, width=10)
threshold_entry.pack(pady=5)

# Start the Tkinter event loop
root.mainloop()
