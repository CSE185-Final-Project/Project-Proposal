import zipfile
import os
import subprocess
import argparse
import sys
import json
from pkg_resources import resource_filename
import packages.R_prep as dp
import sanity_check
import correlation


# this method unzip file into a new directory
def unzip_files(zip_file, extract_to_new_dir):

    # convert to abosolute path
    abs_path = os.path.abspath(extract_to_new_dir)

    # makesure the directory exists / create it
    os.makedirs(abs_path, exist_ok=True)

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(abs_path)
    return abs_path

def print_manual():
    manual_path = resource_filename(__name__, '../docs/manual.txt')
    with open(manual_path, 'r') as f:
        manual_content = f.read()
    print(manual_content)

def main():
    parser = argparse.ArgumentParser(description="Process gene result files and generate visualizations.")
    parser.add_argument('group1_zip', type=str, help='Path to the first zip file.')
    parser.add_argument('group2_zip', type=str, help='Path to the second zip file.')
    parser.add_argument('-o', '--output', type=str, help='Path to save the output graph.')
    parser.add_argument('-v', '--visual', action='store_true', help='Run visualization of correlation if set to True.')
    
    # Parse the arguments
    args = parser.parse_args()
    
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1].lower() == 'help'):
        print_manual()
        return

    # Ensure all required arguments are provided
    if not args.group1_zip or not args.group2_zip or not args.output:
        print_manual()
        return

    #-------------------------sanity_check (zhqian)---------------------------#

    # check if the first zip file and the second zip file has the same amount of files
    zip_file_path_1 = args.group1_zip
    zip_file_path_2 = args.group2_zip
    zip_file_1_file_count = sanity_check.check_files_amount(zip_file_path_1)
    zip_file_2_file_count = sanity_check.check_files_amount(zip_file_path_2)

    # if there are not the same amount of files in zip file path, then end the program
    if not sanity_check.check_if_same_amount_of_files(zip_file_1_file_count, zip_file_2_file_count):
        return
    
    # unzip two input zip_file_path and output it in a new directory
    new_direct1 = 'datasets_home1'
    source_path1 = unzip_files(zip_file_path_1, new_direct1)

    new_direct2 = 'datasets_home2'
    source_path2 = unzip_files(zip_file_path_2, new_direct2)

    # to create the list of csv file
    csv_files_list_1 = sanity_check.convert_files_to_csv(source_path1, df_dir_name="dataframe_home")
    csv_files_list_2 = sanity_check.convert_files_to_csv(source_path2, df_dir_name="dataframe_home")


    #----------------------------------correlation(Sicheng)---------------------------------------#
    
    group_1_df = []
    group_2_df = []
    correlation(group_1_df, group_2_df)
    
    #-------------------------------------------------------------------------#

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
