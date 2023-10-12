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

## input ##

DP_cutoff = 0

## Functions ##

def log2FC_func(A,B):
    FC = B/A
    log2FC = round(math.log(FC,2),4)
    return log2FC

## Folders ##

Folder0= "Data/Meta data"
Folder1 = "Data/Data cleaning"
Folder2 = "Data/Raw data analysis"
os.makedirs(Folder2, exist_ok=True)
Folder3 = "Data/PCA data/Raw"
os.makedirs(Folder3, exist_ok=True)
Folder4 = "Data/Data analysis"
os.makedirs(Folder4,exist_ok=True)
Folder5 = "Data/Normalized data"
os.makedirs(Folder5,exist_ok=True)

## Files ##

File0 = "Meta_data_groups.xlsx"
File1 = "raw_data_QC_iNPH_Control.xlsx"
File2 = "Raw_data_DP.xlsx"
File3 = "PCA_data.xlsx"
File4 = "PCA_targets.xlsx"
File6 = "DP overview.xlsx"
File7 = "Data analysis overview.xlsx"

# Normalized #
File_normalized = "Normalized data for group iNPH and Control.xlsx"
File_normalized_iNPH = "Group iNPH Normalized data.xlsx"
File_normalized_Control = "Group Control Normalized data.xlsx"
# Normalized without outliers 
File_normalized_data_wo_outliers = "Normalized data for group iNPH and Control without outliers.xlsx"
File_normalized_iNPH_wo_outliers = "Group iNPH Normalized data without outliers.xlsx"
File_normalized_Control_wo_outliers = "Group Control Normalized data without outliers.xlsx"

### load data ###

# Meta data #

df_groups = pd.read_excel(os.path.join(Folder0,File0))
df_groups_LOI = df_groups.loc[df_groups['LOI'] == "Yes"]
LOI_metabolite_list = df_groups_LOI['Compounds'].tolist()

df = pd.read_excel(os.path.join(Folder1,File1)).rename(columns=({'Unnamed: 0':'Compounds'}))

Header = df.columns.values.tolist()
QC_list = list(filter(lambda x: x.startswith('QC_'), Header))
Group_iNPH_list = list(filter(lambda x: x.startswith("iNPH_"), Header))
Group_Control_list = list(filter(lambda x: x.startswith("Control_"), Header))

# Modulate data for dict conversion #

df = df.set_index('Compounds')
Info_dict_QC = dict(zip(df.index, df[QC_list].values))
Info_dict_iNPH = dict(zip(df.index, df[Group_iNPH_list].values))
Info_dict_Control = dict(zip(df.index, df[Group_Control_list].values))

Compounds = df.index.tolist()

## Calculate raw descriptive power (DP) ##
Raw_DP_dict = {}
RAW_STD_dict_QC = {}
RAW_STD_dict_Samples = {}
Raw_Significant_metabolite_list = []
# Find DP of raw data and list of significant Compounds -> DP > 2.5 #
for key in Compounds:
    Group_iNPH_and_Control_concatenated = np.concatenate((Info_dict_iNPH[key], Info_dict_Control[key]), axis=None)
    Raw_DP = np.std(Group_iNPH_and_Control_concatenated,ddof=1)/np.std(Info_dict_QC[key],ddof=1)
    Raw_DP_dict[key] = Raw_DP
    RAW_STD_dict_Samples[key] = np.std(Group_iNPH_and_Control_concatenated,ddof=1)/np.mean(Info_dict_QC[key])
    RAW_STD_dict_QC[key] = np.std(Info_dict_QC[key],ddof=1)/np.mean(Info_dict_QC[key])
    if Raw_DP > DP_cutoff:
        if key in LOI_metabolite_list: #NEW!!!
            Raw_Significant_metabolite_list.append(key)
        else:
            pass
        #Raw_Significant_metabolite_list.append(key)
    else:
        pass
  
# create dataframe from DP values (raw) #
raw_df_DP = pd.DataFrame({'Compounds': list(Raw_DP_dict.keys()),'DP':list(Raw_DP_dict.values()),'std samples':list(RAW_STD_dict_Samples.values()),'std QC':list(RAW_STD_dict_QC.values())})

raw_df_DP['Significance'] = np.where(raw_df_DP['DP'] >= DP_cutoff, "Yes", "No")

raw_df_DP.to_excel(os.path.join(Folder2,File2),sheet_name='Raw DP calc',header=True,index=False)

## Create PCA plot tables ##

df_without_QC = df[Group_iNPH_list+Group_Control_list]
# transpose data for correct PCA annotation #
PCA_df_T = df_without_QC.T
# Only include Compounds with DP > 2.5 #
PCA_df = PCA_df_T.loc[:, PCA_df_T.columns.isin(Raw_Significant_metabolite_list)]

PCA_targets = pd.DataFrame(index=PCA_df.index.copy())
PCA_targets['Samples'] = PCA_targets.index
PCA_targets.loc[PCA_targets['Samples'].str.startswith('iNPH_'), 'Target'] = 'iNPH'
PCA_targets.loc[PCA_targets['Samples'].str.startswith('Control_'), 'Target'] = 'Control'


PCA_df.to_excel(os.path.join(Folder3,File3),sheet_name='PCA data',header=False,index=False)
PCA_targets.to_excel(os.path.join(Folder3,File4),sheet_name='PCA Targets',header=False,index=False)

