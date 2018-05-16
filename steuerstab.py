# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def toseconds(minu):
    #return np.floor(minu)
    return np.floor(minu) *60 + (minu - np.floor(minu))*100

def rhoS(t2):
    ls = 0.0001 #s
    ts = t2 / np.log(2)
    beta = 0.0051 #s
    aI = [0.033,0.219,0.196,0.395,0.115,0.042]
    lambdaI = [0.0124,0.0305,0.111,0.301,1.14,3.01] 
    return (ls / ts / beta + sum([aI[i]/(1 + lambdaI[i]*ts) for i in range(6)]))

x1 = np.array([4000,3438,2771,2137,1354,0][::-1])
x2 = np.array([0,810,1637,2418,3190,4000])

x1_mid = np.array([(x1[i]+x1[i+1])/2 for i in range(len(x1)-1)])
x2_mid = np.array([(x2[i]+x2[i+1])/2 for i in range(len(x2)-1)])

t_min = np.array([3.18,1.45,1.22,1.17,1.59]) # min.sec
t2 = toseconds(t_min)

df = pd.DataFrame({"Steuerstab 2": x2,"Steuerstab 1": x1})

df["diff Reaktivität SS1"] = rhoS(df["Steuerstab 1"])
df["diff Reaktivität SS2"] = rhoS(df["Steuerstab 2"])

diff_rho = rhoS(t2)
#

plt.figure(1)
plt.plot(x2_mid,diff_rho, 'k' )



print(x2_mid)

print(diff_rho)
print(df)