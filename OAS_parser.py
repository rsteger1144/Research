#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 23:41:41 2020

@author: robertsteger
"""

import os,gzip,json,pprint
import numpy as np
import pandas as pd
import os

#Fetch all files in directory and subdirectories.
def list_file_paths(directory):
    for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))
         
#Parse out the contents of a single file.
def parse_single_file(src, listx, row, light, heavy):
    #The first line are the meta entries.
    meta_line = True
    for line in gzip.open(src,'rb'):
       if meta_line == True:
           metadata = json.loads(line)
           meta_line=False
           continue
       
       if row >= 10000:
          break
       #Parse actual sequence data.
       basic_data = json.loads(line) 
       listx[row][0]=metadata['Age']
       listx[row][1]=metadata['BSource']
       listx[row][2]=metadata['BType']
       listx[row][3]=metadata['Chain']
       listx[row][4]=metadata['Disease']
       listx[row][5]=metadata['Isotype']
       listx[row][6]=metadata['Size_igblastn']
       listx[row][7]=basic_data['seq']
       listx[row][8]=basic_data['cdr3']
       listx[row][9]=basic_data['j']
       listx[row][10]=basic_data['v']
        
        
       #seperates heavy/ligth chains
       data = basic_data['data']
       holder1 = 0
       holder2 = 0
       count = 0
       count2 = 0
       column = 0
       i = 0
       if light is True:
           while(i < len(data)):
               if data[i] in "cf":
                   count+=1
                   holder1 = i
               elif data[i] in "drlw":
                   count+=1
               if data[holder1] == "c" and count == 4:
                   if data[i+1] == "1":
                       column = 11
                       count = 0
                       count2+=1
                   elif data[i+1] == "2":
                       column = 12
                       count = 0
                       count2+=1
                   elif data[i+1] == "3":
                       column = 13
                       count = 0
                       count2+=1
                   while(i<len(data)):
                       if data[i] == "{":
                           holder2 = i+1
                       if data[i] == "}":
                           listx[row][column] = data[holder2:i]
                           break
                       i+=1
               elif data[holder1] == "f" and count == 3:
                   if data[i+1] == "1":
                       column = 14
                       count = 0
                       count2+=1
                   elif data[i+1] == "2":
                       column = 15
                       count = 0
                       count2+=1
                   elif data[i+1] == "3":
                       column = 16
                       count = 0
                       count2+=1
                   elif data[i+1] == "4":
                       column = 17
                       count = 0
                       count2+=1
                    
                   while(i<len(data)):
                       if data[i] == "{":
                           holder2 = i+1
                       if data[i] == "}":
                           listx[row][column] = data[holder2:i]
                           break
                       i+=1
                
               i+=1
               if count2 == 7:
                   break

       elif heavy is True:
           while(i < len(data)):
               if data[i] in "cf":
                   count+=1
                   holder1 = i
               elif data[i] in "drhw":
                   count+=1
               if data[holder1] == "c" and count == 4:
                   if data[i+1] == "1":
                       column = 11
                       count = 0
                       count2+=1
                   elif data[i+1] == "2":
                       column = 12
                       count = 0
                       count2+=1
                   elif data[i+1] == "3":
                       column = 13
                       count = 0
                       count2+=1
                   while(i<len(data)):
                       if data[i] == "{":
                           holder2 = i+1
                       if data[i] == "}":
                           listx[row][column] = data[holder2:i]
                           break
                       i+=1
               elif data[holder1] == "f" and count == 3:
                   if data[i+1] == "1":
                       column = 14
                       count = 0
                       count2+=1
                   elif data[i+1] == "2":
                       column = 15
                       count = 0
                       count2+=1
                   elif data[i+1] == "3":
                       column = 16
                       count = 0
                       count2+=1
                   elif data[i+1] == "4":
                       column = 17
                       count = 0
                       count2+=1
                    
                   while(i<len(data)):
                       if data[i] == "{":
                           holder2 = i+1
                       if data[i] == "}":
                           listx[row][column] = data[holder2:i]
                           break
                       i+=1
               i+=1
               if count2 == 7:
                   break
            
       row+=1
       if row >= 10000:
           break

    return row


#convert data to csv file
def DataToCSV(directory, chain, numOfData, nameOfFile):
    l = np.zeros((numOfData,18), dtype=object)
    l[0][0]='Age'
    l[0][1]='BSource'
    l[0][2]='BType'
    l[0][3]='Chain'
    l[0][4]= 'Disease'
    l[0][5]='Isotype'
    l[0][6]='Size_igblastn'
    l[0][7]='Sequence'
    l[0][8]='cdr3'
    l[0][9]='j'
    l[0][10]='v'
    l[0][11]='cdrl1'
    l[0][12]='cdrl2'
    l[0][13]='cdrl3'
    l[0][14]='fwl1'
    l[0][15]='fwl2'
    l[0][16]='fwl3'
    l[0][17]='fwl4'
    #l[0][12]='Original Name'
    
    row = 1
    if chain == "L":
        for f in list_file_paths(directory):
            row = parse_single_file(f,l,row, True, False)
            row+=1
    elif chain == "H":
        for f in list_file_paths(directory):
            row = parse_single_file(f,l,row, False, True)
            row+=1
    
    fileName = nameOfFile + ".csv"
    pd.DataFrame(l).to_csv(fileName)
    
    
#checks for sequence in csv file to data
def duplicate_checker_single_file(src, file):
    data_df = pd.read_csv(file)
    X1 = np.array(data_df.values.tolist())
    row, col = X1.shape
    meta_line=True
    
    for line in gzip.open(src,'rb'):
        if meta_line == True:
            metadata = json.loads(line)
            meta_line=False
            continue
        basic_data = json.loads(line)
        seq = basic_data['seq']
        for i in range(row):
            if X1[i][8] == seq:
                print()
                print("HELL YES")
                print()
#checks bulk of data
def duplicate_checker_bulk(directory, file):
     for f in list_file_paths(directory):
         print(f)
         duplicate_checker_single_file(f,file)

#prints data on console
def parse_single_file_printer(src, numOfPrints):
    #The first line are the meta entries.
    meta_line = True
    i = 0
    for line in gzip.open(src,'rb'):
        if meta_line == True:
            metadata = json.loads(line)
            meta_line=False
            print("Metadata:")
            pprint.pprint(metadata)
            continue
        #Parse actual sequence data.
        print("Data:")
        basic_data = json.loads(line) 
        pprint.pprint(basic_data)
        i+=1
        if i == numOfPrints:
            break
        
        

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
    
       
              
        
    


#Replace this with the location of where you uncompressed the bulk data file.
directory1 = "//Users/Location"
directory2 = "//Users/Location2"
file = "File.csv"
#DataToCSV(directory1, "L", 10000, file)
#duplicate_checker_bulk(directory2, file)
print()
JSON_file = "File.json.gz"
parse_single_file_printer(JSON_file,1)

for i in range(1,10):
    l1,l2,l3 = ConvertData(file,i)
    print(l1)
    print(l2)
    print(l3)
    print()
