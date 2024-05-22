import glob
import pandas as pd
import subprocess
from pkg_resources import resource_filename

def run_r_script(data1, data2, output_path, R_path):
    # Call the R script
    subprocess.run(["Rscript", R_path, data1, data2, output_path])
