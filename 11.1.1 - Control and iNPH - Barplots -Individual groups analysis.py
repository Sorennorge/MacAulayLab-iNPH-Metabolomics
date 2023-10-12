# -*- coding: utf-8 -*-

### Bar plot data analysis ### 

## Libraries ##

import os
import pandas as pd
import statsmodels.stats.multitest as smt

## Folders ##

## Folders ##
Folder1 = "Data/Meta data"
Folder2 = "Data/Data analysis"
Folder3 = "Data/Enrichment data/Control group"
Folder4 = "Results/Bar plots"
os.makedirs(Folder4,exist_ok=True)

## Files ##

File1 = "Meta_data_groups.xlsx"
File2 = "Data analysis overview.xlsx"
File3 = "Enrichement_data_all_group_Control.csv"
File4 = "Barplot data for individual groups.xlsx"

## Load data ##

df_groups = pd.read_excel(os.path.join(Folder1,File1))
df_overview = pd.read_excel(os.path.join(Folder2,File2))

## Reduce overview data ##
df_overview_reduced = df_overview[['Compounds','Log2FC','Pvalue']].copy()

## Add groups to data and reduce dataframe  ##
# Create mapping directory #
Group_mapping = dict(df_groups[['Compounds', 'Groups']].values)
# add groups to dataframe #
df_overview_reduced['Groups'] = df_overview_reduced.Compounds.map(Group_mapping)

## create group list for groups of interest ##
df_enrichment_data_interest =  pd.read_csv(os.path.join(Folder3,File3),sep=";")
# Reduce groups to group with more than one count #
df_enrichment_data_interest = df_enrichment_data_interest.loc[df_enrichment_data_interest['Count'] > 1]
# Create group list of interest #
Group_list_interest = df_enrichment_data_interest['Groups'].tolist()

## Create the new dataframe with individual groups for padj## 

df_individual_overview = pd.DataFrame(columns=df_overview_reduced.columns.values.tolist()+['Padj'])

for Group in Group_list_interest:
    # Reduce to only one group #
    df_individual_group = df_overview_reduced[df_overview_reduced['Groups'] == Group].copy()
    # add adjusted pvalue #
    df_individual_group['Padj'] = smt.fdrcorrection(df_individual_group['Pvalue'],alpha=0.05,method="indep")[1]
    # Drop all over significance #
    df_individual_group.drop(df_individual_group[df_individual_group.Padj >= 0.05].index, inplace=True)
    # Append to overview dataframe #
    df_individual_overview = pd.concat([df_individual_overview,df_individual_group],ignore_index=True)

df_individual_overview = df_individual_overview[['Compounds','Groups','Log2FC','Pvalue','Padj']]

df_individual_overview.to_excel(os.path.join(Folder4,File4),sheet_name="Overview",index=False)