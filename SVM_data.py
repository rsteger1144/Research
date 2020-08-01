#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 22:23:55 2020

@author: robertsteger
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
import pandas as pd
from matplotlib import style
style.use("ggplot")
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import os

# Change the current working Directory    
try:    
    os.chdir("//Users/robertsteger/Downloads/")
except OSError:
    print("Can't change the Current Working Directory") 


def Implimenting_Data(yVal):
    #retrieve data from csv files
    data_df1 = pd.read_csv("Original_Data - Sheet1 (4).csv")
    data_df2 = pd.read_csv("Data - Sheet1 (2).csv")
    
    
    #creating test and train data
    scaleString = "Site"
    scale = np.array(data_df1[scaleString].values.tolist())
    count1 = 0
    count2 = 0
    count3 = 0
    X1 = np.array(data_df2.values.tolist())
    X2 = np.array(data_df2.values.tolist())
    X3 = np.array(data_df2.values.tolist())
    y_train = np.array(data_df1[yVal].values.tolist())
    y_test1 = np.array(data_df1[yVal].values.tolist())
    y_test2 = np.array(data_df1[yVal].values.tolist())
    r,c = X1.shape
    
    
    for i in range(r):
        if(scale[i] == 1):
            X2 = np.delete(X2,i-count2,0)
            y_test1 = np.delete(y_test1,i-count2,0)
            count2+=1
            X3 = np.delete(X3,i-count3,0)
            y_test2 = np.delete(y_test2,i-count3,0)
            count3+=1
        elif(scale[i] == 2):
            X1 = np.delete(X1,i-count1,0)
            y_train = np.delete(y_train,i-count1,0)
            count1+=1
            X3 = np.delete(X3,i-count3,0)
            y_test2 = np.delete(y_test2,i-count3,0)
            count3+=1
        elif(scale[i] == 3):
            X1 = np.delete(X1,i-count1,0)
            y_train = np.delete(y_train,i-count1,0)
            count1+=1
            X2 = np.delete(X2,i-count2,0)
            y_test1 = np.delete(y_test1,i-count2,0)
            count2+=1
            
            
    X_train = X1
    X_test1 = X2
    X_test2 = X3
        
            
    
    return X_test1, X_test2, X_train, y_test1, y_test2, y_train




def Analysis(yVal):

    X_test1, X_test2, X_train, y_test1, y_test2, y_train = Implimenting_Data(yVal)
  
    
    """
    #graph size
    plt.axis()
    x_min = 4
    x_max = 12
    y_min = 0
    y_max = 12
    
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    
    #plotting graph
    plt.scatter(X_test[:,0], X_test[:, 1], c=y_test)
    plt.show()
    """
    #testing accuracy of SVM for different kernels
    print()
    print(yVal)
    print()
    print("____________________________________")
    print("Precision of kernel = rbf")
    print("Test 1")
    clf1 = svm.SVC(kernel = 'rbf',C=1, gamma='scale', probability=True)
    clf1.fit(X_train, y_train)
    y_pred1 = clf1.predict(X_test1)
    print(confusion_matrix(y_test1, y_pred1))
    print(classification_report(y_test1, y_pred1))
    print("Accuracy:")
    print(accuracy_score(y_test1, y_pred1))
    print()
    
    print("____________________________________")
    print("Precision of kernel = rbf")
    print("Test 2")
    clf2 = svm.SVC(kernel = 'rbf',C=1, gamma='scale', probability=True)
    clf2.fit(X_train,y_train)
    y_pred2 = clf2.predict(X_test2)
    print(confusion_matrix(y_test2, y_pred2))
    print(classification_report(y_test2, y_pred2))
    print("Accuracy:")
    print(accuracy_score(y_test2, y_pred2))
    print()
    
    print("*********")
    
    print("____________________________________")
    print("Precision of kernel = polynomial")
    print("Test 1")
    clf3 = svm.SVC(kernel='poly', degree=12)
    clf3.fit(X_train, y_train)
    y_pred3 = clf3.predict(X_test1)
    print(confusion_matrix(y_test1, y_pred3))
    print(classification_report(y_test1, y_pred3))
    print("Accuracy:")
    print(accuracy_score(y_test1, y_pred3))
    print()
    
    print("____________________________________")
    print("Precision of kernel = polynomial")
    print("Test 2")
    clf4 = svm.SVC(kernel = 'poly', degree=12)
    clf4.fit(X_train,y_train)
    y_pred4 = clf4.predict(X_test2)
    print(confusion_matrix(y_test2, y_pred4))
    print(classification_report(y_test2, y_pred4))
    print("Accuracy:")
    print(accuracy_score(y_test2, y_pred4))
    print()
    
    print("*********")
        
    print("____________________________________")
    print("Precision of kernel = sigmoid")
    print("Test 1")
    clf5 = svm.SVC(kernel='sigmoid')
    clf5.fit(X_train, y_train)
    y_pred5 = clf5.predict(X_test1)
    print(confusion_matrix(y_test1, y_pred5))
    print(classification_report(y_test1, y_pred5))
    print("Accuracy:")
    print(accuracy_score(y_test2, y_pred5))
    print()
    
    print("____________________________________")
    print("Precision of kernel = sigmoid")
    print("Test 2")
    clf6 = svm.SVC(kernel='sigmoid')
    clf6.fit(X_train,y_train)
    y_pred6 = clf6.predict(X_test2)
    print(confusion_matrix(y_test2, y_pred6))
    print(classification_report(y_test2, y_pred6))
    print("Accuracy:")
    print(accuracy_score(y_test2, y_pred6))
    print()
    


#All 10 binary labels
BinaryLL = ["VS_3y","RRT_3y","glom_inflam","glomscl0","ifta0","inflam_pres0",
            "inflam_fib0","ati0","arteriole_scl0","arterial_scl0"]

for i in range(len(BinaryLL)):
    y_Val = BinaryLL[i]
    Analysis(y_Val)



#Analysis("VS_3y")
#Analysis("RRT_3y")
#Analysis("glom_inflam")
#Analysis("glomscl0")
#Analysis("ifta0")
#Analysis("inflam_pres0")
#Analysis("inflam_fib0")
#Analysis("ati0")
#Analysis("arterial_scl0")
#Analysis("arteriole_scl0")
#Analysis("arterial_scl0")
  