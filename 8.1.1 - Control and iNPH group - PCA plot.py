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
Folder2 = "Results/PCA/Control vs iNPH"

os.makedirs(Folder2, exist_ok=True)

## Files ##

file_data = "PCA_data.xlsx"
file_targets = "PCA_targets.xlsx"

## Load data ##
df_data = pd.read_excel(os.path.join(Folder1,file_data),header=None)

df_targets = pd.read_excel(os.path.join(Folder1,file_targets),header=None)

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

pca_df['Target'] = df_targets[1]


plt.figure(figsize=(20,20))
sns.lmplot(
    x='PC1', 
    y='PC2', 
    data=pca_df, 
    hue='Target', 
    fit_reg=False, 
    legend=True,
    palette=["teal","white"],
    scatter_kws={'linewidths':1,'edgecolor':'k','s':100}
    )
sns.despine(top=False, right=False, left=False, bottom=False)
plt.xlabel( "PC 1 ({} %)".format(PC_1_V))
plt.ylabel( "PC 2 ({} %)".format(PC_2_V))
plt.xticks([-15,-5,5,15,25,35])

# Setting -> Principal components #
x_pc = 1
y_pc = 2

File_out = "PCA_plot_PC{}_PC{}.png".format(x_pc,y_pc)
plt.figure(figsize=(20,20))
sns.lmplot(
    x='PC{}'.format(x_pc), 
    y='PC{}'.format(y_pc), 
    data=pca_df, 
    hue='Target', 
    fit_reg=False, 
    legend=True,
    palette=["teal","white"],
    scatter_kws={'linewidths':1,'edgecolor':'k','s':100}
    )
sns.despine(top=False, right=False, left=False, bottom=False)
plt.xticks([-20,-10,0,10,20,30])
plt.yticks([-10,-5,0,5,10,15,20,25])
plt.xlabel( "PC {} ({} %)".format(x_pc,pc_list[x_pc-1]))
plt.ylabel( "PC {} ({} %)".format(y_pc,pc_list[y_pc-1]))
plt.savefig(os.path.join(Folder2,File_out),dpi=600,bbox_inches='tight')
plt.show()
