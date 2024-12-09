import os
from nilearn import plotting
from jinja2 import Template
from nilearn.image import load_img
import base64
from io import BytesIO
from nilearn.glm import threshold_stats_img
from pretty_html_table import build_table


def to_reporter(selected_atlas,cluster_tables_unc,cluster_tables_corr,selected_files,threshold):
    """
    Generates HTML reports for clusters identified in the provided statistical maps, 
    showing statistical maps, with given thresholds.

    Parameters:
    -----------
    cluster_tables : list of pandas.DataFrame
        DataFrames containing information about clusters.
    
    imgs : list of NIfTI images
        List of NIfTI images.

    Function Workflow:
    ------------------
    Generates HTML files with ortho slice images showing cluster results with the given threshold.
    The resulting HTML is saved in the image directory.
    """
    
    # Template for generating HTML content
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cluster report</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333;
                text-align: center;
            }
            h1 {
                margin-top: 20px;
            }
            .cluster {
                margin-bottom: 40px;
                padding: 20px;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                display: inline-block;
                text-align: center;
                width: 80%;
            }
            .image-container {
                display: flex;
                justify-content: space-around;
                align-items: center;
            }
            img {
                max-width: 80%;
                height: auto;
                margin: 10px;
                border-radius: 8px;
            }
            .image-label {
                text-align: center;
                font-weight: bold;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Cluster report</h1>
        {% for cluster in clusters %}
            <div class="cluster">
                <h2>Anatomical region: {{ cluster.region }}</h2>
                <ul style="list-style-type:none; padding:0;">
                    <li><strong>MNI coordinates:</strong> x={{ cluster.x }}, y={{ cluster.y }}, z={{ cluster.z }}</li>
                    <li><strong>Peak Stat:</strong> {{ cluster.peak_stat }}</li>
                    <li><strong>Cluster Size (mm&sup3;):</strong> {{ cluster.size_mm3 }}</li>
                </ul>
                <div class="image-container">
                    <div>
                        <p class="image-label">Thresholded image</p>
                        <img src="data:image/png;base64,{{ cluster.thresholded_image }}" alt="Ortho slice">
                    </div>
                </div>
            </div>
        {% endfor %}
    </body>
    </html>
    """


    # Prepare the clusters data for rendering in HTML
    for idx, table in enumerate(cluster_tables_unc):   
        
        clusters_data = []

        # Get path and file name
        folder_path = os.path.dirname(selected_files[idx])
        base_name = os.path.splitext(os.path.splitext(os.path.basename(selected_files[idx]))[0])[0]

        img = load_img(selected_files[idx])

        #uncorrected_img, _ = threshold_stats_img(img,alpha=threshold,height_control=None,cluster_threshold=0,two_sided=True)
        #corrected_img, corr_threshold = threshold_stats_img(img,alpha=0.05,height_control='fdr',cluster_threshold=0,two_sided=True)

        for index, row in table.iterrows():
            cluster_id = row['Cluster ID']
            x, y, z = row['X'], row['Y'], row['Z']
            peak_stat = row['Peak Stat']
            size_mm3 = row['Cluster Size (mm3)']
            region = row['Region']

            # Generate ortho slice image and convert it to base64
            img_buffer_uncorrected = BytesIO()
            display_uncorrected = plotting.plot_stat_map(img, threshold=threshold,
                                                         display_mode='ortho', cut_coords=(x, y, z), draw_cross=True, black_bg=True)
            display_uncorrected.savefig(img_buffer_uncorrected)
            display_uncorrected.close()
            img_buffer_uncorrected.seek(0)
            img_base64_uncorrected = base64.b64encode(img_buffer_uncorrected.read()).decode('utf-8')
            img_buffer_uncorrected.close()

            # # Generate FDR-corrected ortho slice image and convert it to base64
            # img_buffer_corrected = BytesIO()
            # display_corrected = plotting.plot_stat_map(corrected_img, threshold=corr_threshold,
            #                                            display_mode='ortho', cut_coords=(x, y, z), draw_cross=False, black_bg=True)
            # display_corrected.savefig(img_buffer_corrected)
            # display_corrected.close()
            # img_buffer_corrected.seek(0)
            # img_base64_corrected = base64.b64encode(img_buffer_corrected.read()).decode('utf-8')
            # img_buffer_corrected.close()

            # Append cluster data for the HTML report
            clusters_data.append({
                'id': cluster_id,
                'x': x,
                'y': y,
                'z': z,
                'peak_stat': peak_stat,
                'size_mm3': size_mm3,
                'region': region,
                'thresholded_image': img_base64_uncorrected,
                #'corrected_image': img_base64_corrected
            })

        # Sort clusters by size (mm³) in descending order
        clusters_data.sort(key=lambda x: x['size_mm3'], reverse=True)
        table = table.sort_values(by='Cluster Size (mm3)', ascending=False)

        # Generate HTML report
        html_report = Template(html_template).render(clusters=clusters_data)

        # Write a HTML report to a file
        output_dir = os.path.join(folder_path,f'reports_atlas-{selected_atlas}')
        os.makedirs(output_dir, exist_ok=True)
        report_filename = os.path.join(output_dir, f"cluster_report_{base_name}.html")
        with open(report_filename, "w") as f:
            f.write(html_report)

        # Write the cluster tables to HTML files
        html_table_ = build_table(table, 'blue_light')
        table_filename = os.path.join(output_dir, f"cluster_table_unc_{base_name}.html")
        with open(table_filename, 'w') as f:
            f.write(html_table_)

        # Add corrected region table
        # corr_table = cluster_tables_corr[idx]
        # corr_table = corr_table.sort_values(by='Cluster Size (mm3)', ascending=False)
        # html_table_ = build_table(corr_table, 'blue_light')
        # table_filename = os.path.join(output_dir, f"cluster_table_corr_{base_name}.html")
        # with open(table_filename, 'w') as f:
        #     f.write(html_table_)

        print(f"Cluster report generated: {report_filename}.html")











