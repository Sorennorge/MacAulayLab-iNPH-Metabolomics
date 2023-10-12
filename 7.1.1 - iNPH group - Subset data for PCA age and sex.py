# -*- coding: utf-8 -*-

import os
import pandas as pd
import numpy as np

# Folders #

Folder1 = "Data/Normalized data"
Folder2 = "Data/Lookup data"
Folder3 = "Data/Meta data"

Folder4 = "Data/Meta data/iNPH group"
os.makedirs(Folder4,exist_ok=True)

Folder5 = "Data/PCA data/Sex/iNPH"
os.makedirs(Folder5,exist_ok=True)
Folder6 = "Data/PCA data/Age/iNPH"
os.makedirs(Folder6,exist_ok=True)


## Files ##

File1 = "Group iNPH Normalized data.xlsx"
File2 = "Patient_meta_data.xlsx"

# Output #
File4 = "Metadata_iNPH_group_overview.csv"

PCA_sex_data = "PCA_data_sex.csv"
PCA_sex_targets = "PCA_targets_sex.csv"
PCA_age_data = "PCA_data_age.csv"
PCA_age_targets = "PCA_targets_age.csv"

## Read raw data ##

# Read data #
df_normalized = pd.read_excel(os.path.join(Folder1,File1)).rename(columns=({"Unnamed: 0":"Samples"})).set_index("Samples")
df_normalized_T = df_normalized.T


# Create lists of samples 
Group_iNPH_list = df_normalized_T.columns.values.tolist()

## Load metadata ##
df_meta_data = pd.read_excel(os.path.join(Folder3,File2))
# Create metadata mapping dicts
Sex_mapping = dict(df_meta_data[['Samples', 'Sex']].values)
Age_mapping = dict(df_meta_data[['Samples', 'Age']].values)


## Create meta data overview as dataframe (for PCA targets) ##

Meta_data_overview = df_normalized.reset_index()[['Samples']]

# Add sex to the overview (and PCA target) #
Meta_data_overview['Sex'] = Meta_data_overview['Samples'].map(Sex_mapping)
Meta_data_overview['Sex targets'] = np.where(Meta_data_overview['Sex'] == "Female", 0, 1)

# Add Age to the overview (and PCA target) #
Meta_data_overview['Age'] = Meta_data_overview['Samples'].map(Age_mapping)

# Age split #
Age_split = Meta_data_overview['Age'].median()
# or set manual #
#Age_split = 60

# add targets #
Meta_data_overview['Age targets'] = np.where(Meta_data_overview['Age'] < Age_split, 1, 0)
Meta_data_overview = Meta_data_overview.set_index('Samples')

# Save overview data #
Meta_data_overview.to_csv(os.path.join(Folder4,File4),sep=";")

## Save normalized PCA data ##
# Sex PCA #
df_normalized_T.to_csv(os.path.join(Folder5,PCA_sex_data),index=False,header=False,sep=";")
Meta_data_overview[['Sex','Sex targets']].to_csv(os.path.join(Folder5,PCA_sex_targets),sep=";")
# Age PCA #
df_normalized_T.to_csv(os.path.join(Folder6,PCA_age_data),index=False,header=False,sep=";")
Meta_data_overview[['Age','Age targets']].to_csv(os.path.join(Folder6,PCA_age_targets),sep=";")
