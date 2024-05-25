import sys
import os
import math
from scipy import stats

def correlation(group1_name, group2_name):
    # Get TPM columns
    # Building empty lists according to the number of files in the two zip files
    tpm_group1 = []
    tpm_group2 = []
    for i in range(len(group1_name)):
        new_list = []
        tpm_group1.append(new_list)
    for i in range(len(group2_name)):
        new_list = []
        tpm_group2.append(new_list)

    # Assigning TPM numbers to the corresponding list
    for i in range(len(group1_name)): tpm_group1[i] = group1_name[i]["TPM"].tolist()
    for i in range(len(group2_name)): tpm_group2[i] = group2_name[i]["TPM"].tolist()

    # Adjust TPM numbers
    for lt in tpm_group1: lt = list(map(lambda x: math.log10(x+1), lt))
    for lt in tpm_group2: lt = list(map(lambda x: math.log10(x+1), lt))

    # Generate correlations
    for i in range(0, len(tpm_group1) - 1):
        for j in range(i+1, len(tpm_group1)):
            r = 0.0
            r = stats.pearsonr(tpm_group1[i], tpm_group1[j])[0]
            print("----------- First Group Pearson Correlation Results -----------")
            print("Group 1 input%d vs. Group 1 input%d: %.4f" % (i, j, r))
            if r < 0.3: # Adjustment may be needed.
                print("WARNING: The Pearson correlation result is below 0.3. You may want to check the quality of the input files.")

    for i in range(0, len(tpm_group2) - 1):
        for j in range(i+1, len(tpm_group2)):
            r = 0.0
            r = stats.pearsonr(tpm_group1[i], tpm_group1[j])[0]
            print("----------- Second Group Pearson Correlation Results -----------")
            print("Group 2 input%d vs. Group 2 input%d: %.4f" % (i, j, r))
            if r < 0.3: # Adjustment may be needed.
                print("WARNING: The Pearson correlation result is below 0.3. You may want to check the quality of the input files.")

    # Generate correlations plots
