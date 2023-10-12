# -*- coding: utf-8 -*-

### Clean raw data for analysis ###

import os
import pandas as pd

## Global variable ##

Sample_counter = 0
QC_counter = 0

## Function ##

def Sample_anno(df):
    global Sample_counter
    global QC_counter
    if df['Group'] == 'QC':
        QC_counter += 1
        return 'QC_{}'.format(QC_counter)
    else:
        Sample_counter += 1
        return 'Sample_{}'.format(Sample_counter)
        
def Sample_anno_meta(df):
    sample = 'Sample_{}'.format(df['Sample number'])
    return sample
## Folders ##

Folder1 = "Data/Raw data"
Folder2 = "Data/Meta data"

## Files ##

file1_input = "Viime 2_v2.csv"
file_meta = "Patient_meta_data.xlsx"

# Output #

File_out_1 = "Raw_data_full.xlsx"
File_out_2 = "Raw_data.xlsx"
File_out_3 = "Raw_data_transposed.xlsx"

## Load data ##

df_raw = pd.read_csv(os.path.join(Folder1,file1_input),sep=";")
df_raw_iNPH = df_raw[(df_raw['Group'] == 'QC') | (df_raw['Group'] == 'Gruppe A') | (df_raw['Group'] == 'Gruppe B')].copy()

# Load meta data #

df_meta_data = pd.read_excel(os.path.join(Folder2,file_meta))

## add samples to iNPH ##

df_raw_iNPH['Samples'] = df_raw_iNPH.apply(Sample_anno,axis=1)

# Rearrange columns #

iNPH_cols = list(df_raw_iNPH.columns.values)
list_rearangement = ['Name','Group','Samples']
for key in list_rearangement:
    iNPH_cols.pop(iNPH_cols.index(key))

df_raw_iNPH = df_raw_iNPH[list_rearangement+iNPH_cols]

df_QC =  df_raw_iNPH[(df_raw_iNPH['Group'] == 'QC')]

df_QC_meta = df_QC[['Samples']].copy()
df_QC_meta['Diagnosis'] = 'QC'

# add samples column to meta data #

df_meta_data['Samples'] = df_meta_data.apply(Sample_anno_meta,axis=1)

df_meta_data_apply = df_meta_data[['Samples','Diagnosis']].copy()

df_meta_data_apply_merged = pd.concat([df_QC_meta,df_meta_data_apply],axis=0)

## Correct annotation for samples ##

df_iNPH_full = pd.concat([df_meta_data_apply_merged.set_index('Samples'),df_raw_iNPH.set_index('Samples')],join='inner',axis=1)

# Rearrange columns #

iNPH_cols_full = list(df_iNPH_full.columns.values)
list_rearangement_full = ['Name','Group','Diagnosis']
for key in list_rearangement_full:
    iNPH_cols_full.pop(iNPH_cols_full.index(key))

df_iNPH_full = df_iNPH_full[list_rearangement_full+iNPH_cols_full]
## Save raw iNPH dataframe to file ##

df_iNPH_full.to_excel(os.path.join(Folder1,File_out_1))

df_iNPH = df_iNPH_full.copy()

df_iNPH = df_iNPH.drop(['Name', 'Group'], axis=1)
df_iNPH = df_iNPH.reset_index()

## Save iNPH dataframe ##

df_iNPH.to_excel(os.path.join(Folder1,File_out_2),index=False)

## Transpose and save ##

df_iNPH_T = df_iNPH.T
df_iNPH_T.to_excel(os.path.join(Folder1,File_out_3),header=False)
