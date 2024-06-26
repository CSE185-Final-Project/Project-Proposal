import zipfile
import os
import subprocess
import argparse
import sys
import json
from pkg_resources import resource_filename
import packages.R_prep as dp
import packages.sanity_check as sanity_check
import packages.correlation as corr
import time
import tracemalloc
from memory_profiler import memory_usage
from pkg_resources import resource_filename


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
    manual_path = resource_filename(__name__, '../docs/Manual.txt')
    with open(manual_path, 'r') as f:
        manual_content = f.read()
    print(manual_content)

def main():
    parser = argparse.ArgumentParser(description="Process gene result files and generate visualizations.")
    parser.add_argument('group1_zip', type=str, nargs= "?", help='Path to the first zip file.')
    parser.add_argument('group2_zip', type=str, nargs= "?", help='Path to the second zip file.')
    parser.add_argument('-o', '--output', type=str, help='Path to save the output graph.')
    parser.add_argument('-p', '--pearson', action='store_true', help='Run Pearson Correlation if set to True.')
    parser.add_argument('-v', '--visual', action='store_true', help='Run visualization of differential equation if set to True.')
    parser.add_argument('-d', '--deseq2', action='store_true', help='Return analyize result from Deseq2 if set to True.')
    parser.add_argument('-p_value','--p_value', type=float, default=0.05, help='Set p-value threshold for visualization.')
    parser.add_argument('-fod', '--fod', type=float, default=1, help='Set FOD value for visualization.')
    parser.add_argument('-filter', '--filter', type=float, default=0, help='filter the genes with count lower than')
    parser.add_argument('-name', '--name', type=str, default="NO", help='2-column dataset containing the name of the genes')
    
    # Parse the arguments
    args = parser.parse_args()
    
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1].lower() == 'help'):
        print_manual()
        return

    # Ensure all required arguments are provided
    if not args.group1_zip or not args.group2_zip or not args.output:
        print("error: the following arguments are required to run the main function: group1_zip, group2_zip, -o/--output")
        print_manual()
        return
    
    # Benchmarking start
    start_time = time.time()
    tracemalloc.start()

    mem_usage_before = memory_usage(max_usage=True)

    #-------------------------sanity_check (zhqian)---------------------------#

    # check if the first zip file and the second zip file has the same amount of files
    zip_file_path_1 = args.group1_zip
    zip_file_path_2 = args.group2_zip
    zip_file_1_file_count = sanity_check.check_files_amount(zip_file_path_1)
    zip_file_2_file_count = sanity_check.check_files_amount(zip_file_path_2)

    # if there are not the same amount of files in zip file path, then end the program
    if not sanity_check.check_if_same_amount_of_files(zip_file_1_file_count, zip_file_2_file_count):
        print(f"Requires same ammount of files within two zip files. Got {zip_file_1_file_count} files and {zip_file_2_file_count} files")
        return
    
    # unzip two input zip_file_path and output it in a new directory
    new_direct1 = 'datasets_home1'
    sanity_check.delete_files_in_directory(new_direct1)
    source_path1 = unzip_files(zip_file_path_1, new_direct1)

    new_direct2 = 'datasets_home2'
    sanity_check.delete_files_in_directory(new_direct2)
    source_path2 = unzip_files(zip_file_path_2, new_direct2)

    # to create the list of csv file
    csv_files_list1 = sanity_check.convert_files_to_csv(source_path1, df_dir_name="dataframe_home")
    csv_files_list2 = sanity_check.convert_files_to_csv(source_path2, df_dir_name="dataframe_home")

    df_dict = {}
    increment = len(csv_files_list1)
    for i in range(len(csv_files_list1)):
        digit = i + 1
        name = f'df_trimmed{digit}'
        file_path = csv_files_list1[i]
        df_dict[name] = sanity_check.create_df(file_path)

    for i in range(len(csv_files_list2)):
        digit = i + 1 + increment
        name = f'df_trimmed{digit}'
        file_path = csv_files_list2[i]
        df_dict[name] = sanity_check.create_df(file_path)
    # now the df_dict will have {df_1: the real trimmed dataframe}
        
    # if there are not the same header line, then end the program
    if not sanity_check.check_header(df_dict):
        return
    
    # gene id check
    if not sanity_check.check_gene_id(df_dict):
        return 
    
    # null element check
    if not sanity_check.check_null(df_dict):
        return
    
    print('Pass all sanity check!')
    # for pearson correlation to take in, two list of dataframe
    group_1_df, group_2_df = sanity_check.split_dfs(df_dict, increment)


    current_directory = os.getcwd()
    subdirectory = 'trimmed_csv_files'
    sanity_check.delete_files_in_directory(subdirectory)
    output_dir_csv = os.path.join(current_directory, subdirectory)
    if not os.path.exists(output_dir_csv):
        os.makedirs(output_dir_csv)
    # for R package to use, two list of csv file paths
    group_1_path, group_2_path = sanity_check.dataframes_to_csv(group_1_df, group_2_df, output_dir_csv)


    new_group1_unzip_file_path = sanity_check.unzip_files_path(source_path1)
    new_group2_unzip_file_path = sanity_check.unzip_files_path(source_path2)

    group1_genes_results_path = sanity_check.ensure_genes_results(new_group1_unzip_file_path)
    group2_genes_results_path = sanity_check.ensure_genes_results(new_group2_unzip_file_path)



    df_dict = {} #clear our df_dict
    csv_files_list1 = []
    csv_files_list2 = []
        
    #--------------------------------------------------------------------------#


    #----------------------------------correlation(Sicheng)---------------------------------------#

    if args.pearson or args.visual:
        corr.correlation(group_1_df, group_2_df)
    else:
        print("Calculating Pearson Correlation is skipped as -p or --pearson flag is not set.")
    
    #---------------------------------------------------------------------------------------------#

    group_1_R = json.dumps(group1_genes_results_path)
    group_2_R = json.dumps(group2_genes_results_path)

    #  Pass processed data and output path to the R script
    if args.visual or args.deseq2:
        deseq2 = str(args.deseq2)
        p_value = str(args.p_value)
        fod =str(args.fod)
        filter = str(args.filter)
        name = str(args.name)
        r_script_path = resource_filename(__name__, '../scripts/data_vis.R')
        dp.run_r_script(group_1_R, group_2_R, args.output, p_value, fod, filter, name, deseq2, r_script_path)
    else:
        print("Visualization is skipped as -v or --visual flag is not set.")
    
    # Benchmarking end
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    mem_usage_after = memory_usage(max_usage=True)

    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print(f"Peak memory usage: {peak / 10**6:.2f} MB")
    print(f"Memory usage before: {mem_usage_before} MB")
    print(f"Memory usage after: {mem_usage_after} MB")

if __name__ == "__main__":
    main()
