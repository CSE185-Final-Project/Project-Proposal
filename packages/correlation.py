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
    for i in range(len(tpm_group1)):
        tpm_group1[i] = [math.log10(float(x) + 1) for x in tpm_group1[i]]
    for i in range(len(tpm_group2)):
        tpm_group2[i] = [math.log10(float(x) + 1) for x in tpm_group2[i]]

    # Generate correlations
    print("----------- First Group Pearson Correlation Results -----------")
    print("Sample size of Group 1 samples: %d" % (len(tpm_group1[0])))
    print("")
    countpass = 0
    count = 0
    for i in range(0, len(tpm_group1)-1):
        for j in range(i+1, len(tpm_group1)):
            count += 1
            res = stats.pearsonr(tpm_group1[i], tpm_group1[j], alternative= "two-sided", method = None)
            print("Correlation of Group 1 sample %d vs. Group 1 sample %d: %.4f" % (i+1, j+1, res[0]))
            if res[0] < 0.3: # Adjustment may be needed.
                print("WARNING: The Pearson correlation result is below 0.3. You may want to check the quality of the input files.")
            if res[1] > 0.05:
                print("WARNING: The Pearson correlation is not statistically significant since it greater than 0.05.")
                print("Your Pearson correlation: %.4f" %(res[1]))
            if res[0] >= 0.3 and res[1] <= 0.05:
                countpass += 1
            if res[1] < 0.0001:
                print("Significant level: P < 0.0001")
            else:
                print("Significant level: P < %.4f" % (res[1]))
            print("95%", res.confidence_interval(confidence_level=0.95), "for this correlation coefficient")
            print("")
    if count == countpass:
        print("Group 1 passed the correlation checks. Samples in this group are associated with each other.")


    print("")
    print("----------- Second Group Pearson Correlation Results -----------")
    print("Sample size of Group 2 samples: %d" % (len(tpm_group2[0])))
    print("")
    countpass = 0
    count = 0
    for i in range(0, len(tpm_group2) - 1):
        for j in range(i+1, len(tpm_group2)):
            count += 1
            res = stats.pearsonr(tpm_group2[i], tpm_group2[j], alternative= "two-sided", method = None)
            print("Correlation of Group 2 sample %d vs. Group 2 sample %d: %.4f" % (i+1, j+1, res[0]))
            if res[0] < 0.3: # Adjustment may be needed.
                print("WARNING: The Pearson correlation result is below 0.3. You may want to check the quality of the input files.")
            if res[1] > 0.05:
                print("WARNING: The Pearson correlation is not statistically significant since it greater than 0.05.")
                print("Your Pearson correlation: %.4f" % (res[1]))
            if res[0] >= 0.3 and res[1] <= 0.05:
                countpass += 1
            if res[1] < 0.0001:
                print("Significant level: P < 0.0001")
            else:
                print("Significant level: P < %.4f" % (res[1]))
            print("95%", res.confidence_interval(confidence_level=0.95), "for this correlation coefficient")
            print("")
    if count == countpass:
        print("Group 2 passed the correlation checks. Samples in this group are associated with each other.")


