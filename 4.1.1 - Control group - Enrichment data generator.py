# -*- coding: utf-8 -*-

### Collect group data for enrichement plot analysis ###

## Libraries ##

import os
import pandas as pd

## Folders ##

Folder1 = "Data/Meta data"
Folder2 = "Data/Data cleaning"
Folder3 = "Data/Enrichment data/Control group"

os.makedirs(Folder3,exist_ok=True)

## Files ##

File1 = "Meta_data_groups.xlsx"
File2 = "raw_data_QC_iNPH_Control.xlsx"

File3 = "Enrichement_data_all_group_Control.csv"

## Read group list - all Compounds ##
# Read data #
df_groups_Compounds = pd.read_excel(os.path.join(Folder1,File1))
# List of interest #
df_groups_Compounds_of_interest = df_groups_Compounds.loc[df_groups_Compounds['LOI'] == "Yes"]
# Create mapping directory #
metabolite_mapping = dict(df_groups_Compounds[['Compounds', 'Groups']].values)

## Read all metabolite entries ##

# Read data #
df_Compounds = pd.read_excel(os.path.join(Folder2,File2)).rename(columns=({'Unnamed: 0':"Compounds"}))

## exclude non-lipids ##

df_Compounds = df_Compounds[df_Compounds["Compounds"].isin(df_groups_Compounds_of_interest["Compounds"])]

# Create list of Compounds #
Metabolite_list = df_Compounds['Compounds'].tolist()
# Create new dataframe with all Compounds #
df_metabolite_with_groups = pd.DataFrame({'Compounds': Metabolite_list})
# Map groups to Compounds #
df_metabolite_with_groups['Groups'] = df_metabolite_with_groups.Compounds.map(metabolite_mapping)


# Create dataframe of group counts #
df_Enrichment_all = df_metabolite_with_groups.groupby('Groups').count().rename(columns={'Compounds':'Count'}).reset_index()
# extract specific entries from the enrichment data to later be placed at the bottom #
# Sort by counts #
df_Enrichment_all_sorted = df_Enrichment_all.sort_values(by=['Count'],ascending=False,ignore_index=True)

## Reindex small metabolite group to last followed by others ##

idx = df_Enrichment_all_sorted.index.tolist()
pop_index = df_Enrichment_all_sorted.index[df_Enrichment_all_sorted['Groups']=='Small group collection'].tolist()[0]
idx.pop(pop_index)
df_Enrichment_all_sorted = df_Enrichment_all_sorted.reindex(idx+[pop_index])

## Save enrichment data files ##

df_Enrichment_all_sorted.to_csv(os.path.join(Folder3,File3),sep=";",index=False)
