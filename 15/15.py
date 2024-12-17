from dataclasses import dataclass
from typing import List, Tuple
import re 

import numpy as np

@dataclass
class Warehouse:
    ma: np.ndarray

    def __init__(self, ma:List[List[str]]):
        self.ma = np.array(ma)

    @property
    def sub(self) -> Tuple[int, int]:
        return list(zip(*np.where(self.ma =='@')))[0]
    
    def move(self, dir:str) -> None:
        if dir in ['<', '>']:
            self.ma[self.sub[0], :] = self.move_array(self.ma[self.sub[0], :], dir=1 if dir=='>' else -1) 
        elif dir in ['v', '^']:
            self.ma[ :, self.sub[1]] = self.move_array(self.ma[ :, self.sub[1]], dir= 1 if dir=='v' else -1) 

    @staticmethod
    def move_array(arry:np.ndarray, dir:int) -> np.ndarray:
        
        if dir==-1: # reversed 
            arry = arry[::-1]

        narry = arry.copy()
        s_i= np.argwhere(arry=='@')[0][0]
        b_j = np.argwhere(arry=='#')[np.argwhere(arry=='#')>s_i][0]
        if np.any(arry[s_i:b_j]=='.'):    
            e_j = np.argwhere(arry[s_i:b_j]=='.')[0][0] + s_i
            narry[s_i+1:e_j+1] = arry[s_i:e_j]
            narry[s_i] = '.'

        if dir==-1: # reversed  back
            narry = narry[::-1]
        
        return narry
    
    @property 
    def gps_sum(self) -> int:
        return int(sum([u*100 + v for (u,v) in np.argwhere(self.ma =='O')]))

if __name__ == '__main__':
    with open('15/data.txt', 'r') as file:
        lines = file.read().splitlines()
    
    map_s:List[List[str]] = []
    inst: List[str] = []
    for l in lines:
        if '#' in l:
            map_s.append(list(l))
        elif re.match(r'[<^>v]', l):
            inst.extend(list(l))
    wh = Warehouse(map_s)
    for i in inst:
        print(i)
        wh.move(i)
        print(np.array2string(wh.ma, separator=' ',
                     prefix='',
                     suffix='', 
                     formatter={'str_kind': lambda x: x}).replace('[', ' ').replace(']', ''))
        
    print(f'{wh.gps_sum = }')