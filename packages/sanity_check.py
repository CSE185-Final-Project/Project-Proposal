import zipfile
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
def create_df(file_path):
    df = pd.read_csv(file_path, delimiter=',')
    df_trimmed = df.iloc[:, :7]
    return df_trimmed

def check_header(df_dict):
    if not df_dict:
        print("The dictionary is empty.")
        return False

    header_example = next(iter(df_dict.values())).columns

    for df in df_dict.values():
        if not df.columns.equals(header_example):
            print('The given files have different headers')
            return False
        
    print('Pass header check')
    return True

# check if gene_id is the same:
def check_gene_id(df_dict):

    if not df_dict:
        print("The dictionary is empty.")
        return False
    
    df_iterator = iter(df_dict.values())

    try:
        gene_id_example = next(df_iterator)['gene_id']
        # print(gene_id_example)
    except KeyError:
        print('Column gene_id not found')
        return False  

    # Iterate through the remaining DataFrames
    for df in df_iterator:
        # print(df['gene_id'])
        try:
            if not df['gene_id'].equals(gene_id_example):
                print('The given files have different gene IDs')
                return False
        except KeyError:
            print('gene id column not found in one of the DataFrames')
            return False
        
    print('Pass Gene ID check')
    return True

# check if there are null inside:
def check_null(df_dict):

    for df in df_dict.values():

        if df.isnull().any().any():
            print('There is null value in the given file')
            return False       
    else:
        print('Pass null check')
        return True 
    
# output two list of dataframe for pearson correlation
def split_dfs(df_dict, x):
    group1_df = []  
    group2_df = [] 
    
    for index, df in enumerate(df_dict.values()):
        if index < x:
            group1_df.append(df)  
        else:
            group2_df.append(df)  
    
    return group1_df, group2_df

def dataframes_to_csv(list_group1, list_group2, output_dir):
     # create output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir) 

    def save_df_to_csv(df, file_name):
        path = os.path.join(output_dir, file_name)
        df.to_csv(path, index=False)  
        return path

    # Initialize a list to store file paths
    group1_path = []
    group2_path = []

    # Process the first list of DataFrames
    for i, df in enumerate(list_group1, 1):  # Start enumeration at 1 for file naming
        file_name = f"group1_df{i}.csv"
        path = save_df_to_csv(df, file_name)
        group1_path.append(path)

    # Process the second list of DataFrames
    for i, df in enumerate(list_group2, 1):  # Start enumeration at 1 for file naming
        file_name = f"group2_df{i}.csv"
        path = save_df_to_csv(df, file_name)
        group2_path.append(path)

    return group1_path, group2_path

def delete_files_in_directory(directory):
    # Check if the directory exists
    if not os.path.exists(directory):
        return 
    
    # List all items in the directory
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        # Check if the item is a file and then delete it
        if os.path.isfile(item_path):
            os.remove(item_path)  # Remove the file

#
def unzip_files_path(abs_path):
    unzip_file_path_results = []
    for item in os.listdir(abs_path):
        item_path = os.path.join(abs_path, item)
        if os.path.isfile(item_path):
            unzip_file_path_results.append(item_path)
    return unzip_file_path_results


def ensure_genes_results(file_paths):

    updated_paths = []
    for path in file_paths:
        directory, filename = os.path.split(path)
        parts = filename.split('.')
        if filename.endswith('.genes.results') and len(parts) == 3 and parts[0] != 'RSEM':
            updated_paths.append(path)
            continue
        if filename.endswith('.txt'):
            base_name = filename[:-4].split('.')[0]
        else:
            base_name = filename.split('.')[0]
        new_filename = f"{base_name}.genes.results"
        new_path = os.path.join(directory, new_filename)
        updated_paths.append(new_path)
    
    return updated_paths

