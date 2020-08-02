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
        """
            Attributes:
                images: dict
                dictionary for storing index in the "image matrix"  as
                    key : tuple of (rox,col)
                    value : 28x28 matrix
                labels: pd.DataFrame
                    Dataframe for storing the rox,col,predicted_label and probability.
                    columns:
                        x: int
                        y: int
                        label: int
                        prob: float between 0 and 1
                aux: pd:DataFrame
                    DataFrame for saving the images detected as different it will be
                    self.labels filtered by being != of the most frequent label in the image.


        """
        self.images=dict()
        self.labels=pd.DataFrame(columns=['x','y','label','prob'])
        self.aux=None
        self.input_shape = (28, 28, 1)
        
    def load(self):
        """
            opens the image set it to a range from 0 to 1
            and calculates the mean between the 3 RGB channels to transform it to
            grayscale and reduce dimension from 28x28x3 to 28x28
            then splits it in 400 28x28 matrixes and store them in the dict self.images:
                key: tuple of int  of coords  (row,column)
                value: np.array with dim 28x28 (matrix)

        """
        color_img = np.asarray(Image.open("digits.jpg")) / 255
        img = np.mean(color_img, axis=2)
        for i in range(20):
            for j in range(20):
                self.images[(i,j)]=img[j*28:(j+1)*28,i*28:(i+1)*28]


    def classify(self):
        """
            iterates over the images dict items and classify using the static model
            at the script for time problems model wasn't  in the class.

            pred is a vector with the probability of being on each class
            pred.shape=(10,1) or (1,10) or (10,) or (,10) not sure anymore lol
            but we take the index where the highest prob is pred.argmax and
            its value pred.max() and store it with the coords at the DataFrame
            columns:
                x: int
                y: int
                label: int
                prob: float between 0 and 1
        """
        self.labels=pd.DataFrame(columns=['x','y','label','prob'])
        for coord,image in self.images.items():
            pred = model.predict(image.reshape(1, 28, 28, 1))
            self.labels.loc[len(self.labels)]=[coord[0],coord[1],pred.argmax(),pred.max()]
        

    def find_different(self):
        """
        find the different using this algorithm:
            - step 1: sorted values on tha labels DataFrame by prob
            - step 2: filtering just the ones that dont belong to the most common label
            - step 3: taking the first three(we use the min because not all the times it
                      found three different) from the result of step 2
            - step 4: putting the coordinates in the format that the challenge required



        """
        self.labels.sort_values('prob',ascending=False,inplace=True) # step 1
        self.aux=self.labels[self.labels.label!=self.labels.label.value_counts().index[0]] #step 2
        #self.aux.x=(self.aux.x*28)
        #self.aux.y=(self.aux.y*28)
        a0=0#step 3.0
        a1=min(1,len(self.aux)-1) #step 3.1
        a2=min(2,len(self.aux)-1)#step 3.2
        #step 4
        coords=[self.aux.iloc[a0,1],self.aux.iloc[a0,0],self.aux.iloc[a1,1],self.aux.iloc[a1,0],self.aux.iloc[a2,1],self.aux.iloc[a2,0]]
        coords=[str(int(i)) for i in coords]
        coords=','.join(coords)
        coords='('+coords+')'
        # lol
        print(coords)
        return coords
    
    def interaction(self):
        """
            using pwn tools to automate the interaction
            - step 0: nc to the server
            - step 1: receive the first image and some more text
            - step 2: striping the image text
            - step 3: decoding base 64 and decompressing zlib **
                ** thanks to Phicar for doing the dirty work here
            - step 4: saving image to local storage (it could be probably done
                    in a more efficient way without saving and loading but it was
                    working fine so we let it be this way )
            - step 5: calling self.load description above
            - step 6: getting and sending coordinates
            - step 7: repeat from 1 to 6, 136 times

        """
        host = "34.70.233.147"
        port= 7777
        socket = remote(host,port) #step 0
        a = b'';
        while True: #step 1 receive the first image
        	b = socket.recv(timeout=1)
        	a = a+b
        	#print(len(a))
        	if len(b)==0:
        		break
        #step 2
        a.strip()
        a = a[2100:-2]
        #print("-->",a[0:10],"   ",a[-10:])
        de = codecs.decode((codecs.decode(a,"base64")),"zlib") # step 3
        fff = open("digits.jpg","wb") # step 4
        fff.write(de)
        self.load()#step 5
        self.classify() #step 6
        coords=self.find_different()#7
        socket.sendline(coords)
        socket.recvline()# confirmation of 1st success line
        n=0 #counting how many images we got
        while(True):
            print('reading')
            a=socket.recvline()
                if(len(a))<100000:#if line is not an image continue to get the flag
                    break
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
            print(a)
            n+=1
            print(cuenta)
        print(socket.recvline())#correct
        print(socket.recvline())
        print(socket.recvline())
        print(socket.recvline())
            
        
def nn():
    """
        - step 1: declare Convolutional NN (because every one know conv. layers rulz )
            and training all in the same function.
            I know dude, training and declaration must be in different functions
            but training took like 20 seconds and i was tired so who cares
            1 conv layer for spotting the digit
            and 3 dense to make sure we get all the complex patterns recognized
         properly fast and without overfitting.
        - step 2: getting data for training was done with MNIST dataset which is conveniently
            in the TF available datasets
        - step 3: training till gets 99% of accuracy as we have to solve +100 images
            with 3 attempst on each one thats like (1-(.01**3))**100 = .9999 success
            probability at 100 images,enough for me
        So we are good to go
    """
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
    model.fit(x=x_train,y=y_train, epochs=10) # at 10 epochs it reaches 99% off accuracy 
    return model


model=nn() #training model
rod=digitMaster() #declaring object
rod.interaction() # doing the magic






