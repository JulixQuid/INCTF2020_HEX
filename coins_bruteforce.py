
import hashlib
import itertools
import pandas as pd
import random
from pwn import *

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
                            print('rodrigo la chupa ',i)
                        bruteforcing = XXXX + str(coin_suffix)
                        bruteforcing = bruteforcing.encode()
                        intento = hashlib.sha256(bruteforcing).hexdigest()
                        if (intento == encrypted):
                            print('cracked!')
                            return intento


    def interaction(self):
        line=self.conn.recvline()
        print(line)
        encrypted=line.split()[2].decode()
        sufix=line.split()[0].decode().split('+')[1].split(')')[0]
        key=self.find_key(sufix,encrypted)
        self.conn.sendline(key[0:4])
        print(key[0:4])
        for i in range(10):
            lines=self.conn.recvline()
            print(lines)




if __name__ == "__main__":
    rod=coinMaster()
    rod.interaction()


