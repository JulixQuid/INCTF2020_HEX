# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 23:09:55 2020

@author: julia
"""
import numpy as np
import pandas as pd
from sklearn import datasets, svm, metrics,  neural_network 
from sklearn.model_selection import train_test_split
from PIL import Image
import pickle
#from PIL import Image, ImageFilter
#import tesserocr
#from tesserocr import PyTessBaseAPI
import socket
import base64
import zlib
import codecs
from pwn import *


class digitMaster:
    def __init__(self):
        self.digits=pd.read_csv('mnist.csv')
        self.classifier = neural_network.MLPClassifier(hidden_layer_sizes=(290,))
        self.images=dict()
        self.labels=pd.DataFrame(columns=['x','y','label','prob'])
        self.classifier=self.load_model()
        self.aux=None
        
    def load_model(self):
        with open('digitsmodel.pkl', 'rb') as f:
            self.classifier = pickle.load(f)

    def save_model(self):
        with open('digitsmodel.pkl', 'rb') as f:
            self.classifier = pickle.dump(f)
        
    def load(self):
        color_img = np.asarray(Image.open("digits.jpg")) / 255
        img = np.mean(color_img, axis=2)
        for i in range(20):
            for j in range(20):
                self.images[(i,j)]=img[j*28:(j+1)*28,i*28:(i+1)*28].reshape(1,784)


    def classify(self):
        for coord,image in self.images.items():
            self.labels.loc[len(self.labels)]=[coord[0],coord[1],self.classifier.predict(image)[0],max(self.classifier.predict_proba(image))]
        

    def find_different(self):
        self.labels['max_prob']=self.labels.prob.apply(max)
        self.labels.sort_values('max_prob',ascending=False,inplace=True)
        self.aux=self.labels[self.labels.label!=self.labels.label.value_counts().index[0]]
        self.aux.x=(self.aux.x*28)+14
        self.aux.y=(self.aux.y*28)+14
        coords=[self.aux.iloc[0,0],self.aux.iloc[0,1],self.aux.iloc[0,0],self.aux.iloc[0,1],self.aux.iloc[0,0],self.aux.iloc[0,1]]
        coords=[str(i) for i in coords]
        coords=','.join(coords)
        coords='('+coords+')'
        return coords

    
    def training(self):
        X_train=self.digits[['col_{0}'.format(i+1) for i in range(784)]]
        y_train=self.digits['y']
        self.classifier.fit(X_train, y_train)
    
    def interaction(self):
        host = "34.70.233.147"
        port= 7777
        socket = remote(host,port)
        a = b'';
        while True:
        	b = socket.recv(timeout=1)
        	a = a+b
        	#print(len(a))
        	if len(b)==0:
        		break
        a.strip()
        a = a[2100:-2]
        #print("-->",a[0:10],"   ",a[-10:])
        de = codecs.decode((codecs.decode(a,"base64")),"zlib")
        fff = open("digits.jpg","wb")
        fff.write(de)
        self.load()
        self.classify()
        coords=self.find_different()
        socket.sendline(coords)
        print(socket.recvline())
        print(socket.recvline())
        print(socket.recvline())
        print(socket.recvline())
        print(socket.recvline())
        
        
        
rod=digitMaster()
rod.load_model()
rod.interaction()

