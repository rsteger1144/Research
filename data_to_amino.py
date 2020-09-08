#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 10:17:53 2020

@author: robertsteger
"""
import pandas as pd
import numpy as np
def ConvertData(csv, row):
    data_df = pd.read_csv(csv)
    array = np.array(data_df.values.tolist())
    c1String = array[row][12]
    c2String = array[row][13]
    c3String = array[row][14]
    cdrl1 = []
    cdrl2 = []
    cdrl3 = []
    for i in range(len(c1String)):
        if c1String[i] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
           cdrl1.append(c1String[i]) 
    for j in range(len(c2String)):
        if c2String[j] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
           cdrl2.append(c2String[j])
    for k in range(len(c3String)):
        if c3String[k] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
           cdrl3.append(c3String[k])
    
    return cdrl1,cdrl2,cdrl3

for i in range(1,10):
    l1,l2,l3 = ConvertData("Bernat_light_chain2.csv",i)
    print(l1)
    print(l2)
    print(l3)
    print()