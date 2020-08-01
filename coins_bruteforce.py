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
        print(self.conn.recvline())#'Give me XXXX:
        self.conn.sendline(key[0:4])
        print(self.conn.recvline())#There exists a coin minting ...
        print(self.conn.recvline())# empty line
        line=self.conn.recvline()
        print(line)
        print(line.split()[-1])
        sol=self.binary_console(line.split()[-1])
        self.conn.sendline(f'! {sol}')
        line = self.conn.recvline()
        print(line.split()[-1])
        sol = self.binary_console(line.split()[-1])
        self.conn.sendline(f'! {sol}')
        print(self.conn.recvline())
        print(self.conn.recvline())
        print(self.conn.recvline())
        print(self.conn.recvline())
        print(self.conn.recvline())
        print(self.conn.recvline())
        print(self.conn.recvline())

    def binary_console(self,size):
        print(self.conn.recvline())#Go ahead, ask some queries
        lower = 0
        upper = int(size.decode()) - 1
        solution=-1
        while (True):
            mid = (upper + lower) // 2
            pad_low = (mid - lower + 1) % 2
            pad_high = (upper - mid + 1) % 2
            if (upper - lower == 2):
                print('difference is 2 so...')
                self.conn.sendline(f'{lower} {lower+1}')
                line3 = self.conn.recvline()
                print(line3)
                sleep(1)
                num_3 = int(line1.split()[-1].decode())
                print(f'[{lower}, {lower+1}]-> {num_3}')

                self.conn.sendline(f'{upper-1} {upper}')
                line4 = self.conn.recvline()
                print(line4)
                sleep(1)
                num_4 = int(line1.split()[-1].decode())
                print(f'[{upper-1}, {upper}]-> {num_4}')

                if num_3 > num_4:
                    solution =lower
                    break
                if num_3 == num_4:
                    solution = lower+1
                    break
                if num_3 < num_4:
                    solution = upper
                    break
            if (upper - lower == 1):
                print('consecutive numbers ...')
                self.conn.sendline(f'{lower-2} {lower}')
                line3 = self.conn.recvline()
                print(line3)
                num_3 = int(line1.split()[-1].decode())
                print(f'[{lower-2}, {lower}]-> {num_3}')

                self.conn.sendline(f'{upper} {upper+2}')
                line4 = self.conn.recvline()
                print(line4)
                num_4 = int(line1.split()[-1].decode())
                print(f'[{upper}, {upper+2}]-> {num_4}')

                if num_3 < num_4:
                    print()
                    solution = upper
                    break
                if num_4 > num_3:
                    solution= lower
                    break
                if num_3 == num_4:
                    solution =-1
                    print('you f***ed it up man !')


            print('still a long way to go...')
            self.conn.sendline(f'{lower} {mid+pad_low}')
            line1 = self.conn.recvline()
            print(line1)
            sleep(1)
            num_1 = int(line1.split()[-1].decode())
            print(f'[{lower}, {mid+pad_low}]-> {num_1}')

            self.conn.sendline(f'{mid-pad_high} {upper}')
            line2 = self.conn.recvline()
            print(line2)
            sleep(1)
            num_2 = int((line2.split()[-1]).decode())
            print(f'[{mid-pad_high}, {upper}]-> {num_2}')

            print(f'{num_1}->{lower},{mid + pad_low},<<{mid}>>,{mid - pad_high},{upper}<-{num_2}')
            print('comparing cases...')


            if (num_1 == 0):
                print('upper half')
                lower = mid - pad_high
            if (0 == num_2):
                print('lower half')
                upper = mid + pad_low
            if (num_1 == num_2):
                print('damn bro... that escalated quickly!!!')
                lower = mid - pad_high
                upper = mid + pad_low
            if(lower==upper):
                solution = lower
                break

            print(f'new range: {lower},{(lower + upper) // 2},{upper}')
        print(f'solution {solution}')
        return solution

    def binary_man(numbers):
        lower=0
        upper=len(numbers)-1
        while(True):
            mid=(upper+lower)//2
            pad_low=(mid-lower)%2
            num_1=reduce(lambda i, j: i ^ j, numbers[lower:mid+pad_low])
            print(num_1)
            pad_high=(upper-mid)%2
            num_2 = reduce(lambda i, j: i ^ j, numbers[mid-pad_high:upper])
            print(num_2)
            print(f'{num_1}->{lower},{mid+pad_low},<<{mid}>>,{mid - pad_high},{upper}<-{num_2}')
            if(upper-lower==2):
                num_3 = numbers[lower] ^ numbers[mid]
                num_4 = numbers[mid] ^ numbers[upper]
                if num_3>num_4:
                    return lower
                if num_3==num_4:
                    return mid
                if num_3<num_4:
                    return upper
            if(upper-lower==1):
                num_3 = numbers[lower] ^ numbers[lower-1]
                num_4 = numbers[upper] ^ numbers[upper+1]
                if num_3 < num_4:
                    return upper
                if num_4 > num_3:
                    return lower
                if  num_3 == num_4:
                    return -1
            if(num_1==0):
                lower=mid-pad_high
            if(0==num_2):
                upper=mid+pad_low
            if(num_1==num_2):
                lower=mid-pad_high
                upper=mid-pad_low
            print(f'{lower},{(lower+upper)//2},{upper}')
            jaja=input()





if __name__ == "__main__":
    rod = coinMaster()
    rod.interaction()


