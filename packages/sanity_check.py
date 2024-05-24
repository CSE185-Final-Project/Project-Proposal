import sys
import zipfile
import csv
import os
import pandas as pd

# check if the take in zip files have the same amount of files
def check_files_amount(zip_path):
    # open the zip file in read mode
    file_count = 0
    with zipfile.ZipFile(zip_path, 'r') as zip:
        list_of_files = zip.namelist()
        for f in list_of_files:
            if not f.endswith('/'):
                file_count += 1
        return file_count
    
def check_if_same_amount_of_files(input1, input2):
    if input1 != input2:
        print("The amount of files in two given zip files does not match.\n")
        print(f"Zip file 1 has {input1} files. Zip file 2 has {input2} files.")
        return False
    else:
        print("The amount of files in two given zip files match")
        return True


# create the abs_path_dataframe_list
def convert_files_to_csv(source_dir, df_dir_name="dataframe_home"):
  
    # source_directory = os.path.abspath(source_directory)
    df_directory = os.path.join(source_dir, df_dir_name)
    os.makedirs(df_directory, exist_ok=True)
    
    # list files for all files under given directory
    all_avaliable_files = os.listdir(source_dir)
    df_file_path_list = []

    for file_name in all_avaliable_files:
        # path to access the file
        full_path = os.path.join(source_dir, file_name)

        if os.path.isfile(full_path):

            df = pd.read_csv(full_path, delimiter='\t')

            # store the new file path
            csv_file_path = os.path.join(df_directory,
                                    os.path.splitext(file_name)[0] + '.csv')
            # save to CSV
            df.to_csv(csv_file_path, index=False)

            # Store the full absolute path of the new CSV file
            df_file_path_list.append(os.path.abspath(csv_file_path)) 

    return df_file_path_list


# check if all files have the same header, and create dataframe for it. 
# Only keep the first 7 columns
def check_header():
    return

# check if gene_id is the same:
def check_gene_id():
    return

# check if there are null inside:
def check_null():
    return

