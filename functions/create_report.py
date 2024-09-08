import os
from nilearn import plotting
from jinja2 import Template
from nilearn.image import load_img
import base64
from io import BytesIO

def to_reporter(cluster_tables):
    
    """
    Generates HTML reports for clusters identified in the provided statistical maps.

    The function takes in a list of cluster tables (pandas DataFrames) and creates 
    an HTML report for each table. Each report includes:
        - Cluster coordinates, peak statistic, size, and brain region.
        - Ortho slice images showing the corresponding brain activity, based on NIfTI files.

    Parameters:
    -----------
    cluster_tables : list of pandas.DataFrame
        Each DataFrame represents clusters from a neuroimaging study with the following columns:
        - 'Cluster ID': Unique identifier for each cluster.
        - 'X', 'Y', 'Z': MNI coordinates of the cluster peak.
        - 'Peak Stat': Peak statistical value of the cluster.
        - 'Cluster Size (mm3)': Volume of the cluster in cubic millimeters.
        - 'Region': Anatomical region associated with the cluster.

    Function Workflow:
    ------------------
    1. **HTML Template**:
        The function uses a Jinja2 template to generate a nicely formatted HTML report. Each cluster's 
        information (ID, coordinates, peak statistic, size, and region) is presented in a well-structured
        HTML layout. Ortho slice images are embedded in base64 format for display.

    2. **Output Directory**:
        The function ensures that the directory `test_data/cluster_reports` exists, creating it if necessary.
        The generated reports are stored in this directory.

    3. **Loading NIfTI Files**:
        The function loads the NIfTI image corresponding to each cluster table. This image is used to 
        generate orthogonal brain slices centered at the MNI coordinates of each cluster.

    4. **Image Generation**:
        For each cluster, the function generates an ortho slice using `nilearn.plotting.plot_stat_map` 
        with the cluster's coordinates (x, y, z). The resulting image is saved as a base64-encoded string 
        for embedding in the HTML report.

    5. **Cluster Sorting**:
        Clusters are sorted by size (in mm³) in descending order before rendering them into the HTML report.

    6. **Saving HTML Reports**:
        The generated HTML report for each cluster table is saved to a file named `cluster_report_N.html` 
        (where N is the index of the table) in the output directory.

    Output:
        HTML file(s): Clusters and anatomical regions for each image. Results are outputed to the directory of the inputs.

    """
    
    
    # Template for generating HTML content
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cluster Report</title>
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
            img {
                max-width: 100%;
                height: auto;
                margin-top: 20px;
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <h1>Cluster Report</h1>
        {% for cluster in clusters %}
            <div class="cluster">
                <h2>Cluster ID: {{ cluster.id }}</h2>
                <ul style="list-style-type:none; padding:0;">
                    <li><strong>Coordinates:</strong> ({{ cluster.x }}, {{ cluster.y }}, {{ cluster.z }})</li>
                    <li><strong>Peak Stat:</strong> {{ cluster.peak_stat }}</li>
                    <li><strong>Cluster Size (mm³):</strong> {{ cluster.size_mm3 }}</li>
                    <li><strong>Region:</strong> {{ cluster.region }}</li>
                </ul>
                <img src="data:image/png;base64,{{ cluster.image }}" alt="Ortho slice">
            </div>
        {% endfor %}
    </body>
    </html>
    """

    # Prepare the clusters data for rendering in HTML
    output_dir = "test_data/cluster_reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for idx, table in enumerate(cluster_tables):   
        
        clusters_data = []
        img = load_img(nifti_files[idx])

        for index, row in table.iterrows():
            cluster_id = row['Cluster ID']
            x, y, z = row['X'], row['Y'], row['Z']
            peak_stat = row['Peak Stat']
            size_mm3 = row['Cluster Size (mm3)']
            region = row['Region']

            # Generate ortho slice image and convert it to base64
            img_buffer = BytesIO()
            display = plotting.plot_stat_map(img, threshold=3,
                                            display_mode='ortho', cut_coords=(x, y, z), draw_cross=True, black_bg=True)
            display.savefig(img_buffer)
            display.close()
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
            img_buffer.close()

            # Append cluster data for the HTML report
            clusters_data.append({
                'id': cluster_id,
                'x': x,
                'y': y,
                'z': z,
                'peak_stat': peak_stat,
                'size_mm3': size_mm3,
                'region': region,
                'image': img_base64
            })

        # Sort clusters by size (mm³) in descending order
        clusters_data.sort(key=lambda x: x['size_mm3'], reverse=True)

        # Generate HTML report
        html_report = Template(html_template).render(clusters=clusters_data)

        # Write the HTML report to a file
        report_filename = os.path.join(output_dir, f"cluster_report_{idx+1}.html")
        with open(report_filename, "w") as f:
            f.write(html_report)

        print(f"Cluster report generated: {report_filename}")