#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 18:59:25 2020

@author: robertsteger
"""
from csv import reader
from CDR_regions import CDR_regions
import pandas as pd
import os
import csv

class Data_Change():
    
    def __init__(self, csv_file):
        self.csv = csv_file
        #self.data = []
        with open(self.csv, 'r') as read_obj:
            csv_reader = reader(read_obj)
            self.data = list(csv_reader)
            
            
        self.data.pop(0)
        self.data.pop(0)
        for row in self.data:
            del row[0]
            
        self.new_data = []
    
    
    def create_new_data(self):
        curr = []
        chain = ""
        for i in range(len(self.data)):
            cdr = CDR_regions(self.csv, self.data[i][5])
            if self.data[i][1] == "Light":
                chain = "L"
            else:
                chain = "H"
                
            cdr.CDR_region_map()
            cdr.CDR_Order()
            cdr_all = cdr.get_all_CDR_ordered_lists()
            res_all = cdr.get_all_res_lists()
            for j in range(len(cdr_all)):
                curr = []
                curr.append(self.data[i][0])
                chainSTR = chain + str(res_all[j])
                curr.append(chainSTR)
                curr.append(cdr_all[j])
                curr.append(self.data[i][5])
                self.new_data.append(curr)
    
    def get_new_data(self):
        return self.new_data
    






                
            
        
        
        
        