"""
Function to load a statistical image or images and get the cluster and anatomical information
"""

import nibabel as nib
from nilearn.image import load_img
from nilearn.reporting import get_clusters_table
from nilearn.glm import threshold_stats_img
import numpy as np
import pandas as pd

def image_to_clusters(selected_files, threshold):
    """
    Process NIfTI files to extract clusters and return the cluster table (note, no mask is applied on the data).
    
    Args:
        nifti_files (list of str): List of file paths to NIfTI images.
        
    Returns:
        List of pandas.DataFrame: Cluster tables for each image.
    """
    cluster_tables_unc,cluster_tables_corr = [],[]

    for file in selected_files:
        # Load the image
        img = load_img(file)
        # Extract clusters and get a table of clusters (0.001 unc by default, removed any corrections)
        #uncorrected_img, _ = threshold_stats_img(img,alpha=threshold,height_control=None,cluster_threshold=0,two_sided=True)
        #corrected_img, corr_threshold = threshold_stats_img(img,alpha=0.05,height_control='fdr',cluster_threshold=0,two_sided=True)
        thresholded_img,_ = threshold_stats_img(img,alpha=threshold,height_control=None,cluster_threshold=20,two_sided=True)
        clusters_table_unc = get_clusters_table(thresholded_img, stat_threshold=threshold, cluster_threshold=20, two_sided=True)
        #clusters_table_corr= get_clusters_table(corrected_img, stat_threshold=corr_threshold, two_sided=True)
        # Remove empty subclusters for clarity
        clusters_table_unc['Cluster Size (mm3)'] = clusters_table_unc['Cluster Size (mm3)'].replace('', np.nan)
        #clusters_table_corr['Cluster Size (mm3)'] = clusters_table_corr['Cluster Size (mm3)'].replace('', np.nan)

        clusters_table_unc['Cluster Size (mm3)'] = pd.to_numeric(clusters_table_unc['Cluster Size (mm3)'], errors='coerce')
        #clusters_table_corr['Cluster Size (mm3)'] = pd.to_numeric(clusters_table_corr['Cluster Size (mm3)'], errors='coerce')

        clusters_table_unc = clusters_table_unc.dropna(subset=['Cluster Size (mm3)'])
        #clusters_table_corr = clusters_table_corr.dropna(subset=['Cluster Size (mm3)'])

        cluster_tables_unc.append(clusters_table_unc)
        #cluster_tables_corr.append(clusters_table_corr)
    
    return cluster_tables_unc,cluster_tables_corr





