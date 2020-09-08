#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 8 22:53:50 2020

@author: robertsteger
"""
import numpy as np
import pandas as pd
from csv import reader

class CDR_regions():
    
    def __init__(self, file, seq):
        
        self.cdr1_map = dict()
        self.cdr2_map = dict()
        self.cdr3_map = dict()
        
        self.cdr1_list = []
        self.cdr2_list = []
        self.cdr3_list = []
        
        self.res1_list = []
        self.res2_list = []
        self.res3_list = []
        
        with open(file, 'r') as read_obj:
           csv_reader = reader(read_obj)
           self.X = list(csv_reader)
            
            
        self.X.pop(0)
        self.X.pop(0)
        for row in self.X:
            del row[0]
        
        
        r = len(self.X)
        self.seq = seq
        self.row = -1
        for i in range(r):
            if self.X[i][5] == self.seq:
                self.row = i
        if self.row == -1:
            print("Sequence not in file, errors will be thrown when calling other functions")
        
        
    def CDR_region_map(self):
        cdr_region = self.X[self.row][2]
        #create map of all 3 cdr regions
        for c in range(3):
            cdr_region = self.X[self.row][c+2]
            count = 0
            holder = 0 
            for i in range(len(cdr_region)):
                if count == 0 and cdr_region[i] in "1234567890":
                    holder = i
                    count = 1
                elif ":" in cdr_region[i]:
                    num = int(cdr_region[holder:i-1])
                    letter = cdr_region[i+3]
                    if c == 0:
                        self.cdr1_map[num] = letter
                        count = 0
                    elif c == 1:
                        self.cdr2_map[num] = letter
                        count = 0
                    elif c == 2:
                        self.cdr3_map[num] = letter
                        count = 0
        
    
    def CDR_Order(self):
        for a in range(150):
            for b in self.cdr1_map.keys():
                if b == a:
                    #print(self.cdr1_map[b])
                    self.res1_list.append(b)
                    self.cdr1_list.append(self.cdr1_map[b])
                    
        for c in range(150):
            for d in self.cdr2_map.keys():
                if d == c:
                    #print(self.cdr2_map[d])
                    self.res2_list.append(d)
                    self.cdr2_list.append(self.cdr2_map[d])
                    
        for e in range(150):
            for f in self.cdr3_map.keys():
                if f == e:
                    #print(self.cdr3_map[f])
                    self.res3_list.append(f)
                    self.cdr3_list.append(self.cdr3_map[f])
                    
                    
    def get_CDR_maps(self):
         return self.cdr1_map, self.cdr2_map, self.cdr3_map
     
    def get_CDR_ordered_lists(self):
        return self.cdr1_list, self.cdr2_list, self.cdr3_list
    def get_all_CDR_ordered_lists(self):
        all_cdr =  self.cdr1_list + self.cdr2_list + self.cdr3_list
        return all_cdr
    def get_res_lists(self):
        return self.res1_list, self.res2_list, self.res3_list
    def get_all_res_lists(self):
        all_res = self.res1_list + self.res2_list + self.res3_list
        return all_res
    def get_seq(self):
        return self.seq
    def get_seq_row(self):
        return self.row
    def get_CDR_lists_len(self):
        return len(self.cdr1_list) + len(self.cdr2_list) + len(self.cdr3_list)
    
    
#call this from OAS to create CSv file

