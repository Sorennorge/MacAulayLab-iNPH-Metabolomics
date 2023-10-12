# -*- coding: utf-8 -*-

### Create weigted data for enrichment analysis ###

## Need normalized data ## -> coming from a later script ##

import os
import pandas as pd


## Folders ##

Folder1 = "Data/Meta data"
Folder2 = "Data/Normalized data"
Folder3 = "Data/Enrichment data/Control group"
Folder4 = "Data/Enrichment data/Control group & iNPH Weighted"
os.makedirs(Folder4,exist_ok=True)

## Files ##

File1 = "Meta_data_groups.xlsx"
File_norm_Control = "Group Control Normalized data.xlsx"
File_norm_iNPH = "Group iNPH Normalized data.xlsx"
File_norm_Control_wo_outliers = "Group Control Normalized data without outliers.xlsx"
File_norm_iNPH_wo_outliers = "Group iNPH Normalized data without outliers.xlsx"


File_out_1 = "Group Control - Weighted data.xlsx"
File_out_2 = "Group iNPH - Weighted data.xlsx"

File_out_3 = "Group Control - Weighted data without outliers.xlsx"
File_out_4 = "Group iNPH - Weighted data without outliers.xlsx"


## Load color scheme and create color mapping ##
Color_file = "Color_scheme_groups.csv"
df_color = pd.read_csv(os.path.join(Folder1,Color_file),sep=";")
Color_mapping = dict(df_color[['Groups', 'Colors']].values)

## Load meta data ##

df_meta = pd.read_excel(os.path.join(Folder1,File1))
df_meta = df_meta.loc[df_meta['LOI'] == "Yes"]
df_meta_mapping = df_meta[['Compounds','Groups']].set_index('Compounds')

### With outliers ###

## Load data ##

# Group Control #
df_normalized_Control = pd.read_excel(os.path.join(Folder2,File_norm_Control)).rename(columns={"Unnamed: 0":"Samples"}).set_index('Samples')
df_normalized_Control_T = df_normalized_Control.T

# Group iNPH #
df_normalized_iNPH = pd.read_excel(os.path.join(Folder2,File_norm_iNPH)).rename(columns={"Unnamed: 0":"Samples"}).set_index('Samples')
df_normalized_iNPH_T = df_normalized_iNPH.T

## Modify data ##
# Group Control #
df_Control_grouped = pd.concat([df_normalized_Control_T,df_meta_mapping],join="inner",axis=1)
df_Control_sum = df_Control_grouped.groupby('Groups').sum()

# Group iNPH #

df_iNPH_grouped = pd.concat([df_normalized_iNPH_T,df_meta_mapping],join="inner",axis=1)
df_iNPH_sum = df_iNPH_grouped.groupby('Groups').sum()

## Sum data ##

# Group Control #
df_Control_sum['Mean'] = df_Control_sum.mean(axis=1)
df_Control_sum = df_Control_sum.reset_index()

# Group iNPH #
df_iNPH_sum['Mean'] = df_iNPH_sum.mean(axis=1)
df_iNPH_sum = df_iNPH_sum.reset_index()

### Control Group ###
df_Control_sum_sorted_sum = df_Control_sum.sort_values(by=['Mean'],ascending=False,ignore_index=True)
idx_Control = df_Control_sum_sorted_sum.index.tolist()
pop_index_Control = df_Control_sum_sorted_sum.index[df_Control_sum_sorted_sum['Groups']=='Small group collection'].tolist()[0]
idx_Control.pop(pop_index_Control)
df_Control_sum_sorted_sum = df_Control_sum_sorted_sum.reindex(idx_Control+[pop_index_Control]).reset_index(drop=True)
df_Control_sum_sorted_sum.to_excel(os.path.join(Folder4,File_out_1),index=False)

### iNPH Group ###
df_iNPH_sum_sorted_sum = df_iNPH_sum.sort_values(by=['Mean'],ascending=False,ignore_index=True)
idx_iNPH = df_iNPH_sum_sorted_sum.index.tolist()
pop_index_iNPH = df_iNPH_sum_sorted_sum.index[df_iNPH_sum_sorted_sum['Groups']=='Small group collection'].tolist()[0]
idx_iNPH.pop(pop_index_iNPH)
df_iNPH_sum_sorted_sum = df_iNPH_sum_sorted_sum.reindex(idx_iNPH+[pop_index_iNPH]).reset_index(drop=True)
df_iNPH_sum_sorted_sum.to_excel(os.path.join(Folder4,File_out_2),index=False)

### Without outliers ###

## Load data ##

# Group Control #
df_normalized_Control_wo = pd.read_excel(os.path.join(Folder2,File_norm_Control_wo_outliers)).rename(columns={"Sample number":"Samples"}).set_index('Samples')
df_normalized_Control_T_wo = df_normalized_Control_wo.T

# Group iNPH #
df_normalized_iNPH_wo = pd.read_excel(os.path.join(Folder2,File_norm_iNPH_wo_outliers)).rename(columns={"Sample number":"Samples"}).set_index('Samples')
df_normalized_iNPH_T_wo = df_normalized_iNPH_wo.T
## Modify data ##
# Group C #
df_Control_grouped_wo = pd.concat([df_normalized_Control_T_wo,df_meta_mapping],join="inner",axis=1)
df_Control_sum_wo = df_Control_grouped_wo.groupby('Groups').sum()

# Group iNPH #

df_iNPH_grouped_wo = pd.concat([df_normalized_iNPH_T_wo,df_meta_mapping],join="inner",axis=1)
df_iNPH_sum_wo = df_iNPH_grouped_wo.groupby('Groups').sum()

## Sum data ##

# Group Control #
df_Control_sum_wo['Mean'] = df_Control_sum_wo.mean(axis=1)
df_Control_sum_wo = df_Control_sum_wo.reset_index()

# Group iNPH #
df_iNPH_sum_wo['Mean'] = df_iNPH_sum_wo.mean(axis=1)
df_iNPH_sum_wo = df_iNPH_sum_wo.reset_index()

### Control Group ###
df_Control_sum_sorted_sum_wo = df_Control_sum_wo.sort_values(by=['Mean'],ascending=False,ignore_index=True)
idx_Control_wo = df_Control_sum_sorted_sum_wo.index.tolist()
pop_index_Control_wo = df_Control_sum_sorted_sum_wo.index[df_Control_sum_sorted_sum_wo['Groups']=='Small group collection'].tolist()[0]
idx_Control_wo.pop(pop_index_Control_wo)
df_Control_sum_sorted_sum_wo = df_Control_sum_sorted_sum_wo.reindex(idx_Control_wo+[pop_index_Control_wo]).reset_index(drop=True)
df_Control_sum_sorted_sum_wo.to_excel(os.path.join(Folder4,File_out_3),index=False)

### iNPH Group ###
df_iNPH_sum_sorted_sum_wo = df_iNPH_sum_wo.sort_values(by=['Mean'],ascending=False,ignore_index=True)
idx_iNPH_wo = df_iNPH_sum_sorted_sum_wo.index.tolist()
pop_index_iNPH_wo = df_iNPH_sum_sorted_sum_wo.index[df_iNPH_sum_sorted_sum_wo['Groups']=='Small group collection'].tolist()[0]
idx_iNPH_wo.pop(pop_index_iNPH_wo)
df_iNPH_sum_sorted_sum_wo = df_iNPH_sum_sorted_sum_wo.reindex(idx_iNPH_wo+[pop_index_iNPH_wo]).reset_index(drop=True)
df_iNPH_sum_sorted_sum_wo.to_excel(os.path.join(Folder4,File_out_4),index=False)