## For PCA plot ##
# Run script 3.1.2 - PCA plots for raw data #

## Normalize data for Compounds DP > 2.5 ##
# Reduce dataframe to only Compounds with DP > 2.5 #
df_significant = df[df.index.isin(Raw_Significant_metabolite_list)]
# Calculate geomean for Compounds
df_geomean = pd.DataFrame(index=df_significant.index.copy())
df_geomean['geomean'] = gmean(df_significant.iloc[:, df_significant.columns.get_indexer(QC_list)], axis=1)

# Normalize data based on geomean #
DF_normalized = df_significant.loc[:,Group_iNPH_list+Group_Control_list].div(df_geomean["geomean"], axis=0)
## Remove outliers
DF_normalized_without_outliers =  DF_normalized.copy()

## Save normalized data to files ##

DF_normalized_all_T = DF_normalized.reset_index().rename(columns=({"Compounds":"Samples"})).set_index('Samples').T
DF_normalized_all_T.to_excel(os.path.join(Folder5,File_normalized),sheet_name='Normalized data',index=False)

# Divide normalized data into two seperate files #

DF_normalized_all_T_iNPH = DF_normalized_all_T.T[Group_iNPH_list].T
DF_normalized_all_T_Control = DF_normalized_all_T.T[Group_Control_list].T

DF_normalized_all_T_iNPH.to_excel(os.path.join(Folder5,File_normalized_iNPH),sheet_name='Normalized data iNPH')
DF_normalized_all_T_Control.to_excel(os.path.join(Folder5,File_normalized_Control),sheet_name='Normalized data Control')


index_list = DF_normalized.index
column_list = np.array(DF_normalized.columns.tolist())
counter = 0
for i in DF_normalized.index:
    # Get array for control (C) and Disease (iNPH)
    numpy_array_iNPH = np.array(DF_normalized.loc[i,Group_iNPH_list])
    numpy_array_Control = np.array(DF_normalized.loc[i,Group_Control_list])
    # Get outlier index #
    outlier_index_iNPH =  grubbs.two_sided_test_indices(numpy_array_iNPH, alpha=.05)
    outlier_index_iNPH = np.array(outlier_index_iNPH,dtype=int)
    outlier_index_Control =  grubbs.two_sided_test_indices(numpy_array_Control, alpha=.05)
    outlier_index_Control = np.array(outlier_index_Control,dtype=int)
    outlier_index_Control = (outlier_index_Control + len(Group_iNPH_list))
    all_entries = np.concatenate((outlier_index_iNPH,outlier_index_Control), axis=0)
    if len(all_entries) > 0:
        cols = column_list[all_entries].tolist()
        for loc_col in cols:
            DF_normalized_without_outliers.at[i,loc_col] = np.nan


# Transpose normalized data #
# Here without outliers #!!! 
DF_normalized_T = DF_normalized_without_outliers.T.copy()
DF_normalized_T = DF_normalized_T.reset_index().rename(columns=({'index':"Sample number"}))
# Save normalized - transposed data to file #
DF_normalized_T.to_excel(os.path.join(Folder5,File_normalized_data_wo_outliers),sheet_name='Normalized data',index=False)

## Divide normalized data into two seperate files ##

DF_normalized_T_iNPH = DF_normalized_T.set_index('Sample number').T[Group_iNPH_list].T
DF_normalized_T_Control = DF_normalized_T.set_index('Sample number').T[Group_Control_list].T

DF_normalized_T_iNPH.to_excel(os.path.join(Folder5,File_normalized_iNPH_wo_outliers),sheet_name='Normalized data iNPH')
DF_normalized_T_Control.to_excel(os.path.join(Folder5,File_normalized_Control_wo_outliers),sheet_name='Normalized data Control')
                          

## Create overview table - without outliers ##

df_overview = DF_normalized_without_outliers.reset_index()[['Compounds']].copy()
df_overview = df_overview.set_index('Compounds')
## Add Mean and SD to overview ##
# Group Control #
df_overview["Group Control Mean"] = DF_normalized_without_outliers[Group_Control_list].mean(axis=1)
df_overview["Group Control SD"] = DF_normalized_without_outliers[Group_Control_list].std(axis=1,ddof=1)
# Group iNPH #
df_overview["Group iNPH Mean"] = DF_normalized_without_outliers[Group_iNPH_list].mean(axis=1)
df_overview["Group iNPH SD"] = DF_normalized_without_outliers[Group_iNPH_list].std(axis=1,ddof=1)

# Add Log2FC #
df_overview["Log2FC"] = np.log2(df_overview["Group iNPH Mean"]/df_overview["Group Control Mean"])
## add p-value of welch t test #
df_overview['Pvalue'] = ttest_ind(DF_normalized_without_outliers[Group_Control_list], DF_normalized_without_outliers[Group_iNPH_list],nan_policy='omit',equal_var = False, axis=1)[1]
df_overview['Padj'] = smt.fdrcorrection(df_overview['Pvalue'],alpha=0.05,method="indep")[1]

## Save overview table to file ###
df_overview = df_overview.reset_index()
#.rename(columns={'Name':"Compounds"})
df_overview.to_excel(os.path.join(Folder4,File7),sheet_name='Overview',header=True,index=False)