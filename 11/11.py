from typing import *

def blink(stones:List[int]) -> List[int]:
    #1. if 0 then 1
    #2. if even digits then split by two stones with first digits and last digits 
    #3. else multiply by 2024 
    res:List[int] = []
    for i in stones:
        if i ==0:
            res.append(1)
        elif len(str(i))%2==0:
            sr = str(i)
            res.extend([int(sr[:len(sr)//2]), int(sr[len(sr)//2:])])
        else:
            res.append(i*2024)
    return res 


if __name__ == '__main__':
    ol = [0]
    #ol = [0,27,5409930,828979,4471,3,68524,170]
    for i in range(24):
        print(i, len(ol))
        ol = blink(ol)
