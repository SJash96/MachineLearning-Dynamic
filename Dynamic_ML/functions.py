from sklearn.model_selection import train_test_split 
from sklearn.tree import DecisionTreeClassifier 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report
#from imblearn.under_sampling import RandomUnderSampler
#from imblearn.over_sampling import RandomOverSampler
from collections import Counter
import ipaddress as ipadd
import pandas as pd
import numpy as np
import sys
import os

def memoryOptimization(data):
    
    #Downcast float datatypes to the smallest possible datatype without losing information
    floats = data.select_dtypes(include=['float64']).columns.tolist()
    data[floats] = data[floats].apply(pd.to_numeric, downcast='float')

    #Downcast int datatypes to the smallest possible datatype without losing information
    ints = data.select_dtypes(include=['int64']).columns.tolist()
    data[ints] = data[ints].apply(pd.to_numeric, downcast='integer')

    #Downcast object datatypes to the smallest possible datatype without losing information
    objects = data.select_dtypes(include=['object']).columns.tolist()
    for o in objects:
        num_unique_values = len(data[o].unique())
        num_total_values = len(data[o])
        if float(num_unique_values) / num_total_values < 0.5:
            data[o] = data[o].astype('category')

    dtypes = data.dtypes

    colnames = dtypes.index
    types = [t.name for t in dtypes.values]
    
    return dict(zip(colnames, types))


def readCSV(): 
    
    #Cannot read a sample of n = 1000 rows as it will give an error of stating NAN in integer columns
    #For now reads the entire CSV file.
    data = pd.read_csv('DataFiles/TrainingV3.csv')

    #Apply memory optimization to all the data
    #In total about 85% memory was reduced just by changing datatypes!!!
    data_Optimized = pd.read_csv('DataFiles/TrainingV3.csv', dtype=memoryOptimization(data))

    #Drop rows with missing values
    data_Optimized = data_Optimized.dropna()

    #pd.set_option('display.max_columns', None)

    return data_Optimized


def convertData(data, Proto_le, Label_le = None):

    #Converting the IP address to int values for more integer based dataset
    data['Source'] = data['Source'].apply(lambda x: int(ipadd.IPv4Address(x)))
    data['Destination'] = data['Destination'].apply(lambda x: int(ipadd.IPv4Address(x)))

    #Force change data types for both columns
    data['Source'] = data['Source'].astype('int64')
    data['Destination'] = data['Destination'].astype('int64')

    #Training set puts these columns as float types, force changing them to integer types
    data['Source Port'] = data['Source Port'].astype('int32')
    data['Destination Port'] = data['Destination Port'].astype('int32')

    #Encode the labels and fit protocol with the same encoding
    if Label_le:
        data['Label'] = Label_le.fit_transform(data['Label'])
        data['Protocol'] = Proto_le.fit_transform(data['Protocol'])
        if set(['No.', 'Time']).issubset(data.columns):
            data = data.drop(columns=['No.'])
            data = data.drop(columns=['Time'])
    else:
        data['Protocol'] = Proto_le.transform(data['Protocol'])

    return data


def printMetatdata(data):
    
    print(data.info(memory_usage='deep'))
    print("\nData Shape:\n", data.shape)
    data = data.sort_index(axis=1)
    print("\nSample Data:\n", data.head())
    #print("\nTypes:\n", data['Label'].value_counts())


def splitXY_train(data):

    X = data[data.columns.difference(['Label'])]
    Y = data['Label'].values.tolist()

    #print(X_train)
    #print(Y_train)

    return X, Y


def trainOnCLassifier(X, Y):

    #Running with default parameters
    decTree = DecisionTreeClassifier()
    decTree.fit(X, Y)

    return decTree 


def readLiveCSV():

    #Read and optimize the live data file(s)
    liveData = pd.read_csv('C:/Users/sjash/Desktop/packetFiles/livePackets.csv', nrows=1000)
    liveData_Optimized = pd.read_csv('C:/Users/sjash/Desktop/packetFiles/livePackets.csv', dtype=memoryOptimization(liveData))

    return liveData_Optimized


def predictions(X_test, classifier, Proto_le, Labe_le, exiting):

    Y_pred = classifier.predict(X_test)
    if not exiting:
        print("\nPrediction Outcome:")

    labels = list(Labe_le.inverse_transform(Y_pred))
    labelK = list(Counter(labels).keys())
    labelV = list(Counter(labels).values())
    labelDic = {labelK[i]: labelV[i] for i in range(len(labelK))}

    if not exiting:
        print("\nLabel Names: ")
        [print(str(k) + "\t" + str(v)) for k, v in labelDic.items()]

    sampleDF = pd.DataFrame(X_test)
    sampleDF['Label'] = labels
    sampleDF['Source'] = sampleDF['Source'].apply(lambda x: ipadd.IPv4Address(x))
    sampleDF['Destination'] = sampleDF['Destination'].apply(lambda x: ipadd.IPv4Address(x))
    sampleDF['Protocol'] = Proto_le.inverse_transform(sampleDF['Protocol'])
    if not exiting:
        print("\nSample Predicitons: ")
        print(sampleDF.tail(n=15))

    return sampleDF, labelK


def writeLiveCSV(data):

    print("Writing results to CSV")
    data.to_csv('C:/Users/sjash/Desktop/packetFiles/Results.csv', index=False)
    print("Results written to CSV")


def accuracyCalc(Y_test, Y_pred, lbl_keys, lbl_names=None):

    print("\nConfusion Matrix:\n ", confusion_matrix(Y_test, Y_pred, labels=lbl_keys))
    print("\nAccuracy: ", accuracy_score(Y_test, Y_pred) * 100)
    print("\nReport:\n ", classification_report(Y_test, Y_pred))