# CSE 185 scRNAseq_Easy
scRNAseq_Easy is a python and with some R package inside that will takin in STAR and RSEM results file, checking for correlation, and then generate the volcano plot to show the differnetial expression analysis.

# Installation instructions
```
git clone https://github.com/CSE185-Final-Project/scRNAseq_Easy/
cd scRNAseq_Easy
pip install setup.py
```
if the install was successful, typing `scRNAseq_Easy help` to see the user manual.  

# Basic usage instructions
The basic usage of `scRNAseq_Easy` is:
```
scRNAseq_Easy [options] <group1_zip> <group2_zip> -o <output_path>
```
To run `scRNAseq_Easy` on test example (using files in this repo):
```
scRNAseq_Easy dataset/HFD_Rep.zip dataset/Chow_Rep.zip
```

# scRNASeq_Easy Options

* `-o`, `--output <output_path>`   Optional. Specifies the path where the output graph will be saved.     
* `-v`, `--visual`   Optional. If set, runs visualization of the correlation among datasets if set to True.

Generate the volcano plot in current directory:  
  `scRNAseq_Easy path/to/group1.zip path/to/group2.zip`  
    
Generate the volcano plot in user specified directory:  
  `scRNAseq_Easy path/to/group1.zip path/to/group2.zip -o path/to/newdirectory`  
    
Generate the visualization of correlation and the volcano plot in the specified output path:  
  `scRNAseq_Easy path/to/group1.zip path/to/group2.zip -v -o path/to/output/graph.png`

# File format
Under default version, the output file format is a png file - the volcano plot

# Credits
We want to appreciate the project demo provided by Professor Gymrek:  
`https://github.com/gymreklab/cse185-demo-project/`  
And example final projects come from last year:   
`https://github.com/BennyXie/CSE185-GWAS-Implementation/`  
`https://github.com/WillardFord/wf-align-CSE185/`  
`https://github.com/kyrafetter/spyglass/`

# Bonus: badges


