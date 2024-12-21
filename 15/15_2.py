from dataclasses import dataclass
from typing import List, Tuple
import re 

import numpy as np

#might not work 

@dataclass
class Warehouse:
    ma: np.ndarray

    def __init__(self, ma:List[List[str]]):
        self.ma = np.array(ma)

    def __str__(self) :
        return np.array2string(self.ma, separator='',
                               threshold=np.inf,
                               max_line_width=400,
                                prefix='',
                                suffix='', 
                                formatter={'str_kind': lambda x: x})
    @property
    def sub(self) -> Tuple[int, int]:
        return list(zip(*np.where(self.ma =='@')))[0]
    
    def move(self, dir:str) -> None:
        if dir in ['<', '>']:
            self.ma[self.sub[0], :] = self.move_horizontal(self.ma[self.sub[0], :], dir=1 if dir=='>' else -1) 
        elif dir in ['v', '^']:
            self.move_vertical(dir == '^') 
    

    def move_vertical(self, up:bool) -> None:
        if up is False:
            self.ma = np.flip(self.ma, 0)
        
        def is_mobile(x:List[int], y:int) -> bool:
            if len(x)==1 and self.ma[y,x] == '[':
                return is_mobile(x+[x[0]+1],y)
            if len(x)==1 and self.ma[y,x] == ']':
                return is_mobile(x+[x[0]-1],y)
            if all(self.ma[y-1,i] == '.' for i in x):
                return True 
            elif any(self.ma[y-1,i] == '#' for i in x):
                return False
            else:
                return all([is_mobile(x=[i], y=y-1) for i in x])
            
        def move_up(x:List[int], y:int):
            print(f'move up {x}, {y}, {self.ma[y,x]}')
            if len(x)==1 and self.ma[y,x] == '[':
                move_up(sorted(x+[x[0]+1]),y)
                return 
            if len(x)==1 and self.ma[y,x] == ']':
                move_up(sorted(x+[x[0]-1]),y)
                return 
            if len(x)==1 and self.ma[y,x] == '.':
                return 
            if all(self.ma[y-1,i] == '.' for i in x):
                # if empty space then move 
                self.ma[y-1,x], self.ma[y,x] =  self.ma[y,x], self.ma[y-1,x]
            else:
                if len(x)==2 and self.ma[y-1,x[0]] == '[' and self.ma[y-1,x[1]] == ']':
                    move_up(x,y-1)
                else:
                    for i in x:
                        move_up([i],y-1)
                move_up(x,y)

        if is_mobile(x=[self.sub[1]], y=self.sub[0]):            
            move_up(x=[self.sub[1]],y= self.sub[0])

        if up is False:
            self.ma = np.flip(self.ma, 0)

    @staticmethod
    def move_horizontal(arry:np.ndarray, dir:int) -> np.ndarray:
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
        return int(sum([u*100 + v for (u,v) in np.argwhere(self.ma =='[')]))

p2_dict = {'#':['#','#'],
           'O':['[',']'],
           '.':['.','.'],
           '@':['@','.'],

}

if __name__ == '__main__':
    with open('15/data.txt', 'r') as file:
        lines = file.read().splitlines()
    
    map_s:List[List[str]] = []
    inst: List[str] = []
    for l in lines:
        if '#' in l:
            chars = list(l)
            row = [ i  for char in chars for i in p2_dict[char] ]
            
            map_s.append(row)
        elif re.match(r'[<^>v]', l):
            inst.extend(list(l))
    wh = Warehouse(map_s)
    for i, j in enumerate(inst):
        print(i, j)
        wh.move(j)
        print(wh)
        
    print(f'{wh.gps_sum = }')