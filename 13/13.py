from typing import Tuple, List, Dict
from dataclasses import dataclass
import re
import numpy as np

@dataclass(repr=True)
class ClawMachine:
    A: Tuple[int, int]
    B: Tuple[int, int]
    target: Tuple[int, int]
    cost_a:int = 3
    cost_b: int = 1

def min_cost(cm:ClawMachine)-> float:
    future_cost_map:Dict[Tuple[int,int], int] =dict() # current position min cost ?
    
    def future_cost(x:int, y:int):
        nonlocal cm
        nonlocal future_cost_map
        
        if (x,y) in future_cost_map:
            return future_cost_map[(x,y)]

        if x > cm.target[0] or y> cm.target[1]:
            return np.inf
        if x==cm.target[0] and y == cm.target[1]:
            return 0
        result = min([cm.cost_a + future_cost(x+cm.A[0], y+cm.A[1]),
                      cm.cost_b + future_cost(x+cm.B[0], y+cm.B[1])
                      ])
        future_cost_map[(x,y)] = result
        return result 
    
    fc = future_cost(x=0,y=0)
    
    return fc  
    

if __name__ == '__main__':
    with open('13/data_t.txt', 'r') as file:
        lines = file.read().splitlines()
    
    m_params:List[Tuple] = []
    machines:List[ClawMachine] = []
    for line in lines:
        if 'Y' in line:
            line_d = re.findall(r'\d+', line)
            tup = (int(line_d[0]), int(line_d[1]))
            m_params.append(tup)
        else:
            cm = ClawMachine(A= m_params[0],B=m_params[1], target=m_params[2])
            machines.append(cm)
            m_params = []
    cost = 0
    for cm in machines:
        min_c= min_cost(cm)
        print(cm, min_c)
        if min_c < np.inf:
            cost += min_c 
    print(f'{cost = }')