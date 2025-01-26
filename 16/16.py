from typing import List, Dict, Tuple, Set
from collections import namedtuple
import heapq

import numpy as np


State = namedtuple('State', ['r','c','dr','dc'])

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



def min_cost(start_state, lab:List[List]):
    frontier = PriorityQueue()
    frontier.push(start_state, 0)
    costs_dict: Dict[State, float] = {}
    
    while True:
        cs, past_cost = frontier.pop() # extract the min cost state
        # print(cs, past_cost)
        costs_dict[cs] = min(past_cost, costs_dict[cs]) if cs in costs_dict else past_cost # fucking cycles
        
        if lab[cs.r][cs.c] == 'E': # if terminal state 
            return past_cost, costs_dict, cs #end state

        front_state = State(r=cs.r + cs.dr, 
                            c=cs.c + cs.dc, 
                            dc=cs.dc, 
                            dr=cs.dr) # state in front 

        if (lab[front_state.r][front_state.c] != '#' and 
            front_state not in costs_dict.keys()): #only add to frontier if not explored before  
            # this is a greedy search, it works because if the cost is already stored on the dict means that 
            # It is the min cost to get to the state S   
            frontier.push(front_state, past_cost+1)
        
        #rotate 
        for ndr, ndc in [(-cs.dc, cs.dr), (cs.dc, -cs.dr)]:
            r_state = State(c=cs.c, r=cs.r, dr=ndr, dc=ndc) # rotated_state
            if r_state not in costs_dict.keys(): # only add to frontier if not explored before
                frontier.push(r_state, past_cost+1000)


parents_dict:Dict[State, List[State]] = dict()
def parents(s:State, cost_dict:Dict[State, float]):
    # cache
    global parents_dict 
    if s in parents_dict:
        return parents_dict[s]
    # calculation
    parents:List[State] = []
    bb = State(r=s.r-s.dr, c=s.c-s.dc, dc=s.dc, dr=s.dr)
    br = State(r=s.r, c=s.c, dc=-s.dr, dr=s.dc)
    bl = State(r=s.r, c=s.c, dc=s.dr, dr=-s.dc)
    
    for bs,c in [(bb,1),(br,1000),(bl,1000)]:
        if bs in cost_dict and cost_dict[bs] == cost_dict[s]-c:
            parents.append(bs)

    parents_dict[s] =  parents
    return parents 
    
Coord = namedtuple('Coord', ['r','c'])
states_path:Set[Tuple[int, int]] = set({})
def paths(node:State, cost_dict:Dict[State, float])->None:
    global states_path
    parents_n = parents(node, cost_dict)
    cand_parents = [p for p in parents_n if p in cost_dict and cost_dict[p]<cost_dict[node]] 
    
    
    for sn in cand_parents:
        states_path.add(Coord(sn.c, sn.r))
        paths(sn, cost_dict)
    
if __name__ == '__main__':
    with open('16/data.txt', 'r') as file:
        lines = file.read().splitlines()
    
    lab:List[List[str]] = []
    inst: List[str] = []
    for l in lines:
        lab.append(list(l))
    # get start state 
    lab_a = np.array(lab)
    start = list(zip(*np.where(lab_a=='S')))[0]
    start_state = State(r=start[0], c=start[1], dr=0, dc=1)

    cost, cost_dict, end_state = min_cost(start_state, lab)
    print(cost)
    
    # part 2 
    paths(end_state, cost_dict)
    lab_b = lab_a[:,:]
    for s in states_path:
        lab_b[s.c,s.r] = '0'

    print(np.array2string(lab_b, 
                          threshold=np.inf,
                          max_line_width=400,
                          formatter={'str_kind': lambda x: x}))
    print(len(states_path)+1)