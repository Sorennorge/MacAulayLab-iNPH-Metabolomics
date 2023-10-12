# -*- coding: utf-8 -*-

### Enrichment plots ###

## Libraries ##

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#import matplotlib.colors
sns.set(font_scale=2)
sns.set_style("white")
## functions ##

def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{:.1f}%\n({v:d})'.format(pct, v=val)
    return my_format

# global variables #

font_size = 24

## Folders ##

Folder1 = "Data/Enrichment data/Control group"
Folder2 = "Results/Enrichement Analysis/Control group"
Folder3 = "Data/Meta data"

os.makedirs(Folder2,exist_ok=True)
    
## Files ##

File1 = "Enrichement_data_all_group_Control.csv"


File3 = "Enrichment_plot_all_percent_exploded.png"

## Load color scheme and create color mapping ##
Color_file = "Color_scheme_groups.csv"
df_color = pd.read_csv(os.path.join(Folder3,Color_file),sep=";")
Color_mapping = dict(df_color[['Groups', 'Colors']].values)

## Load data ##

# All metabolite groups ##
df_all = pd.read_csv(os.path.join(Folder1,File1),sep=";")

## Create plot data ##
# Variables #
data_all = df_all['Count']
labels_all = df_all['Groups']

## Create color palettes for plots #
color_all = labels_all.to_frame().replace({"Groups": Color_mapping})['Groups'].tolist()

color_palette = sns.color_palette(color_all)

## Set exploded set ##

explode_set_all = [0.15]*len(color_all)

# plot data #
print("Creating enrichment plot for all Compounds")
plt.figure(figsize=(10,10))
ax = sns.barplot(data=df_all, x = 'Groups',y = 'Count', hue='Groups',palette=color_palette,alpha=0.75,dodge=False)
        #explode=explode_set_all,
        #autopct=autopct_format(data_all),
        #textprops={'fontsize': font_size},
        #wedgeprops = {"edgecolor":"black",'linewidth': 1.2,"alpha": 0.65},
        #counterclock=False,
        #startangle=90,
        #pctdistance=1.2,
        #labeldistance=1.3)
sns.despine(top=True, right=True, left=True, bottom=True)
plt.ylabel('Lipid count')
plt.xlabel('')
plt.yticks([])
ax.legend([],[], frameon=False)
for i in ax.containers:
    ax.bar_label(i,)
ticks = []
for i in range(0,len(labels_all),1):
    ticks.append(i)
ax.set_xticks(ticks, labels_all,rotation=45, ha='right', rotation_mode='anchor')

print("Saving plot...")
plt.savefig(os.path.join(Folder2,File3),dpi=600,bbox_inches='tight',transparent=True)
plt.show()
print("Done.")