from typing import List, Dict, Tuple
from collections import namedtuple
import heapq

import numpy as np


State = namedtuple('State', ['r','c','dr', 'dc'])

class PriorityQueue:
    def __init__(self):
        self._queue = []

    def push(self, item:State, cost:float):
        heapq.heappush(self._queue, (cost, item))

    def pop(self) -> Tuple[State, float]:
        item = heapq.heappop(self._queue)
        return item[1], item[0]

    def empty(self) -> bool:
        return len(self._queue) == 0



def min_cost(lab:List[List]):
    # get start state 
    lab_a = np.array(lab)
    start = list(zip(*np.where(lab_a=='S')))[0]
    start_state = State(r=start[0], c=start[1], dr=0, dc=1)
    
    # initialize variables for UCS 
    # it has to be UCS because DP don't work with cycles 
    frontier = PriorityQueue()
    frontier.push(start_state, 0)
    costs: Dict[State, float] = {}
    
    while True:
        cs, past_cost = frontier.pop() # extract the min cost state
        print(cs, past_cost)
        costs[cs] =  past_cost
        
        if lab[cs.r][cs.c] == 'E': # if terminal state 
            return past_cost, costs

        front_state = State(r=cs.r + cs.dr, 
                            c=cs.c + cs.dc, 
                            dc=cs.dc, 
                            dr=cs.dr) # state in front 

        if (lab[front_state.r][front_state.c] != '#' and front_state not in costs.keys()):      
            frontier.push(front_state, past_cost+1)
        
        #rotate 
        for ndr, ndc in [(-cs.dc, cs.dr), (cs.dc, -cs.dr)]:
            r_state = State(c=cs.c, r=cs.r, dr=ndr, dc=ndc) # rotated_state
            if r_state not in costs.keys():
                frontier.push(r_state, past_cost+1000)


if __name__ == '__main__':
    with open('16/data_t1.txt', 'r') as file:
        lines = file.read().splitlines()
    
    lab:List[List[str]] = []
    inst: List[str] = []
    for l in lines:
        lab.append(list(l))
    cost, cost_dict = min_cost(lab)
    print(cost)


