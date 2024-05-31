# CSE 185 scRNAseq_Easy
`scRNAseq_Easy` is a Python project with embedded R packages, developed for CSE185. It processes STAR and RSEM result files, checks for correlations, and generates a volcano plot to show differential expression analysis.
The scRNAseq_Easy project will output the results that users specify. Specifically, users can choose to output the Pearson correlation result, the CSV file generated after running the DESeq2 R package, and a volcano plot. These outputs are conditional upon successfully passing the packages/sanity_check.py script.

# Installation instructions

Clone the repository and install the required packages using the following commands:
```
git clone https://github.com/CSE185-Final-Project/scRNAseq_Easy/
cd scRNAseq_Easy
pip install .
```
Alternatively, install directly from GitHub:
```
pip install git+https://github.com/CSE185-Final-Project/scRNAseq_Easy.git
```
Export to your local path (needed if you're using class Juypter Notebook server or if you don't have root authorization)
```
export PATH="$HOME/.local/bin:$PATH"
```

If the install was successful, you can type `scRNAseq_Easy help` to view the user manual.  

# Basic usage
The basic usage of `scRNAseq_Easy` is:
```
scRNAseq_Easy <group1_zip> <group2_zip> [options] 
```
> **Example**: To run `scRNAseq_Easy` using example files from this repository:
>```
>scRNAseq_Easy dataset/HFD_Rep.zip dataset/Chow_Rep.zip [options]
>```

# scRNAseq_Easy Options

The paths to two zip files are only required inputs for `scRNAseq_Easy`. Users may additionally specify the options below:
* `<group1_zip>`, `<group2_zip>`  Required. The path to two zipped files containing aligned and quantified gene reads processed by STAR and RSEM.       
* `-o`, `--output <output_path>`   Optional. Specifies the path where the output graph will be saved.
* `-p`, `--pearson` Optional. If set, check the Pearson correlation for the data within the group and stop the program.
* `-d`, `--DESeq2 [-filter int]` Optional. If set, pass all the files to DESeq2 to process and stop. The result will be saved in the output path if set. The result will be filtered by removing the genes with a count lower than `filter`, default `filter = 0`.  Note: Automatically check Pearson correlation.
* `-v`, `--visual [-p-value int, - fod int, -filter int]`   Optional. If set, generate a volcano  plot of the given data. The plot will have labels Up, Down, and None based on p-value and fold-of-change(fod) inputted, default `p-value = 0.05, fod = 0`. Note: Automatically check Pearson correlation and process the data through DESeq2.
* `-name`, `--name <file_path>` Optional. A two-column file without a header. The first column contains the gene ID measured, and the second column contains the corresponding gene name.

Examples:\
Print Manual for usage:\
  `scRNAseq_Easy`\
or\
  `scRNAseq_Easy help`

Check Pearson Correlation within group:  
  `scRNAseq_Easy path/to/group1.zip path/to/group2.zip -o path/to/newdirectory -p`  
    
Process data through DESeq2 and filter out gene with count lower than 10:  
  `scRNAseq_Easy path/to/group1.zip path/to/group2.zip -o path/to/newdirectory -d -filter 10`  
    
Generate the visualization of volcano plot with p-value threshold = 0.05, fold-of-change threshold = 2 :  
  `scRNAseq_Easy path/to/group1.zip path/to/group2.zip -o path/to/output/graph.png -v -p_value 0.05 -fod 2`

# File format
`-d` option will generate a csv file containing the result dataframe processed by DESeq2, deliminator = ','\
`-v` option will generate a volcano plot save as PNG formate.

# Test guide (important)
1. Recommend to test on class Juypter Notebook Server
2. Download and install the package by link
```
pip install git+https://github.com/CSE185-Final-Project/scRNAseq_Easy.git
```
and export by 
```
export PATH="$HOME/.local/bin:$PATH"
```
3. make new directory for test `mkdir test_scRNA`
4. set working directory `cd test_scRNA`
5. download the test file from GitHub: https://github.com/CSE185-Final-Project/scRNAseq_Easy/
   -> dataset
   -> Chow_Rep.zip, HFD_Rep.zip, GRCm38.75.gene_names
6. upload to test_scRNA on the server
7. run command
   ```
   scRNAseq_Easy HFD_Rep.zip Chow_Rep.zip -o ~/test_scRNA -v -name GRCm38.75.gene_names
   ```
8. check the visualization plot `result_vol_plot.png` and deseq2 result `result_deseq2.png`
9. free to modify options based on this manual 

# Contributors
This project was generated by Zhijun Qian, Sicheng Jing, and Jiarun Liu, with inspiratioin from Lab4 Assignment and many other projects.  
  
We want to appreciate the project demo provided by Professor Gymrek:  
`https://github.com/gymreklab/cse185-demo-project/` 
  
And example final projects come from last year:   
`https://github.com/BennyXie/CSE185-GWAS-Implementation/`  
`https://github.com/WillardFord/wf-align-CSE185/`  
`https://github.com/kyrafetter/spyglass/`

Please submit a pull request with any corrections or suggestions. Thank you!

# Testing
We store test file in `dataset/test_file/*`. In order to test whether our code work or not, we will run our code on the file store inside.
defaut:
>```
>scRNAseq_Easy dataset/test_file/baby_HFD_Rep.zip dataset/test_file/baby_Chow_Rep.zip [options]
>```

