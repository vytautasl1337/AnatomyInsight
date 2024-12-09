"""
Function to load atlases   
"""

from nilearn.image import load_img
import pandas as pd

def load_atlas(atlas_name):
    """
    Load the specified atlas.

    Args:
        atlas_name (str): The name of the atlas to load.
        
    Returns:
        dict: A dictionary containing 'maps' (nifti image) and 'labels' (list of region names).
    """
    atlas_data={}
    if atlas_name == "DiFuMo":
        # Load DiFuMo map
        atlas_data['map'] = load_img('atlases/difumo_atlases/512/2mm/maps.nii.gz')
        
        # Load the DiFuMo labels
        labels_df = pd.read_csv('atlases/difumo_atlases/512/labels_512_dictionary.csv')
        atlas_data['labels'] = labels_df['Difumo_names'].tolist()
        
    elif atlas_name == "Juelich":

        # Load Juelich map
        atlas_data['map'] = load_img('atlases/Juelich/Juelich-prob-1mm.nii.gz') 
        atlas_data['map'].shape
        # Load Juelich labels
        import xml.etree.ElementTree as ET
        tree = ET.parse('atlases/Juelich/Juelich.xml')
        root = tree.getroot()

        index,x,y,z,brain_region = [[] for x in range(5)]

        for label in root.findall(".//label"):
            idx = int(label.attrib['index']) + 1
            x_ = label.attrib['x']
            y_ = label.attrib['y']
            z_ = label.attrib['z']
            brain_region_ = label.text.strip()
    
            index.append(idx)
            x.append(x_)
            y.append(y_)
            z.append(z_)
            brain_region.append(brain_region_)

        labels_df = pd.DataFrame({
            'index': index,
            'x': x,
            'y': y,
            'z': z,
            'brain_region': brain_region
        })

        atlas_data['labels'] = labels_df['brain_region'].tolist()

    elif atlas_name == 'AAL3':

        # Load AAL3 map
        atlas_data['map'] = load_img('atlases/AAL3/ROI_MNI_V7.nii')
        atlas_data['map'].shape
        # Load AAL3 labels
        labels_df = pd.read_csv('atlases/AAL3/AAL3v1_1mm.nii.txt', 
                                sep='\s+',
                                header=None, 
                                names=['Index', 'Region', 'Value'])
        
        atlas_data['labels'] = labels_df['Region'].tolist()

    
    return atlas_data







