from typing import List, Dict, Tuple
from collections import namedtuple
import heapq

import numpy as np

class PriorityQueue:
    def __init__(self):
        self._queue = []

    def push(self, item, cost):
        heapq.heappush(self._queue, (cost, item))

    def pop(self):
        item = heapq.heappop(self._queue)
        return item[1], item[0]

    def empty(self):
        return len(self._queue) == 0

    def update(self, item, cost):
        self._queue = [(p, i) for p, i in self._queue if i != item] # Remove existing item if present
        heapq.heapify(self._queue)
        self.push(item, cost) # Add item with new cost

State = namedtuple('State', ['x','y','d'])


def min_cost(lab:List[List]):
    # get start state 
    lab_a = np.array(lab)
    start = list(zip(*np.where(lab_a=='S')))[0]
    start_state = State(x=start[1], y=start[0], d=0)
    
    # initialize variables for UCS 
    dir = {0:(1,0),
           1:(0,1),
           2:(-1,0),
           3:(0,-1), 
          }
    # it has to be UCS because DP don't work with cycles 
    frontier = PriorityQueue()
    frontier.update(start_state, 0) # initialize start with cost 0

    while True:
        new_state, past_cost = frontier.pop() # extract the min cost state
        #print(new_state, past_cost)

        if lab[new_state.y][new_state.x] == 'E': # if terminal state 
            return past_cost 

        possible_actions = [(State(new_state.x , new_state.y, (new_state.d+1)%4), 1000), # 90 deg
                            (State(new_state.x , new_state.y, (new_state.d-1)%4), 1000), # -90 deg
        ]
        if lab[new_state.y+ dir[new_state.d][1]][new_state.x + dir[new_state.d][0]] != '#':
            possible_actions.append((State(new_state.x + dir[new_state.d][0], new_state.y+ dir[new_state.d][1], new_state.d), 1))

        for new_state, cost in possible_actions:
            frontier.update(new_state, past_cost + cost)


if __name__ == '__main__':
    with open('16/data_t1.txt', 'r') as file:
        lines = file.read().splitlines()
    
    lab:List[List[str]] = []
    inst: List[str] = []
    for l in lines:
        lab.append(list(l))
    print(min_cost(lab))
