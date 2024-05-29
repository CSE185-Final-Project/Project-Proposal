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
    for i in range(0, len(tpm_group1)-1):
        for j in range(i+1, len(tpm_group1)):
            if len(tpm_group1[i]) == len(tpm_group1[j]):
                res = stats.pearsonr(tpm_group1[i], tpm_group1[j], alternative= "two-sided", method = None)
                print("----------- First Group Pearson Correlation Results -----------")
                print("Sample size of Group 1 input %d: %d" % (i+1, len(tpm_group1[i])))
                print("Sample size of Group 1 input %d: %d" % (j+1, len(tpm_group1[j])))
                print("Correlation of Group 1 input %d vs. Group 1 input %d: %.4f" % (i+1, j+1, res[0]))
                if res[0] < 0.3: # Adjustment may be needed.
                    print("WARNING: The Pearson correlation result is below 0.3. You may want to check the quality of the input files.")
                print("P-value: %.4f " % (res[1]))
                print("Significant level: P < %.4f" % (stats.norm.sf(abs(res[0]))))
                print("95%", res.confidence_interval(confidence_level=0.95), "for correlation")
            else:
                print("WARNING: Group 1 input %d file and Group 1 input %d file don't have the same sample size, so cannot calculate Pearson correlation." % (i+1, j+1))

    for i in range(0, len(tpm_group2) - 1):
        for j in range(i+1, len(tpm_group2)):
            if len(tpm_group2[i]) == len(tpm_group2[j]):
                res = stats.pearsonr(tpm_group2[i], tpm_group2[j], alternative= "two-sided", method = None)
                print("----------- Second Group Pearson Correlation Results -----------")
                print("Sample size of Group 2 input %d: %d" % (i+1, len(tpm_group2[i])))
                print("Sample size of Group 2 input %d: %d" % (j+1, len(tpm_group2[j])))
                print("Correlation of Group 2 input %d vs. Group 2 input %d: %.4f" % (i+1, j+1, res[0]))
                if res[0] < 0.3: # Adjustment may be needed.
                    print("WARNING: The Pearson correlation result is below 0.3. You may want to check the quality of the input files.")
                print("P-value: %.4f " % (res[1]))
                print("Significant level: P < %.4f" % (stats.norm.sf(abs(res[0]))))
                print("95%", res.confidence_interval(confidence_level=0.95), "for correlation")
            else:
                print("WARNING: Group 2 input %d file and Group 2 input %d file don't have the same sample size, so cannot calculate Pearson correlation." % (i+1, j+1))

