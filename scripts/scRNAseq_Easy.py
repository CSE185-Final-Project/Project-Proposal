import zipfile
import os
import subprocess
import argparse
import sys
import json
from pkg_resources import resource_filename
import packages.R_prep as dp

def unzip_files(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def print_manual():
    manual_path = resource_filename(__name__, '../docs/manual.txt')
    with open(manual_path, 'r') as f:
        manual_content = f.read()
    print(manual_content)

def main():
    parser = argparse.ArgumentParser(description="Process gene result files and generate visualizations.")
    parser.add_argument('group1_zip', type=str, nargs='?', help='Path to the first zip file.')
    parser.add_argument('group2_zip', type=str, nargs='?', help='Path to the second zip file.')
    parser.add_argument('-o', '--output', type=str, help='Path to save the output graph.')
    parser.add_argument('-v', '--visual', action='store_true', help='Run visualization if set to True.')
    
    # Parse the arguments
    args = parser.parse_args()
    
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1].lower() == 'help'):
        print_manual()
        return

    # Ensure all required arguments are provided
    if not args.group1_zip or not args.group2_zip or not args.output:
        print_manual()
        return

    # TODO
    
    group_1 = []
    group_1_R = json.dumps(group_1)
    group_2 = []
    group_2_R = json.dumps(group_2)

    #  Pass processed data and output path to the R script
    if args.visual:
        r_script_path = resource_filename(__name__, '../scripts/data_vis.R')
        dp.run_r_script(group_1_R, group_2_R, args.output, r_script_path)
    else:
        print("Visualization is skipped as -v or --visual flag is not set.")

if __name__ == "__main__":
    main()
