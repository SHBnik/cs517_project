#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

currentDir = os.getcwd()
currentFileCSV2021 = currentDir +"\\" + "batpitch2021.csv"
# csvFileObj = open(currentFileCSV)
batpitch2021 = pd.read_csv(currentFileCSV2021)
currentFileCSV2019 = currentDir +"\\" + "batpitch2019.csv"
batpitch2019 = pd.read_csv(currentFileCSV2019)

def f_z_norm(data):
    mean = np.mean(data)
    std = np.std(data)
    z_norm = [(y-mean)/std for y in data]
    return z_norm

batpitch2021.head()


# In[2]:


batpitch2021['z_Bat'] = f_z_norm(batpitch2021['Bat']) 
batpitch2021['z_Pitch'] = f_z_norm(batpitch2021['Pitch']) 

batpitch2021.head()


# In[3]:


print(batpitch2021.loc[0,'Team'], batpitch2021.loc[0,'Rank'] )

for i in range(0,30):
    if batpitch2021.loc[i,'Team'] == "ARI":
        print("ARI :", i)


# In[4]:


import math
print("*" * 60 )
print("     In 2021, analyze Pitching and Batting impact on MLB by BGD ") 
print("*" * 60 )
epoch = 5000
l_rate = [10**-1, 10**-2, 10**-3, 10**-4, 10**-5, 10**-6]
t_errors0 = []
t_errors1 = []
t_errors2 = []
t_errors3 = []
t_errors4 = []
t_errors5 = []
t_errors6 = []
t_errors7 = []

t_MSE0 = []
t_MSE1 = []
t_MSE2 = []
t_MSE3 = []
t_MSE4 = []
t_MSE5 = []
t_MSE6 = []
t_MSE7 = []


X = np.array([
batpitch2021['z_Bat'],
batpitch2021['z_Pitch']
])
Y = np.array(batpitch2021['Rank'])

mX = np.concatenate((np.ones((1,30)),X),axis=0)
print("mX shape: ", mX.shape )

for l_num in (0,1,2,3,4,5):
    t_error = []
## not theta W gonna be 19
    W = np.random.rand(1,3)
    
    for step in range(epoch):
        hat_y = np.dot(W, mX)
        diff = hat_y - Y
        #MSE
        MSE = (diff**2).mean()
        
        t_error = 2*(diff*mX).mean()

        if abs(t_error) < 0.0001 or math.isinf(t_error) or math.isnan(t_error) :
#        if abs(t_error) < 0.0001 or math.isinf(t_error) :
            t_error = backup
            break 

        W = W - l_rate[l_num] * t_error

        if l_num == 0:
            t_errors0.append(t_error)
            t_MSE0.append(MSE)
        elif l_num == 1:
            t_errors1.append(t_error)
            t_MSE1.append(MSE)
        elif l_num == 2:
            t_errors2.append(t_error)
            t_MSE2.append(MSE)
        elif l_num == 3:
            t_errors3.append(t_error)
            t_MSE3.append(MSE)
        elif l_num == 4:
            t_errors4.append(t_error)
            t_MSE4.append(MSE)
        else:
            t_errors5.append(t_error)
            t_MSE5.append(MSE)
        
        backup = t_error
        
        # if step % 200 == 0 :
        #         print("{ learning rate : ", l_rate[l_num] , " step :" , step, "** error : " , t_error,  "## W : " , W , " ### MSE : " , MSE,  " }") 

    print("----" * 15)
    print("{ learning rate : ", l_rate[l_num] , " step :" , step, "** error : " , t_error,  "## W : " , W ,  " ### MSE : " , MSE, " }") 
    print("====" * 15)

plt.figure(figsize=(12,8))
# plt.ylim([-1, 1])
plt.plot(t_errors0 , 'y-')
plt.plot(t_errors1 , 'v-')
plt.plot(t_errors2 , 'm-')
plt.plot(t_errors3 , 'y-')
plt.plot(t_errors4 , 'g-')
plt.plot(t_errors5 , 'b-')
plt.legend([r'$\frac{1}{10}$',r'$\frac{1}{100}$',r'$\frac{1}{1000}$',r'$\frac{1}{10000}$',r'$\frac{1}{100000}$',r'$\frac{1}{1000000}$'])
plt.xlabel('epoch')
plt.ylabel('cost by different learning rate')
plt.title('BGD with Z normalization')

plt.show()

plt.figure(figsize=(12,8))
#plt.ylim([0, 3])
plt.plot(t_MSE0 , 'y-')
plt.plot(t_MSE1 , 'v-')
plt.plot(t_MSE2 , 'm-')
plt.plot(t_MSE3 , 'y-')
plt.plot(t_MSE4 , 'g-')
plt.plot(t_MSE5 , 'b-')
plt.legend([r'$\frac{1}{10}$',r'$\frac{1}{100}$',r'$\frac{1}{1000}$',r'$\frac{1}{10000}$',r'$\frac{1}{100000}$',r'$\frac{1}{1000000}$'])
plt.xlabel('epoch')
plt.ylabel('MES by different learning rate')
plt.title('BGD with Z normalization')


