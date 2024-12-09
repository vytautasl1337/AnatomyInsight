# AnatomyInsight - README

## Overview

**AnatomyInsight** is a Python-based program designed for analyzing brain imaging data in the NIfTI format. It leverages multiple statistical analysis techniques to identify significant clusters in fMRI and related brain imaging data. The program uses a graphical user interface (GUI) to interact with the user and allows users to select NIfTI files, set analysis thresholds, and generate cluster reports and anatomical region visualizations. The output is provided in the form of a table and an HTML-based slice viewer for easy review and interpretation of the results.

---

## Features

- **NIfTI File Input**: Easily load NIfTI files for processing through a GUI file dialog.
- **Atlas Selection**: Choose from a list of predefined brain atlases (DiFuMo, Juelich, AAL3) to map clusters onto anatomical regions.
- **Threshold Adjustment**: Set a custom threshold for cluster analysis directly from the interface.
- **Cluster Analysis**: Calculate significant clusters and output tables and HTML visualizations with anatomical regions mapped onto them.
- **Report Generation**: Automatically generate detailed cluster reports and slice viewers in HTML format.
  
---


## Usage
Start the Program: Simply run the Python script to launch the GUI. The GUI allows you to:

Select NIfTI files (statistical maps, typically in .nii or .nii.gz formats).
Choose an atlas for anatomical region mapping.
Set the desired threshold for statistical significance.
Select NIfTI Files: Click the "Select images" button to open a file dialog. You can select multiple NIfTI files at once. The selected files will be listed in the interface.

Select Atlas: Choose one of the three available atlases (DiFuMo, Juelich, AAL3) from the dropdown menu. This determines the reference anatomical regions for cluster mapping. Note: DiFuMo is the primary atlas used, while AAL3 and Juelich are still under development.

Set Threshold: Enter the desired threshold for the analysis in the Image threshold field. This threshold controls the level of significance for clustering.

Process and Analyze: Once files and parameters are set, click "Get reports" to generate the reports. The output will consist of:

- **A table of significant clusters.**
- **An HTML report with anatomical region mappings and brain slice visualizations.**

Clear Selection: If you wish to clear the selected files, click "Clear selected files".

## Functionality breakdown
- **File selection:** Using tkinter.filedialog.askopenfilenames, the user selects the NIfTI files for analysis.
- **Atlas loading:** The program allows you to choose from the DiFuMo brain atlas, with AAL3 and Juelich atlases under development, which are loaded using load_atlas.
- **Cluster analysis:** The statistical clusters are identified using the image_to_clusters function, and anatomical regions are associated with each cluster via get_anatomical_regions.
- **Report generation:** A report is automatically generated using the to_reporter function, and it's saved in HTML format for easy viewing.

## License
This project is licensed under the MIT License - see the LICENSE file for details.