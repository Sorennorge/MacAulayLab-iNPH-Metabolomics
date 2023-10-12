# -*- coding: utf-8 -*-

### PCA - Normalized ###

import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt 
import seaborn as sns
sns.set(style="white")
sns.set(style="ticks",font_scale=1.70)

## Settings ##

save_files = "Yes"
#save_files = "no"

# Functions #

def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x']+.4, point['y'], str(point['val']))

## Folders ##
folder1 = "Data/PCA data/Responders/iNPH"
folder2 = "Results/PCA/Responders/iNPH"

os.makedirs(folder2,exist_ok=True)

## Files ##

PCA_Responders_data = "PCA_data_Responders.csv"
PCA_Responders_targets = "PCA_targets_Responders.csv"

PCA_Responders_legend = "PCA_Responders_with_legend.png"
PCA_Responders_nolegend = "PCA_Responders_without_legend.png"

## Load data ##

df_data = pd.read_csv(os.path.join(folder1,PCA_Responders_data),sep=";",header=None)
df_data = df_data.T

df_targets = pd.read_csv(os.path.join(folder1,PCA_Responders_targets),sep=";")

# data scaling
x_scaled = StandardScaler().fit_transform(df_data)

pca = PCA(n_components=4)

pca_features = pca.fit_transform(x_scaled)

pca_df = pd.DataFrame(
    data=pca_features, 
    columns=['PC1', 'PC2','PC3','PC4'])

## Variance for plot 

Variance_PC_array = pca.explained_variance_ratio_

PC_1_V = round(Variance_PC_array[0]*100,2)
PC_2_V = round(Variance_PC_array[1]*100,2)
PC_3_V = round(Variance_PC_array[2]*100,2)

# map target names to PCA features   
target_names = {
    1:'Non-responder',
    0:'Responder'
}

pca_df['Response'] = df_targets['Shunt response targets']
pca_df['Response'] = pca_df['Response'].map(target_names)
pca_df['Values'] = df_targets['Samples']

print("Creating age plot with legend...")
# With legend
plt.figure(figsize=(20,20))
sns.lmplot(
    x='PC1', 
    y='PC2', 
    data=pca_df, 
    hue='Response', 
    fit_reg=False, 
    legend=True,
    palette=["red","Teal"],
    scatter_kws={'linewidths':1,'edgecolor':'k','s':100}
    )
plt.xlabel( "PC 1 ({} %)".format(PC_1_V))
plt.ylabel( "PC 2 ({} %)".format(PC_2_V))
plt.xticks([-20,-10,0,10,20])
plt.yticks([-10,0,10,20])
sns.despine(top=False, right=False, left=False, bottom=False)
#plt.show()
print("Saving age plot with legend...")
if save_files == "Yes":
    plt.savefig(os.path.join(folder2,PCA_Responders_legend),dpi=600,bbox_inches='tight')
else:
    plt.show()
print("Done.")


print("Creating age plot without legend...")
# Without legend
plt.figure(figsize=(20,20))
sns.lmplot(
    x='PC1', 
    y='PC2', 
    data=pca_df, 
    hue='Age', 
    fit_reg=False, 
    legend=False,
    palette=["#EAEAEA","#777777"],
    scatter_kws={'linewidths':1,'edgecolor':'k','s':100}
    )
plt.xlabel( "PC 1 ({} %)".format(PC_1_V))
plt.ylabel( "PC 2 ({} %)".format(PC_2_V))
plt.xticks([-20,-10,0,10,20])
plt.yticks([-10,0,10,20])
sns.despine(top=False, right=False, left=False, bottom=False)
print("Saving age plot without legend...")
if save_files == "Yes":
    plt.savefig(os.path.join(folder2,PCA_Responders_nolegend),dpi=600,bbox_inches='tight')
else:
    plt.show()
print("Done. Enjoy.")