# In[5]:


# We know that Pitching is more important than Batting in 2021 by BGD. Pitching 54%, Batting 46%. 
# If we apply the winning rate with this for 50%, Pitching (Run allowed on game) will be 27%, Batting (Run on game) will be 23%
# Now we're ready to make winning rate matrix. 


# In[6]:


ALmatchingCSV2021 = currentDir +"\\" + "ALmatching2021.csv"
ALmat_data2021 = pd.read_csv(ALmatchingCSV2021)
NLmatchingCSV2021 = currentDir +"\\" + "NLmatching2021.csv"
NLmat_data2021 = pd.read_csv(NLmatchingCSV2021)

ALmatchingCSV2019 = currentDir +"\\" + "ALmatching2019.csv"
ALmat_data2019 = pd.read_csv(ALmatchingCSV2019)
NLmatchingCSV2019 = currentDir +"\\" + "NLmatching2019.csv"
NLmat_data2019 = pd.read_csv(NLmatchingCSV2019)

# ALmat_data2021.head()
NLmat_data2019.head()


# In[300]:


def find_rank(team):
    # print("chk :", team[-2:] , " and " , team[0:3]) 
    for i in range(0,30):
        for j in range(0,31):
            if team[-2:] == '21':
                if batpitch2021.loc[j,'Team'] == team[0:3]:
                    return batpitch2021.loc[j,'Rank'], batpitch2021.loc[j,'Bat'], batpitch2021.loc[j,'Pitch']    
            else :
                if batpitch2019.loc[j,'Team'] == team[0:3]:
                    return batpitch2019.loc[j,'Rank'], batpitch2019.loc[j,'Bat'], batpitch2019.loc[j,'Pitch']    


NLlist = ['ATL','MIA','NYM','PHI','WSN','CHC','CIN','MIL','PIT','STL','ARI','COL','LAD','SDP','SFG']
ALlist = ['BAL','BOS','NYY','TBR','TOR','CHW','CLE','DET','KCR','MIN','HOU','LAA','OAK','SEA','TEX']
print(ALmat_data2021)
print(NLmat_data2021)
# for row_index, row in ALmat_data.iterrows():
#     print(row_index)
#     print(row)
    
# print(ALmat_data.loc[0,'BOS'])

dataframe_A = pd.DataFrame(ALmat_data2021)
dataframe_B = pd.DataFrame(NLmat_data2021)
df_TM1 = pd.merge(dataframe_A, dataframe_B, left_on='Tm', right_on='Tm', how='outer')
df_TM1 = df_TM1.fillna('999')
print("# 1 :", df_TM1)

dataframe_C = pd.DataFrame(ALmat_data2019)
dataframe_D = pd.DataFrame(NLmat_data2019)
df_TM2 = pd.merge(dataframe_C, dataframe_D, left_on='Tm', right_on='Tm', how='outer')
df_TM2 = df_TM2.fillna('999')
print("# 2 :", df_TM2)

df_TM = pd.merge(df_TM1, df_TM2, left_on='Tm', right_on='Tm', how='outer')
df_TM = df_TM.fillna('999')
print("# 3 :", df_TM)

# print(df_TM.columns[2])
for i in range(0,60):
    for j in range(1,61):
        # print("Found :", i, j, df_TM.columns[j], df_TM.iloc[i,0])
        col_rank, col_bat, col_pitch = find_rank(df_TM.columns[j])
        row_rank, row_bat, row_pitch = find_rank(df_TM.iloc[i,0])
        forecasting_rate = 0
        
        if df_TM.iloc[i,j] == '999'  :
            learn_from_past = round(row_rank / (col_rank + row_rank) , 3)
        elif df_TM.iloc[i,j] == '--' :
            # df_TM.iloc[i,j] = 999
            learn_from_past = 999
        else:
            if int(df_TM.iloc[j-1,i+1]) in range(0,1) :
            # if  "." in df_TM.iloc[j-1,i+1]:
                learn_from_past = round(1 - float(df_TM.iloc[j-1,i+1]),3)
                # print("chk2 simple ### ", float(df_TM.iloc[j-1,i+1]), learn_from_past)
            else:
                total_g = int(df_TM.iloc[i,j]) + int(df_TM.iloc[j-1,i+1])
                learn_from_past = round(int(df_TM.iloc[i,j])/total_g,3)
                # print("chk3 calculate ### ", total_g, df_TM.iloc[i,j], df_TM.iloc[j-1,i+1], learn_from_past)
                # learn_from_past = round(int(df_TM.iloc[i,j])/7,2)
        
        # For pitching ability, smaller value is better. Thus change the sequence to calculate the importance 
        learn_from_ability = round((col_bat / (col_bat+row_bat)) * 0.46 + (col_pitch / (col_pitch+row_pitch)) * 0.54, 3)

        forecasting_rate = round(learn_from_past * 0.5 + learn_from_ability * 0.5, 3)
        
        if j == i+1 and forecasting_rate > 1:
            forecasting_rate = 0.5
        # if j == i+1:
        #     forecasting_rate = 0
            
        df_TM.iloc[i,j] = forecasting_rate

