# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def toseconds(minu):
    return np.floor(minu) *60 + (minu - np.floor(minu))*100

def rhoS(t2):
    ls = 0.0001 #s
    ts = t2 / np.log(2)
    beta = 0.0051 #s
    aI = [0.033,0.219,0.196,0.395,0.115,0.042]
    lambdaI = [0.0124,0.0305,0.111,0.301,1.14,3.01]
    return (ls / ts / beta + sum([aI[i]/(1 + lambdaI[i]*ts) for i in range(6)]))

x1 = np.array([4000,4000,3438,2771,2137,1354,0,0][::-1])
x2 = np.array([0,0,810,1637,2418,3190,4000,4000])

x1_mid = np.array([(x1[i]+x1[i+1])/2 for i in range(len(x1)-1)])
x2_mid = np.array([(x2[i]+x2[i+1])/2 for i in range(len(x2)-1)])

t_min = np.array([1000,3.18,1.45,1.22,1.17,1.59,1000]) # min.sec
t2 = toseconds(t_min)

df = pd.DataFrame({"Steuerstab 2": x2[1::],"Steuerstab 1": x1[1::],
                   "Steuerstab 2 (mid)": x2_mid,"Steuerstab 1 (mid)": x1_mid,
                   "Reaktorperiode" : t2, "inv. Reaktorperiode" : t2[::-1]})


df["diff Reaktivität SS1"] = rhoS(df["inv. Reaktorperiode"])
df["diff Reaktivität SS2"] = rhoS(df["Reaktorperiode"])



df["integ Reaktivität SS1"] = df["diff Reaktivität SS1"].cumsum()
df["integ Reaktivität SS2"] = df["diff Reaktivität SS2"].cumsum()
#df["integ Reaktivität SS3"] = df["diff Reaktivität SS3"].cumsum()


#TODO
df["Steuerstab 3"] = (df["Steuerstab 1"] + df["Steuerstab 2"]) /2
df["Steuerstab 3 (mid)"] = (df["Steuerstab 1 (mid)"] + df["Steuerstab 2 (mid)"]) /2
df["diff Reaktivität SS3"] = (df["diff Reaktivität SS1"] + df["diff Reaktivität SS2"])/ 2
df["integ Reaktivität SS3"] = (df["integ Reaktivität SS1"] + df["integ Reaktivität SS2"])/ 2

fig, axes = plt.subplots(nrows=1, ncols=1)
df.plot(y = "diff Reaktivität SS1", x = "Steuerstab 1 (mid)", ax = axes, marker = "x", title = "differentielle Steuerstabkennlinie")
df.plot(y = "diff Reaktivität SS2", x = "Steuerstab 2 (mid)", ax = axes, marker = "x")
df.plot(y = "diff Reaktivität SS3", x = "Steuerstab 3 (mid)", ax = axes)

fig2, axes2 = plt.subplots(nrows=1, ncols=1)
df.plot(y = "integ Reaktivität SS1", x = "Steuerstab 1", ax = axes2, marker = "x", title = "integrale Steuerstabkennlinie")
df.plot(y = "integ Reaktivität SS2", x = "Steuerstab 2", ax = axes2, marker = "x")
df.plot(y = "integ Reaktivität SS3", x = "Steuerstab 3", ax = axes2)

axes.set_xlabel("Stabposition [1]")
axes.set_ylabel("differentielle Reaktivität [$]")
axes.grid()
axes2.set_xlabel("Stabposition [1]")
axes2.set_ylabel("integrale Reaktivität [$]")
axes2.grid()

#change size of the figures
fig.set_size_inches((19.2, 12), forward=False) #fullscreen
fig.set_size_inches((19.2, 12), forward=False)
fig.savefig("differentielle Steuerstabkennlinie", dpi=200)
fig2.savefig("integrale Steuerstabkennlinie", dpi=200)

print(df)
