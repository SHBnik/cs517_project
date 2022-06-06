#!/usr/bin/env python
# coding: utf-8

# In[102]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

currentDir = os.getcwd()
currentFileCSV2021 = currentDir +"\\" + "stat2021.csv"
# csvFileObj = open(currentFileCSV)
stat2021 = pd.read_csv(currentFileCSV2021)
currentFileCSV2021f = currentDir +"\\" + "fullstat2021.csv"
stat2021f = pd.read_csv(currentFileCSV2021f)

def f_z_norm(data):
    mean = np.mean(data)
    std = np.std(data)
    z_norm = [(y-mean)/std for y in data]
    return z_norm

stat2021f.head()


# In[104]:


# stat2021['z_Bat'] = f_z_norm(stat2021['Bat']) 
# stat2021['z_Pitch'] = f_z_norm(stat2021['Pitch'])
# stat2021['z_W'] = f_z_norm(stat2021['W'])
# stat2021['z_W-L%'] = f_z_norm(stat2021['W-L%'])

stat2021f['z_R/G'] = f_z_norm(stat2021f['R/G']) 
stat2021f['z_RA/G'] = f_z_norm(stat2021f['RA/G'])
stat2021f['z_W'] = f_z_norm(stat2021f['W'])
stat2021f['z_W-L%'] = f_z_norm(stat2021f['W-L%'])

stat2021f.head()


# In[141]:


l = stat2021f[0:0].T
rt_label = []
rt_val = []
# chk_range = [1,2,3,4,5,6,7,8,12,13,14]
for i in range(1,len(l)):
    # print(l.index[i])
    df = pd.DataFrame([stat2021f['z_W-L%'],stat2021f[l.index[i]]]).T
    corr = df.corr(method = 'pearson')
    # print(corr)
    # print(corr.iloc[1,0])
    rt_label.append(l.index[i])
    rt_val.append(corr.iloc[1,0])
    print( l.index[i] , round(corr.iloc[1,0],3))


# In[142]:


plt.figure(figsize=(35,8))
plt.bar(rt_label,rt_val)
# plt.legend(rt_label)
# plt.legend(['10',r'$10^0$',r'$\frac{1}{10}$',r'$\frac{1}{100}$',r'$\frac{1}{1000}$',r'$\frac{1}{10000}$',r'$\frac{1}{100000}$',r'$\frac{1}{1000000}$'])
plt.xlabel('Metrics')
plt.ylabel('Correlation coefficient')
plt.title('Pearson Correlation coefficient(with W-L%)')

for i, v in enumerate(rt_label):
    plt.text(v, rt_val[i], str(round(rt_val[i],3)),
             fontsize=9,
             color="blue",
             horizontalalignment='center',
             verticalalignment='bottom')

plt.show()

