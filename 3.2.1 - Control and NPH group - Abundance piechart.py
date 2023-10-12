# -*- coding: utf-8 -*-

### Abundance piecharts ###

## Libraries ##

import os
import pandas as pd
import matplotlib.pyplot as plt

font_size = 24

## Function ##
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = pct*total/100.0
        return '{:.1f}%\n({v:.2f})'.format(pct, v=val)
    return my_format

## Folders ##

Folder_0 = "Data/Meta data"

Folder_1 = "Data/Enrichment data/Control group & iNPH Weighted"
Folder_2 = "Results/Enrichement Analysis/Abundance"
os.makedirs(Folder_2,exist_ok=True)

Color_file = "Color_scheme_groups.csv"

## Files ##

File_1 = "Group Control - Weighted data without outliers.xlsx"
File_2 = "Group iNPH - Weighted data without outliers.xlsx"

File_out_1 = "Abundance piechart - group Control.png"
File_out_2 = "Abundance piechart - group iNPH.png"

## Load data ##

## Load color scheme and create color mapping ##

df_color = pd.read_csv(os.path.join(Folder_0,Color_file),sep=";")
Color_mapping = dict(df_color[['Groups', 'Colors']].values)

# Data #
df_Control = pd.read_excel(os.path.join(Folder_1,File_1))
df_iNPH = pd.read_excel(os.path.join(Folder_1,File_2))

## Create variables for plots ##

data_all_Control = df_Control['Mean']
labels_all_Control = df_Control['Groups']

data_all_iNPH = df_iNPH['Mean']
labels_all_iNPH = df_iNPH['Groups']

## Create color palettes for plots #
color_all_Control = labels_all_Control.to_frame().replace({"Groups": Color_mapping})['Groups'].tolist()
color_all_iNPH = labels_all_iNPH.to_frame().replace({"Groups": Color_mapping})['Groups'].tolist()

explode_set_all_Control = [0.15]*len(color_all_Control)
explode_set_all_iNPH = [0.15]*len(color_all_iNPH)


print("Creating enrichment plot for all Compounds - Group Control")
plt.figure(figsize=(20,20))
plt.pie(data_all_Control, labels = labels_all_Control,
        colors = color_all_Control,
        explode=explode_set_all_Control,
        autopct=autopct_format(data_all_Control),
        textprops={'fontsize': font_size},
        wedgeprops = {"edgecolor":"black",'linewidth': 1.2,"alpha": 0.65},
        counterclock=False,
        startangle=90,
        pctdistance=1.2,
        labeldistance=1.3)
print("Saving plot...")
plt.savefig(os.path.join(Folder_2,File_out_1),dpi=600,bbox_inches='tight')
plt.show()
print("Done.")

print("Creating enrichment plot for all Compounds - Group iNPH")
plt.figure(figsize=(20,20))
plt.pie(data_all_iNPH, labels = labels_all_iNPH,
        colors = color_all_iNPH,
        explode=explode_set_all_iNPH,
        autopct=autopct_format(data_all_iNPH),
        textprops={'fontsize': font_size},
        wedgeprops = {"edgecolor":"black",'linewidth': 1.2,"alpha": 0.65},
        counterclock=False,
        startangle=90,
        pctdistance=1.2,
        labeldistance=1.3)
print("Saving plot...")
plt.savefig(os.path.join(Folder_2,File_out_2),dpi=600,bbox_inches='tight')
plt.show()
print("Done.")