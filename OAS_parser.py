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
from Data_Alter import Data_Change

#Fetch all files in directory and subdirectories.
def list_file_paths(directory):
    for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))
         
#Parse out the contents of a single file.
def parse_single_file(src, listx, row, light, heavy, numOfData):
    #The first line are the meta entries.
    meta_line = True
    for line in gzip.open(src,'rb'):
       if meta_line == True:
           metadata = json.loads(line)
           meta_line=False
           continue
       
       if row >= numOfData:
          break
       #Parse actual sequence data.
       basic_data = json.loads(line) 
       seq = basic_data['seq']
       str_row = str(row)
       listx[row][0]= "Seq_"+ str_row + ":"+ seq[0:5]
       listx[row][1]=metadata['Chain']
       listx[row][5]=basic_data['seq']
       
       
       
       #listx[row][0]=metadata['Age']
       #listx[row][1]=metadata['BSource']
       #listx[row][2]=metadata['BType']
       #listx[row][4]=metadata['Disease']
       #listx[row][5]=metadata['Isotype']
       #listx[row][6]=metadata['Size_igblastn']
       #listx[row][8]=basic_data['cdr3']
       #listx[row][9]=basic_data['j']
       #listx[row][10]=basic_data['v']
        
        
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
               if data[i] in "c":
                    #add f^
                   count+=1
                   holder1 = i
               elif data[i] in "drl":
                  #add w^
                   count+=1
               if data[holder1] == "c" and count == 4:
                   if data[i+1] == "1":
                       column = 2
                       count = 0
                       count2+=1
                   elif data[i+1] == "2":
                       column = 3
                       count = 0
                       count2+=1
                   elif data[i+1] == "3":
                       column = 4
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
               if data[i] in "c":
                   #add f^
                   count+=1
                   holder1 = i
               elif data[i] in "drh":
                   #add w^
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

    return row


#convert data to csv file
def DataToCSV(directory, chain, numOfData, nameOfFile):
    l = np.zeros((numOfData,6), dtype=object)
    l[0][0]='Identifier'
    l[0][1]='Chain'
    l[0][5]='Sequence'
    
    
    #l[0][0]='Age'
    #l[0][1]='BSource'
    #l[0][2]='BType'
    #l[0][4]= 'Disease'
    #l[0][5]='Isotype'
    #l[0][6]='Size_igblastn'
    #l[0][8]='cdr3'
    #l[0][9]='j'
    #l[0][10]='v'
    
    
    if chain == "L":
        l[0][2]='cdrl1'
        l[0][3]='cdrl2'
        l[0][4]='cdrl3'
        #l[0][14]='fwl1'
        #l[0][15]='fwl2'
        #l[0][16]='fwl3'
        #l[0][17]='fwl4'
        #l[0][12]='Original Name'
        
        row = 1
        for f in list_file_paths(directory):
            row = parse_single_file(f,l,row, True, False, numOfData)
            row+=1
            
    elif chain == "H":
        l[0][11]='cdrh1'
        l[0][12]='cdrh2'
        l[0][13]='cdrh3'
        l[0][14]='fwh1'
        l[0][15]='fwh2'
        l[0][16]='fwh3'
        l[0][17]='fwh4'
        #l[0][12]='Original Name'
        
        row = 1
        for f in list_file_paths(directory):
            row = parse_single_file(f,l,row, False, True, numOfData)
            row+=1
    temp = nameOfFile + "_temp.csv"
    pd.DataFrame(l).to_csv(temp)
    
    converter = Data_Change(temp)
    converter.create_new_data()
    new_data = converter.get_new_data()
    
    fileName = nameOfFile + ".csv"
    df = pd.DataFrame(new_data)
    df.to_csv(fileName, index=False, header=False)
    
    
    
    
    
#checks for sequence in csv file to data
def duplicate_checker_single_file(src, file):
    data_df = pd.read_csv(file)
    X1 = np.array(data_df.values.tolist())
    row, col = X1.shape
    meta_line=True
    seq_map = dict()
    for i in range(row):
        seq_map[i] = X1[i][0]
    for line in gzip.open(src,'rb'):
        if meta_line == True:
            metadata = json.loads(line)
            meta_line=False
            continue
        basic_data = json.loads(line)
        seq = basic_data['seq']
        for s in seq_map.values():
            if seq == s:
                print("There is a duplicate")
            
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
        
        

def ConvertDatatoAmino(csv, row):
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
    

def CreateFafstaFile(csv_file, file_name):
    data_df = pd.read_csv(csv_file)
    array = np.array(data_df.values.tolist())
    row, col = array.shape
    all_seq = ">Sequences"
    for i in range(1,row):
        Seq = array[i][2]
        all_seq= all_seq + "\n" + Seq
    
    file_name += ".txt"
    fasta = open(file_name, 'w')
    fasta.write(all_seq)
        
    fasta.close()
        

    
    


#Replace this with the location of where you uncompressed the bulk data file.

# Change the current working Directory    
try:    
    os.chdir("//Users/robertsteger/Research(Kola)/Data/OAS-data/CSV files/")
except OSError:
    print("Can't change the Current Working Directory")

directory1 = "//Users/robertsteger/Research(Kola)/Data/OAS-data/Bernat_Ligh_C/"
directory2 = "//Users/robertsteger/Downloads/Heavy_Chain/"
file = "Bernat_light_chain.csv"
DataToCSV(directory1, "L", 38, "Bernat_light_38_seq")
#duplicate_checker_bulk(directory2, file)
#parse_single_file_printer("Bernat_2019_Light_IgK_Light_IgK_A007.json.gz",1)
#CreateFafstaFile("Bernat_light_38_seq.csv", 'c')

print("completed")




