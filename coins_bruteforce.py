import hashlib
import random
from pwn import *
from time import sleep
import numpy as np
class coinMaster:
    def __init__(self):
        self.conn = remote('34.74.30.191', 1337)

    def find_key(self,coin_suffix,encrypted):
        i=0
        i+=1
        space='abcdefghijklmnopqrstuwxyzABCDEFGHIJKLMNOPQRSTUWXYZ1234567890'
        for i_1 in range(len(space)):
            for i_2 in range(len(space)):
                for i_3 in range(len(space)):
                    for i_4 in range(len(space)):
                        XXXX = space[i_1]+space[i_2]+space[i_3]+space[i_4]
                        i+=1
                        if(i%1000000==0):
                            print('# tries',i)
                        bruteforcing = XXXX + str(coin_suffix)
                        bruteforcing = bruteforcing.encode()
                        intento = hashlib.sha256(bruteforcing).hexdigest()
                        if (intento == encrypted):
                            print('cracked!')
                            return bruteforcing.decode()
    def interaction(self):
        line = self.conn.recvline().decode("utf-8")
        sufix = line[12:28]
        encrypted = line[33:-1]
        print(sufix, encrypted)
        key = self.find_key(sufix, encrypted)
        print(key)
        print(self.conn.recvline())
        self.conn.sendline(key[0:4])
        print(self.conn.recvline())
        print(self.conn.recvline())
        line=self.conn.recvline()
        self.binary_man(line.split()[-1])

    def binary_man(self,size):
        print(size)




    def jumpstart(self,line):
        encrypted = line.split()[2].decode()
        sufix = line.split()[0].decode().split('+')[1].split(')')[0]
        key = self.find_key(sufix, encrypted)
        print(key)

if __name__ == "__main__":
    rod = coinMaster()
    rod.interaction()