for i in range(0,60):
    for j in range(1,61):
        chk_1 = float(df_TM.iloc[i,j]) + float(df_TM.iloc[j-1,i+1])
        if chk_1 < 2 and chk_1 != 1:
            df_TM.iloc[j-1,i+1] = round(1 - float(df_TM.iloc[i,j]),3)

print(df_TM)


# In[8]:


# pd.set_option('display.max_seq_items', None)
# pd.set_option('display.max_columns', None)


# In[301]:


from IPython.core.display import HTML
display(HTML(df_TM.to_html()))


# In[146]:


def match(team1, team2):
    # Check routine
    if team1[0:3] not in NLlist and team1[0:3] not in ALlist:
        print("Input team1(=",team1,") is not in MLB. Please check the name of team1")
        return
    if team2[0:3] not in NLlist and team2[0:3] not in ALlist:
        print("Input team2(=",team2,") is not in MLB. Please check the name of team1")
        return
    if team1[-2:] != '19':
        if team1[-2:] != '21':
            print("There are only 2021 and 2019 data in the Matrix.(2020 was not considered /Covid)")
            return
    if team2[-2:] != '19':
        if team2[-2:] != '21':
            print("There are only 2021 and 2019 data in the Matrix.(2020 was not considered /Covid)")
            return
    if len(team1) != 5 or len(team2) != 5:
        print("Input value should be 5 length by team + year (i.e. BOS19 )")
        return
    
    for i in range(0,60):
        for j in range(0,61):
            if df_TM.iloc[i,0] == team1 and df_TM.columns[j] == team2:
                # print("Found Result :", df_TM.iloc[i,j])
                return team1, df_TM.iloc[i,j]
            
print(match('BAL21','CLE21'))
print(match('CLE21','BAL21'))
# print(match('BAL2021','CIN2021'))


# In[148]:


names = ['BAL21','NYY21','SEA19','CHC19','LAD21','ATL21','TEX19','OAK21']
# temp = []
matrix = []

for i in range(9):
    temp = []
    if i == 0 :
        matrix.append(names)
        continue
    for j in range(9):
        if j == 0 :
            temp.append(names[i-1])
            continue
        temp.append(match(names[i-1],names[j-1])[1])
    matrix.append(temp)

# for n1,i in enumerate(names):
#     for n2,j in enumerate(names):
#         # print(match(i,j))
#         matrix[n1][n2] = match(i,j)[1]
        
for i in matrix : print(i)


# In[149]:


filteredMatrix = []
def filterResult(prob, threshold):
    if prob >= 0.5 + threshold:
        return 1
    elif prob <= 0.5 - threshold:
        return 0
    else:
        return 0.5

for i in range(9):
    temp = []
    if i == 0 :
        matrix.append(names)
        continue
    for j in range(9):
        if j == 0 :
            temp.append(names[i-1])
            continue
        temp.append(filterResult(match(names[i-1],names[j-1])[1], 0.2))
    matrix.append(temp)

for i in matrix : print(i)


# In[159]:


import random

def make_mask(win_team, n):
    pop_str =  df_TM.columns[1:].tolist()
    # print("chk " , type(pop_str), pop_str)
    pop_str.remove(win_team)
    ran_choice = random.sample(pop_str,n-1)
    names = []
    matrix = []
    names.insert(0,win_team)
    j = 1
    for i in ran_choice:
        names.insert(j,ran_choice[j-1])
        j += 1
        
    print("++Selected randomly ", n ," teams : ", names)
    
    filteredMatrix = []
    def filterResult(prob, threshold):
        if prob >= 0.5 + threshold:
            return 1
        elif prob <= 0.5 - threshold:
            return 0
        else:
            return 0.5

    for i in range(n+1):
        temp = []
        if i == 0 :
            matrix.append(names)
            continue
        for j in range(n+1):
            if j == 0 :
                temp.append(names[i-1])
                continue
            temp.append(filterResult(match(names[i-1],names[j-1])[1], 0.05))
        matrix.append(temp)

    for i in matrix : print(i)
    ##
    return matrix

rt_matrix = make_mask('BAL19',32)

