# -*- coding: utf-8 -*-

### Generate data for age function plots ###

## Libraries ##

import os
import pandas as pd

## Folders ##

Folder1 = "Data/Meta data"
Folder2 = "Data/Meta data/Control group"
Folder3 = "Data/Normalized data"
Folder4 = "Data/Enrichment data/Control group"

Folder5 = "Data/Plot data/Age vs groups/all groups"
os.makedirs(Folder5,exist_ok=True)

## Files ##

File1 = "Meta_data_groups.xlsx"
File2 = "Metadata_control_group_overview.csv"
File3 = "Group Control Normalized data.xlsx"
#File3 = "Group Control Normalized data without outliers.xlsx"
File4 = "Enrichement_data_all_group_C.csv"

File6 = "Age_data_all.csv"

## Load data ##

df_groups = pd.read_excel(os.path.join(Folder1,File1))

df_metadata = pd.read_csv(os.path.join(Folder2,File2),sep=";")

df_data = pd.read_excel(os.path.join(Folder3,File3))
df_data = df_data.rename(columns={'Unnamed: 0':"Samples"})
#df_data = df_data.rename(columns={'Sample number':"Samples"})

df_data = df_data.set_index("Samples")
df_data_T = df_data.T
sample_list = df_data_T.columns.tolist()

df_employ = df_groups.loc[df_groups['LOI'] == "Yes"]
Group_mapping = dict(df_employ[['Compounds', 'Groups']].values)
df_data_T['Groups'] = df_data_T.index.map(Group_mapping)

## Create dataframe of samples with mean of groups ##
df_mean_all = df_data_T.groupby(['Groups'])[sample_list].mean()

## Create age data for group as function of age plot ##
Age_mapping = dict(df_metadata[['Samples', 'Age']].values)
Age_data_all = df_mean_all.T.reset_index()
Age_data_all = Age_data_all.rename(columns={"Samples":'Age'}).replace({'Age':Age_mapping}).set_index('Age')
# Move "Small group collection" to the end #
col_list_age_all = list(Age_data_all.columns.values)
col_list_age_all.pop(col_list_age_all.index('Small group collection'))
Age_data_all = Age_data_all[col_list_age_all+['Small group collection']]
Age_data_all_cols = list(Age_data_all.columns.values)
Age_data_all_mean = Age_data_all.groupby(['Age'])[Age_data_all_cols].mean()
Age_data_all_stacked = Age_data_all_mean.stack().to_frame().rename(columns={0:'Values'})


## Save age plot data ##

Age_data_all_stacked.to_csv(os.path.join(Folder5,File6),sep=";")
