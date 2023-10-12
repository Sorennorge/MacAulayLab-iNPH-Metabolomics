# -*- coding: utf-8 -*-

### Bar chart group C and D ###

## Libraries ##

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy
from scipy import stats
sns.set(font_scale=2)
sns.set_style("white")

## Folders ##
Folder1 = "Data/Enrichment data/Control group & iNPH Weighted"
Folder2 = "Results/Abundance/Group barplot"
os.makedirs(Folder2,exist_ok=True)

## Files ##
File1 = "Group Control - Weighted data without outliers.xlsx"
File2 = "Group iNPH - Weighted data without outliers.xlsx"
bar_file = "Abundance bar plot control vs iNPH.png"
overview_file = "Bar chart overview control vs iNPH.xlsx"

## load data ##

df_c = pd.read_excel(os.path.join(Folder1,File1))
df_c = df_c.drop(['Mean'], axis=1)
df_c_T = df_c.set_index('Groups').T
df_c_T['mean'] = df_c_T.mean(axis=1)


df_c_mean = df_c_T['mean'].to_frame()
df_c_mean['Group'] = "Control"
    
df_d = pd.read_excel(os.path.join(Folder1,File2))
df_d = df_d.drop(['Mean'], axis=1)
df_d_T = df_d.set_index('Groups').T
df_d_T['mean'] = df_d_T.mean(axis=1)

df_d_mean = df_d_T['mean'].to_frame()
df_d_mean['Group'] = "iNPH"

df_data = pd.concat([df_c_mean,df_d_mean],ignore_index=True)

# Create figures #
plt.figure(figsize=(8,8))
p1 = sns.barplot(data=df_data, x="Group", y="mean",
                 hue="Group",palette = ['grey','darkred'],estimator=np.mean,ci = 68) #bootstrap ci 68% is SEM
plt.xticks([])
plt.ylabel('Lipid abundance')
plt.xlabel('')
plt.title("Control vs iNPH Lipid abundance")
p1.legend_.set_title(None)
plt.ylim([0,30])
sns.despine(top=True, right=True, left=False, bottom=True)
p1.axhline(y=0.0,color='black',linewidth=2)
plt.savefig(os.path.join(Folder2,bar_file),dpi=600,bbox_inches='tight')
plt.show()

control_values = np.array(df_c_mean['mean'].to_list(),dtype=float)
iNPH_values = np.array(df_d_mean['mean'].to_list(),dtype=float)
stat, pvalue = scipy.stats.ttest_ind(iNPH_values,control_values,equal_var = False)
mean_control = np.mean(control_values)
mean_iNPH = np.mean(iNPH_values)
SEM_control = stats.sem(control_values,ddof=1)
SEM_iNPH = stats.sem(iNPH_values,ddof=1)

#df_overview 
df_overview = pd.DataFrame()
df_overview['Control mean'] = [mean_control]
df_overview['Control SEM'] = [SEM_control]
df_overview['iNPH mean'] = [mean_iNPH]
df_overview['iNPH SEM'] = [SEM_iNPH]
df_overview['Pvalue'] = [pvalue]

def convert_pvalue_to_asterisks(pvalue):
    if pvalue <= 0.0001:
        return "****"
    elif pvalue <= 0.001:
        return "***"
    elif pvalue <= 0.01:
        return "**"
    elif pvalue <= 0.05:
        return "*"
    return "ns"


df_overview['Significance'] = convert_pvalue_to_asterisks(pvalue)
df_overview.to_excel(os.path.join(Folder2,overview_file),index=False)