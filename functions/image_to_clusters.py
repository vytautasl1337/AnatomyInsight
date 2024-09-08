"""
Function to load a statistical image or images and get the cluster and anatomical information
"""

import nibabel as nib
from nilearn.image import load_img
from nilearn.reporting import get_clusters_table

def image_to_clusters(nifti_files):
    """
    Process NIfTI files to extract clusters and return the cluster table.
    
    Args:
        nifti_files (list of str): List of file paths to NIfTI images.
        
    Returns:
        List of pandas.DataFrame: Cluster tables for each image.
    """
    cluster_tables = []
    for file in nifti_files:
        # Load the image
        img = load_img(file)
        # Extract clusters and get a table of clusters
        clusters_table = get_clusters_table(img, stat_threshold=3, cluster_threshold=0, two_sided=True)
        cluster_tables.append(clusters_table)
    
    return cluster_tables





