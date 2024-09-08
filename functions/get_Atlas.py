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
    if atlas_name == "DiFUMO":
        atlas_data['maps'] = load_img('atlases/difumo_atlases/512/2mm/maps.nii.gz')
        
        # Load the DiFUMO labels
        labels_df = pd.read_csv('atlases/difumo_atlases/512/labels_512_dictionary.csv')
        atlas_data['labels'] = labels_df['Difumo_names'].tolist()
        
    elif atlas_name == "Brainnetome":
        atlas = load_img('atlases/Brainnetome/BN_Atlas_246_1mm.nii.gz') 
    else:
        raise ValueError(f"Atlas {atlas_name} is not supported.")
    
    return atlas_data

