import glob
import pandas as pd
import subprocess
from pkg_resources import resource_filename

def run_r_script(data1, data2, output_path):
    # Save the processed data to CSV files
    data1_path = '/tmp/processed_data1.csv'
    data2_path = '/tmp/processed_data2.csv'
    
    # Call the R script
    r_script_path = resource_filename(__name__, '../scripts/data_vis.R')
    subprocess.run(["Rscript", r_script_path, data1_path, data2_path, output_path])
