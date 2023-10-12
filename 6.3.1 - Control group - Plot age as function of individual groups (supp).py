# -*- coding: utf-8 -*-

## Libraries ##

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.cm import register_cmap

## Folders ##

Folder1 = "Data/Meta data"
Folder2 = "Data/Meta data/Control group"
Folder3 = "Data/Normalized data"
Folder4 = "Data/Enrichment data/Control group"

Folder5 = "Results/Age plots/Individual groups"
os.makedirs(Folder5,exist_ok=True)
Folder6 = "Data/Meta data/cmap colors"
os.makedirs(Folder6,exist_ok=True)

## Files ##

File1 = "Meta_data_groups.xlsx"
File2 = "Metadata_control_group_overview.csv"
File3 = "Group Control Normalized data.xlsx"
File4 = "Enrichement_data_all_group_Control.csv"

File6 = "Color_scheme_groups.csv"

## Load data ##

df_groups = pd.read_excel(os.path.join(Folder1,File1))

df_metadata = pd.read_csv(os.path.join(Folder2,File2),sep=";")

df_colors = pd.read_csv(os.path.join(Folder1,File6),sep=";")

Metabolite_color_dict = df_colors.set_index('Groups')['Colors'].to_dict()

# Create mapping directory #
Group_mapping = dict(df_groups[['Compounds', 'Groups']].values)
Age_mapping = dict(df_metadata[['Samples', 'Age']].values)

df_data = pd.read_excel(os.path.join(Folder3,File3))
df_data = df_data.rename(columns={'Unnamed: 0':"Samples"})
#Rename samples to age #
df_data = df_data.set_index("Samples")
df_data = df_data.reset_index().rename(columns={"Samples":'Age'}).replace({'Age':Age_mapping}).set_index('Age')

# take the mean of samples with the same age #
Age_data_interst_cols = list(df_data.columns.values)

df_data_mean = df_data.reset_index().groupby(['Age'])[Age_data_interst_cols].mean()

df_data_T = df_data_mean.T
sample_list = df_data_T.columns.tolist()
# Enrichment data
df_enrichment_data_interest =  pd.read_csv(os.path.join(Folder4,File4),sep=";")
# Reduce groups to group with more than one count #

df_enrichment_data_interest = df_enrichment_data_interest.loc[df_enrichment_data_interest['Count'] > 1]
# Create lists of groups for age plots #
Group_list_interest = df_enrichment_data_interest['Groups'].tolist()

## Add groups to data and reduce dataframe  ##

# add groups to dataframe #
df_data_T['Groups'] = df_data_T.index.map(Group_mapping)

# For each group 

## Mean plot ##
for Group in Group_list_interest:
    try:
        plt.figure(figsize=(14,8))
        print("Creating data for {}".format(Group))
        df_data_plot = df_data_T[df_data_T['Groups'] == Group]
        del df_data_plot['Groups']
        
        df_data_plot_T = df_data_plot.T
        df_data_plot_T_stacked = df_data_plot_T.stack().to_frame().reset_index().rename(columns={0:'Values',"level_1":"Compounds"})
        color_palette = [Metabolite_color_dict[Group]]*len(df_data_plot.index)
        ax = sns.lineplot(data=df_data_plot_T_stacked,
                          x="Age",
                          y="Values",
                          color=Metabolite_color_dict[Group],
                          marker="o",
                          markersize=10,
                          legend=None)
        plt.title('{} as a function of age'.format(Group))
        plt.xlabel( "Age")
        plt.xticks(sample_list)
        plt.ylim([0,2])
        plt.yticks([0,0.5,1,1.5,2])
        plt.ylabel("Lipid abundance")
        file_name = "Mean - {} vs age.png".format(Group)
        print("Creating plot...")
        plt.savefig(os.path.join(Folder5,file_name),dpi=600,bbox_inches='tight')
        plt.show()
        print("Done.")
    except:
        print("Error occurred: {}".format(Group))
