from typing import *
from collections import defaultdict
from copy import deepcopy


class Stones:
    states:Dict[int, int]
    next_state_map:Dict[int, Iterable[int]]

    def __init__(self, stones_list:List[int]):
        hm = defaultdict(lambda:0)
        for s in stones_list:
            hm[s]+=1
        self.states = dict(hm)
        self.next_state_map = dict()
    
    def blink(self):
        n_state = dict()
        for s in self.states:
            if s in self.next_state_map:
                nsl = self.next_state_map[s]
            else:
                nsl = self.next_state(s)
                self.next_state_map[s] = nsl
            
            for ns in nsl:
                n_state[ns] = n_state.get(ns,0)+ self.states[s] # s stones will transition to ns 
        self.states = deepcopy(n_state)

    @staticmethod
    def next_state(s:int) -> Iterable[int]:
        #1. if 0 then 1
        #2. if even digits then split by two stones with first digits and last digits 
        #3. else multiply by 2024 
        if s==0:
            return [1]
        ss = str(s)
        lss = len(ss)
        mp = len(ss)//2
        if lss%2==0:
            return [int(ss[:mp]), int(ss[mp:])]
        return [s*2024]
    
    def __len__(self):
        return sum(self.states.values())

if __name__=='__main__':
    ol = [0,27,5409930,828979,4471,3,68524,170]
    stones = Stones(ol)
    for i in range(76):
        print(i, len(stones))
        stones.blink()