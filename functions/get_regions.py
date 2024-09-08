import numpy as np
from nilearn.image import coord_transform

def get_anatomical_regions(cluster_tables, atlas_data):
    """
    Match clusters to the nearest region in the DiFUMO atlas.

    Args:
        cluster_table (pd.DataFrame): Table containing cluster information with MNI coordinates.
        atlas_img (Nifti1Image): The 4D atlas image.
        labels (dict): Dictionary of atlas region labels.
        
    Returns:
        pd.DataFrame: Cluster table with an additional column for the closest region label.
    """
    atlas_data_ = atlas_data['maps'].get_fdata()
    atlas_affine = atlas_data['maps'].affine
    region_labels = atlas_data['labels']

    for table in cluster_tables:
        # Add a new column to store the region labels
        table['Region'] = None

        for index, row in table.iterrows():
            x, y, z = row['X'], row['Y'], row['Z']
            
            try:
                # Convert MNI coordinates to voxel indices in the atlas space
                voxel_coords = np.round(coord_transform(x, y, z, np.linalg.inv(atlas_affine))).astype(int)
                
                # Clip the voxel coordinates to ensure they are within the atlas dimensions
                voxel_coords = np.clip(voxel_coords, 0, np.array(atlas_data_[:, :, :, 0].shape) - 1)
                
                # Get the atlas label at the given voxel coordinate
                atlas_index = int(atlas_data_[voxel_coords[0], voxel_coords[1], voxel_coords[2], :].argmax())
                region_label = region_labels[atlas_index]
                
                # Assign the region label to the current row in the table
                table.at[index, 'Region'] = region_label
            except:
                table.at[index, 'Region'] = 'Unknown region'

    return cluster_tables

