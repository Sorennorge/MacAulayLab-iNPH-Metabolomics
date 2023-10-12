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

Folder5 = "Data/PCA data/Responders/iNPH"
os.makedirs(Folder5,exist_ok=True)
Folder6 = "Data/PCA data/Responders/iNPH"
os.makedirs(Folder6,exist_ok=True)


## Files ##

File1 = "Normalized data for group iNPH and Control.xlsx"
File2 = "Patient_meta_data.xlsx"

# Output #
#File4 = "Metadata_iNPH_group_overview.csv"

PCA_responders_data = "PCA_data_responders.csv"
PCA_responders_targets = "PCA_targets_responders.csv"


## Read raw data ##

# Read data #
df_normalized = pd.read_excel(os.path.join(Folder1,File1)).rename(columns=({"Unnamed: 0":"Samples"})).set_index("Samples")
df_normalized_T = df_normalized.T


# Create lists of samples 
Group_iNPH_list = df_normalized_T.columns.values.tolist()

## Load metadata ##
df_meta_data = pd.read_excel(os.path.join(Folder3,File2))
# Create metadata mapping dicts
responders_mapping = dict(df_meta_data[['Samples', 'Shunt response']].values)

## Create meta data overview as dataframe (for PCA targets) ##

Meta_data_overview = df_normalized.reset_index()[['Samples']]
# Add sex to the overview (and PCA target) #
Meta_data_overview['Shunt response'] = Meta_data_overview['Samples'].map(responders_mapping)
Meta_data_overview['Shunt response targets'] = np.where(Meta_data_overview['Shunt response'] == "Responder", 0, 1)
# Add Age to the overview (and PCA target) #
Meta_data_overview = Meta_data_overview.set_index('Samples')

## Save normalized PCA data ##
# Responders PCA #
df_normalized_T.to_csv(os.path.join(Folder5,PCA_responders_data),index=False,header=False,sep=";")
Meta_data_overview[['Shunt response','Shunt response targets']].to_csv(os.path.join(Folder5,PCA_responders_targets),sep=";")