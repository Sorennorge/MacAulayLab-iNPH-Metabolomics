# -*- coding: utf-8 -*-

### Generate PCA plots (Supplementary for each group) ###

## Libraries ##

import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt 
import seaborn as sns

sns.set(style="white")
sns.set(style="ticks",font_scale=1.60)

## Folders ##
Folder1 = "Data/Meta data"
Folder2 = "Data/PCA data/Raw"
Folder3 = "Data/Normalized data"
Folder4 = "Data/Enrichment data/Control group"

Folder5 = "Results/PCA/Control vs iNPH/Individual groups"
os.makedirs(Folder5,exist_ok=True)

## Files ##

File1 = "Meta_data_groups.xlsx"
File2 = "PCA_targets.xlsx"
File3 = "Group Control Normalized data.xlsx"
File3_2 = "Group iNPH Normalized data.xlsx"
File4 = "Enrichement_data_all_group_Control.csv"

## Load data ##

df_groups = pd.read_excel(os.path.join(Folder1,File1))

df_metadata = pd.read_excel(os.path.join(Folder2,File2),header=None)
df_metadata = df_metadata.rename(columns={0:"Sample number",1:"Target"})

df_data1 = pd.read_excel(os.path.join(Folder3,File3))
df_data1 = df_data1.rename(columns={'Unnamed: 0':"Sample number"})
df_data2 = pd.read_excel(os.path.join(Folder3,File3_2))
df_data2 = df_data2.rename(columns={'Unnamed: 0':"Sample number"})
df_data = pd.concat([df_data1, df_data2], ignore_index=True)


df_data = df_data.set_index("Sample number")
df_data_T = df_data.T
sample_list = df_data_T.columns.tolist()

# Enrichment data
df_enrichment_data_all =  pd.read_csv(os.path.join(Folder4,File4),sep=";")

# Reduce groups to group with more than one count #
df_enrichment_data_all = df_enrichment_data_all.loc[df_enrichment_data_all['Count'] > 1]

# Create lists of groups for age plots #
Group_list_all = df_enrichment_data_all['Groups'].tolist()

## Add groups to data and reduce dataframe  ##
# Create mapping directory #
Group_mapping = dict(df_groups[['Compounds', 'Groups']].values)
# add groups to dataframe #
df_data_T['Groups'] = df_data_T.index.map(Group_mapping)

## Plot PCA for each group ##

for Group in Group_list_all:
    try:
        df_data_plot = df_data_T[df_data_T['Groups'] == Group]
        del df_data_plot['Groups']
        df_data_plot_T = df_data_plot.T
        pca_data = df_data_plot_T.values
        
        # data scaling
        x_scaled = StandardScaler().fit_transform(pca_data)
        
        pca = PCA(n_components=2)
        
        pca_features = pca.fit_transform(x_scaled)
        
        pca_df = pd.DataFrame(
            data=pca_features, 
            columns=['PC1','PC2'])
        
        Variance_PC_array = pca.explained_variance_ratio_
        
        PC_1_V = round(Variance_PC_array[0]*100,2)
        PC_2_V = round(Variance_PC_array[1]*100,2)
        
        pca_df['Groups'] = df_metadata['Target']
        pca_df['Values'] = df_metadata['Sample number']
        
        print("Creating age plot with legend...")
        # With legend
        plt.figure(figsize=(20,20))
        sns.lmplot(
            x='PC1', 
            y='PC2', 
            data=pca_df, 
            hue='Groups', 
            fit_reg=False, 
            legend=False,
            palette=["Teal","White"],
            scatter_kws={'linewidths':1,'edgecolor':'k','s':100}
            )
        plt.title("{}".format(Group))
        plt.xlabel( "PC 1 ({} %)".format(PC_1_V))
        plt.ylabel( "PC 2 ({} %)".format(PC_2_V))
        plt.locator_params(axis='both', nbins=6)
        sns.despine(top=False, right=False, left=False, bottom=False)
        print("Saving age plot with legend...")
        filename = "PCA_group_{}.png".format(Group)
        plt.savefig(os.path.join(Folder5,filename),dpi=600,bbox_inches='tight')
        print("Done.")
        plt.show()
    except:
        print("Did not manage to create:")
        print(Group)
