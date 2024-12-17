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

def min_cost(cm: ClawMachine) -> float:
    # Set up the system of equations as matrices
    A = np.array([[cm.A[0], cm.B[0]],
                  [cm.A[1], cm.B[1]]])
    b = np.array([cm.target[0], cm.target[1]])
    
    try:
        # Solve the system of equations
        na, nb = np.linalg.solve(A, b)
        
        # Check if solution has non-negative integers
        if (na >= 0 and nb >= 0 and
                round(na,0)*cm.A[0]+round(nb,0)*cm.B[0] == cm.target[0]
            and round(na,0)*cm.A[1]+round(nb,0)*cm.B[1] == cm.target[1]
            ):
            return int(round(na,0) * cm.cost_a + round(nb,0) * cm.cost_b)
        else:
            print(na,nb) 
            return np.inf
    except np.linalg.LinAlgError:
        return np.inf


if __name__ == '__main__':
    with open('13/data.txt', 'r') as file:
        lines = file.read().splitlines()
    
    m_params:List[Tuple] = []
    machines:List[ClawMachine] = []
    for line in lines:
        if 'Y' in line:
            line_d = re.findall(r'\d+', line)
            tup = (int(line_d[0]), int(line_d[1]))
            m_params.append(tup)
        else:
            cm = ClawMachine(A= (m_params[0][0], 
                                 m_params[0][1]),
                             B= (m_params[1][0],
                                 m_params[1][1],
                                 ), 
                             target=( 1e13+m_params[2][0],  #1e13+
                                      1e13+m_params[2][1])) #1e13+
            machines.append(cm)
            m_params = []
    cost = 0
    for cm in machines:
        min_c= min_cost(cm)
        print(cm, min_c)
        if min_c < np.inf:
            cost += min_c 
    print(f'{cost = }')