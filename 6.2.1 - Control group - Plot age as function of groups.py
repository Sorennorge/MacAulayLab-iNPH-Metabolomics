# -*- coding: utf-8 -*-

### Plot ages as function of groups ###

import os
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

## Folders ##

Folder1 = "Data/Plot data/Age vs groups/all groups"
Folder2 = "Results/Age plots/All groups"
Folder3 = "Data/Meta data"

os.makedirs(Folder2,exist_ok=True)

## Files ##

File1 = "Age_data_all.csv"
File2 = "Age_data_interest.csv"

File3 = "Age_data_all_dot_transp.png"

## load Color scheme ##
Color_file = "Color_scheme_groups.csv"
df_color = pd.read_csv(os.path.join(Folder3,Color_file),sep=";")
Color_mapping = dict(df_color[['Groups', 'Colors']].values)

## Styles ##
sns.set(style="white")
sns.set(style="ticks",font_scale=1.70)

## Load data ##

df_data_all = pd.read_csv(os.path.join(Folder1,File1),sep=";",header=0)
#df_data_interest = pd.read_csv(os.path.join(Folder1,File2),sep=";",header=0)

## color scheme ##
colors_all = df_data_all['Groups'].drop_duplicates().replace(Color_mapping).tolist()

# ticks #
age_list = df_data_all['Age'].unique().tolist()

## Plot data ##
# All groups #

plt.figure(figsize=(14,8))
ax1 = sns.lineplot(data=df_data_all, x="Age",
                   y="Values",alpha=0.75,palette=colors_all,
                   hue="Groups",style="Groups",markers=True, dashes=False, markersize=10)
sns.move_legend(ax1, "upper left", bbox_to_anchor=(1, 1))
plt.title('Lipid groups as a function of age')
plt.xlabel( "Age")
plt.ylabel( "Lipid abundance")
plt.xticks(age_list)
#plt.xlim([])
plt.ylim([0,2])
plt.yticks([0,0.5,1,1.5,2])
plt.savefig(os.path.join(Folder2,File3),dpi=600,bbox_inches='tight',transparent=True)
plt.show()
