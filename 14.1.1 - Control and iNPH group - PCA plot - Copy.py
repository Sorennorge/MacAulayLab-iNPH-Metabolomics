# -*- coding: utf-8 -*-

import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt 
import seaborn as sns
sns.set(style="white")
sns.set(style="ticks",font_scale=1.70)

## Folders ##

Folder1 = "Data/PCA data/Raw"
Folder2 = "Results/PCA/Control vs iNPH/TEST"
Folder3= "Data/Meta data"

os.makedirs(Folder2, exist_ok=True)

## Files ##

file_data = "PCA_data.xlsx"
file_targets = "PCA_targets.xlsx"

meta_data_file = "Patient_meta_data.xlsx"

## Load data ##
df_data = pd.read_excel(os.path.join(Folder1,file_data),header=None)

df_targets = pd.read_excel(os.path.join(Folder1,file_targets),header=None)


#### divide into responders and non responders ###

df_meta_data = pd.read_excel(os.path.join(Folder3,meta_data_file))
df_meta_data['Shunt response'] = df_meta_data['Shunt response'].fillna("Control")

responders_mapping = dict(df_meta_data[['Samples', 'Shunt response']].values)

df_targets['modded'] = df_targets[0]
df_targets['modded'] = df_targets['modded'].map(responders_mapping)

# data scaling
x_scaled = StandardScaler().fit_transform(df_data)

# set principal compnents #
n = 10
pca = PCA(n_components=n)

# transport data
pca_features = pca.fit_transform(x_scaled)

columns_n = []
for i in range(1,n+1,1):
    columns_n.append("PC{}".format(i))
# create dataframe with the n PC
pca_df = pd.DataFrame(
    data=pca_features, 
    columns=columns_n)

## Variance for plot 

Variance_PC_array = pca.explained_variance_ratio_

PC_1_V = round(Variance_PC_array[0]*100,2)
PC_2_V = round(Variance_PC_array[1]*100,2)
PC_3_V = round(Variance_PC_array[2]*100,2)
PC_4_V = round(Variance_PC_array[3]*100,2)

pc_list = [PC_1_V,PC_2_V,PC_3_V,PC_4_V]
# map target names to PCA features   

pca_df['Target'] = df_targets['modded']

# PC settings #
x_pc = 1
y_pc = 2

File_out = "TEST_PCA_plot_PC{}_PC{}.png".format(x_pc,y_pc)
plt.figure(figsize=(20,20))
sns.lmplot(
    x='PC{}'.format(x_pc), 
    y='PC{}'.format(y_pc), 
    data=pca_df, 
    hue='Target', 
    fit_reg=False, 
    legend=True,
    palette=["teal",'red',"white"],
    scatter_kws={'linewidths':1,'edgecolor':'k','s':100}
    )
sns.despine(top=False, right=False, left=False, bottom=False)
plt.xticks([-20,-10,0,10,20,30])
plt.yticks([-10,-5,0,5,10,15,20,25])
plt.xlabel( "PC {} ({} %)".format(x_pc,pc_list[x_pc-1]))
plt.ylabel( "PC {} ({} %)".format(y_pc,pc_list[y_pc-1]))
plt.savefig(os.path.join(Folder2,File_out),dpi=600,bbox_inches='tight')
plt.show()
