import glob
import pandas as pd
import subprocess

def run_r_script(data1, data2, output_path):
    # Save the processed data to CSV files
    data1_path = '/tmp/processed_data1.csv'
    data2_path = '/tmp/processed_data2.csv'
    
    # Call the R script
    subprocess.run(["Rscript", "scripts/data_vis.R", data1_path, data2_path, output_path])
