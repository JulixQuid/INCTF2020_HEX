# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 23:09:55 2020

@author: julia
"""
import numpy as np
import pandas as pd
from sklearn import datasets, svm, metrics,  neural_network,linear_model
from sklearn.model_selection import train_test_split
from PIL import Image,ImageOps
import pickle
#from PIL import Image, ImageFilter
#import tesserocr
#from tesserocr import PyTessBaseAPI
import socket
import base64
import zlib
import codecs
from pwn import *
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D

interactions=[]

class digitMaster:
    def __init__(self):
        self.images=dict()
        self.labels=pd.DataFrame(columns=['x','y','label','prob'])
        self.aux=None
        self.input_shape = (28, 28, 1)
        
    def load_model(self):
        with open('digitsmodel.pkl', 'rb') as f:
            self.classifier = pickle.load(f)

    def save_model(self):
        with open('digitsmodel.pkl', 'wb') as f:
            pickle.dump(self.classifier,f)
        
    def load(self):
        
        color_img = np.asarray(Image.open("digits.jpg")) / 255
        img = np.mean(color_img, axis=2)
        for i in range(20):
            for j in range(20):
                self.images[(i,j)]=img[j*28:(j+1)*28,i*28:(i+1)*28]


    def classify(self):
        self.labels=pd.DataFrame(columns=['x','y','label','prob'])
        for coord,image in self.images.items():
            pred = model.predict(image.reshape(1, 28, 28, 1))
            self.labels.loc[len(self.labels)]=[coord[0],coord[1],pred.argmax(),pred.max()]
        

    def find_different(self):
        self.labels.sort_values('prob',ascending=False,inplace=True)
        self.aux=self.labels[self.labels.label!=self.labels.label.value_counts().index[0]]
        #self.aux.x=(self.aux.x*28)
        #self.aux.y=(self.aux.y*28)
        a0=0
        a1=min(1,len(self.aux)-1)
        a2=min(2,len(self.aux)-1)
        coords=[self.aux.iloc[a0,1],self.aux.iloc[a0,0],self.aux.iloc[a1,1],self.aux.iloc[a1,0],self.aux.iloc[a2,1],self.aux.iloc[a2,0]]
        coords=[str(int(i)) for i in coords]
        coords=','.join(coords)
        coords='('+coords+')'
        print(coords)
        return coords
    
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
        socket.recvline()
        while(True):
            print('reading')
            a=socket.recvline()
            interactions.append(a)
            print('decode')
            de = codecs.decode((codecs.decode(a[2:-2],"base64")),"zlib")
            fff = open("digits.jpg","wb")
            fff.write(de)
            self.load()
            self.classify()
            coords=self.find_different()
            socket.sendline(coords)
            a=socket.recvline()
        print(socket.recvline())#correct
        print(socket.recvline())
        print(socket.recvline())
        print(socket.recvline())
            
        
def nn():
    input_shape = (28, 28, 1)
    model = Sequential()
    model.add(Conv2D(28, kernel_size=(3,3), input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten()) # Flattening the 2D arrays for fully connected layers
    model.add(Dense(128, activation=tf.nn.relu))
    model.add(Dropout(0.2))
    model.add(Dense(40, activation=tf.nn.relu))
    model.add(Dropout(0.2))
    model.add(Dense(10,activation=tf.nn.softmax))

    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
    x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
    
    # Making sure that the values are float so that we can get decimal points after division
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    # Normalizing the RGB codes by dividing it to the max RGB value.
    x_train /= 255
    x_test /= 255
    print('x_train shape:', x_train.shape)
    print('Number of images in x_train', x_train.shape[0])
    print('Number of images in x_test', x_test.shape[0])
    model.compile(optimizer='adam', 
          loss='sparse_categorical_crossentropy', 
          metrics=['accuracy'])
    model.fit(x=x_train,y=y_train, epochs=10)
    return model


model=nn()
rod=digitMaster()
rod.interaction()




# Creating a Sequential Model and adding the layers


