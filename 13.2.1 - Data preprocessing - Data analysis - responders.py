# -*- coding: utf-8 -*-

### Metabolomics data analysis ###

## Libraries ##

import os
import numpy as np
import pandas as pd
import math
import statsmodels.stats.multitest as smt
from scipy.stats import gmean
from scipy.stats import ttest_ind
from OUTLIERS import smirnov_grubbs as grubbs


## Functions ##

def log2FC_func(A,B):
    FC = B/A
    log2FC = round(math.log(FC,2),4)
    return log2FC

## Folders ##

Folder1= "Data/Meta data"
Folder2 = "Data/Normalized data"
Folder3 = "Results/Supplementary tables"
Folder4 = "Data/Plot data/Volcano/TEST"
os.makedirs(Folder4,exist_ok=True)

file_out_TEST = "overview_for_responders.xlsx"
## Files ##

meta_data_file = "Patient_meta_data.xlsx"

# Normalized #

File_normalized_iNPH_wo_outliers = "Group iNPH Normalized data without outliers.xlsx"

# supplementary table #

supp_file = "Supplementary table 1.xlsx"

## load data ##

# Meta data #
df_meta = pd.read_excel(os.path.join(Folder1, meta_data_file))

# Normalized data #

df_data = pd.read_excel(os.path.join(Folder2, File_normalized_iNPH_wo_outliers))
df_data = df_data.set_index('Sample number').T
df_data.index.names = ['Compounds']
included_list = df_data.columns.tolist()

resonder_list = df_meta[(df_meta['Shunt response'] == 'Responder') & (df_meta['Samples'].isin(included_list))]['Samples'].tolist()       
nonresonder_list = df_meta[(df_meta['Shunt response'] == 'Non-responder') & (df_meta['Samples'].isin(included_list))]['Samples'].tolist()

## Create overview table - without outliers ##

df_overview = df_data.reset_index()[['Compounds']].copy()
df_overview = df_overview.set_index('Compounds')

## Add Mean and SD to overview ##
# Group Control #
df_overview["Group respond Mean"] = df_data[resonder_list].mean(axis=1)
df_overview["Group respond SD"] = df_data[resonder_list].std(axis=1,ddof=1)
# Group iNPH #
df_overview["Group nonrespond Mean"] = df_data[nonresonder_list].mean(axis=1)
df_overview["Group nonrespond SD"] = df_data[nonresonder_list].std(axis=1,ddof=1)

# Add Log2FC #
df_overview["Log2FC"] = np.log2(df_overview["Group nonrespond Mean"]/df_overview["Group respond Mean"])
## add p-value of welch t test #
df_overview['Pvalue'] = ttest_ind(df_data[resonder_list], df_data[nonresonder_list],nan_policy='omit',equal_var = False, axis=1)[1]
df_overview['Padj'] = smt.fdrcorrection(df_overview['Pvalue'],alpha=0.05,method="indep")[1]

## Save overview table to file ###
df_overview = df_overview.reset_index()
df_overview.to_excel(os.path.join(Folder4,file_out_TEST),sheet_name='Overview',header=True,index=False)