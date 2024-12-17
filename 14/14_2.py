from dataclasses import dataclass
from typing import Tuple, List
import re
from copy import deepcopy

import numpy as np

@dataclass(repr=True)
class Robot:
    pos:Tuple[int,int]
    sp:Tuple[int,int]

    def move(self, shape:Tuple[int,int]):
        nx = (self.pos[0] + self.sp[0])%shape[0]
        ny = (self.pos[1] + self.sp[1])%shape[1]
        self.pos = (nx, ny)

@dataclass
class Map:
    robots:List[Robot]
    shape:Tuple[int,int]
    
    @property
    def to_array(self) -> np.ndarray:
        mp = np.zeros(self.shape)
        for rb in self.robots:
            mp[rb.pos[0], rb.pos[1]] += 1
        return mp.T
    
    def move(self, n:int =1) -> None:
        for _ in range(n):
            for rb in self.robots:
                rb.move(self.shape)
    @property
    def safety_factor(self) -> int:
        mp = self.to_array
        lx = mp.shape[0]//2
        ly = mp.shape[1]//2
        sf = (mp[:lx, :ly].sum() * 
              mp[lx+1:, ly+1:].sum() * 
              mp[:lx, ly+1:].sum() * 
              mp[lx+1:, :ly].sum())
        return int(sf )

if __name__ == '__main__':
    with open('14/data.txt', 'r') as file:
        lines = file.read().splitlines()
    
    robots:List[Robot] =[] 
    for l in lines:
        tups = re.findall(r'-?\d+,-?\d+', l)
        pos = [int(i) for i in tups[0].split(',')]
        speed = [int(i) for i in tups[1].split(',')]
        rb = Robot(tuple(pos), tuple(speed))
        robots.append(rb)
        print(rb)

    mp = Map(deepcopy(robots), shape=(101,103))
    min_sf = np.inf
    steps = 0
    for i in range(10000):
        if mp.safety_factor < min_sf:
            steps = i
            min_sf = mp.safety_factor
        mp.move(1)
        print(f'{i}, {mp.safety_factor = }')
    
    print(f'{min_sf = }, {steps = }')

    mp2 = Map(robots, shape=(101,103))
    mp2.move(steps)
    print(mp2.safety_factor)
    
    import matplotlib.pyplot as plt 
    plt.imshow(mp2.to_array, cmap='gray') 
    plt.show()