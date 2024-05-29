import glob
import pandas as pd
import subprocess
from pkg_resources import resource_filename

def run_r_script(group_1_R, group_2_R, output, p_value, fod, filter, name, deseq2, R_path):
    # Call the R script
    subprocess.run(["Rscript", R_path, group_1_R, group_2_R, output, p_value, fod, filter, name, deseq2])
