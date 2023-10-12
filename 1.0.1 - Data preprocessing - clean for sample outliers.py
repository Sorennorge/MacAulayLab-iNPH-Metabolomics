# -*- coding: utf-8 -*-

### Data analysis - Outlier test for whole samples ###

## Requirements ##
# Raw data - Metabolomics #

## Libraries ##

import os
import numpy as np
import pandas as pd
from OUTLIERS import smirnov_grubbs as grubbs
from natsort import natsort_keygen

## Global counter variable ##

control_counter = 0

## functions ##

def rewrite_samples(df):
    global control_counter
    number = df['Samples'].split("_")[1]
    condition = df['Diagnosis']
    if condition == 'Control':
        control_counter += 1
        return "{}_{}".format(condition,control_counter)
    else:
        return "{}_{}".format(condition,number)

## Folders ##

# input #
Folder1 = "Data/Raw data"

# output #

Folder2 = "Data/Lookup data"
Folder3 = "Data/Data cleaning"

os.makedirs(Folder2,exist_ok=True)
os.makedirs(Folder3,exist_ok=True)

##  Files ##

# Input #

file1_input = "Raw_data.xlsx"

# output #

file2_init_sample_lookup_file = "Initial_Sample_lookup_table.xlsx"
file3_init_outliers_overview = 'Outliers overview.xlsx'

file4_raw_data_without_outliers = "raw_data_QC_iNPH_Control.xlsx"

# Load data #

df_init = pd.read_excel(os.path.join(Folder1,file1_input))


df_init['Sample number'] = df_init.apply(rewrite_samples,axis=1)

df_correct_anno = df_init[['Samples','Diagnosis','Sample number']]

# Save initial lookup sample number #

df_correct_anno.to_excel(os.path.join(Folder2,file2_init_sample_lookup_file),index=False)

## Set sample number to index and remove Samples and diagnosis ##

df_init = df_init.set_index('Sample number').drop('Samples',axis=1).drop('Diagnosis',axis=1)

## Transpose dataframe ##

df_init_T = df_init.T

## Sample lists ##

QC_list = df_init_T.columns[df_init_T.columns.str.startswith("QC")].to_list()
iNPH_list = df_init_T.columns[df_init_T.columns.str.startswith("iNPH")].to_list()
Control_list = df_init_T.columns[df_init_T.columns.str.startswith("Control")].to_list()

## init variables ##

# initial data variables for data cleaning #

init_Name_list = df_init_T.index.tolist()

# create dictionaries with numpy arrays #

init_QC_dict = dict(zip(df_init_T.index, df_init_T[QC_list].values))
init_Group_iNPH_dict = dict(zip(df_init_T.index, df_init_T[iNPH_list].values))
init_Group_Control_dict = dict(zip(df_init_T.index, df_init_T[Control_list].values))

# Outlier calculations #

Group_iNPH_without_outliers = {}
Group_Control_without_outliers = {}

## create dictionaries with numpy arrays ##

## run grubbs test for outliers in initial raw data ##

outlier_overview_iNPH = {}
outlier_overview_Control = {}

for key in init_Name_list:
    ## remove outliers ##
    Group_iNPH_without_outliers[key] = grubbs.test(init_Group_iNPH_dict[key], alpha=.05)
    Group_Control_without_outliers[key] = grubbs.test(init_Group_Control_dict[key], alpha=.05)
    
    ## Get outlier index and and create overview of which samples have outliers ##
    outlier_index_iNPH = grubbs.two_sided_test_indices(init_Group_iNPH_dict[key], alpha=.05)
    outlier_index_Control = grubbs.two_sided_test_indices(init_Group_Control_dict[key], alpha=.05)
    ## iNPH outliers overview ##
    for i in outlier_index_iNPH:
        outlier_sample_iNPH = "iNPH_{}".format(i+1)
        if outlier_sample_iNPH in outlier_overview_iNPH:
            outlier_overview_iNPH[outlier_sample_iNPH] += 1
        else:
            outlier_overview_iNPH[outlier_sample_iNPH] = 1
    ## Control outliers overview ##
    for i in outlier_index_Control:
        outlier_sample_Control = "Control_{}".format(i+1)
        if outlier_sample_Control in outlier_overview_Control:
            outlier_overview_Control[outlier_sample_Control] += 1
        else:
            outlier_overview_Control[outlier_sample_Control] = 1
## Percentage calculateion ##
outlier_overview_percentage = {}
for key in outlier_overview_iNPH:
    outlier_overview_percentage[key] = round(outlier_overview_iNPH[key]/len(init_Name_list)*100,2)
for key in outlier_overview_Control:
    outlier_overview_percentage[key] = round(outlier_overview_Control[key]/len(init_Name_list)*100,2)   

## Create overview dataframe of outliers ##
# iNPH #
df_outlier_overview_iNPH = pd.DataFrame.from_dict(outlier_overview_iNPH,orient='index',columns=['Outliers'])
df_outlier_overview_iNPH['Percentage'] = df_outlier_overview_iNPH.index.map(outlier_overview_percentage)
df_outlier_overview_iNPH = df_outlier_overview_iNPH.reset_index().rename(columns=({"index":"Samples"}))
df_outlier_overview_iNPH = df_outlier_overview_iNPH.sort_values(by="Samples",key=natsort_keygen()).reset_index(drop=True)

# Control #
df_outlier_overview_Control = pd.DataFrame.from_dict(outlier_overview_Control,orient='index',columns=['Outliers'])
df_outlier_overview_Control['Percentage'] = df_outlier_overview_Control.index.map(outlier_overview_percentage)
df_outlier_overview_Control = df_outlier_overview_Control.reset_index().rename(columns=({"index":"Samples"}))
df_outlier_overview_Control = df_outlier_overview_Control.sort_values(by="Samples",key=natsort_keygen()).reset_index(drop=True)

df_outlier_overview = pd.concat([df_outlier_overview_iNPH,df_outlier_overview_Control],axis=0,ignore_index=True)                                                                               

df_outlier_overview.to_excel(os.path.join(Folder3,file3_init_outliers_overview),index=False)

# Exclusion of samples based on percentage of outliers within the sample #
Sample_exclusion_list = []
for key in outlier_overview_percentage:
    if outlier_overview_percentage[key] > 20:
        Sample_exclusion_list.append(key)


df_raw_without_outliers = df_init_T[df_init_T.columns[~df_init_T.columns.isin(Sample_exclusion_list)]]

## Save dataframe without outlier samples to file ##

df_raw_without_outliers.to_excel(os.path.join(Folder3,file4_raw_data_without_outliers))