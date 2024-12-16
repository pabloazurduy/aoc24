from typing import *
import numpy as np
import itertools as it

type Coord = Tuple[int,int]

def nodes(p1:Coord, p2:Coord, shape:Tuple[int, int])-> Set[Coord]:
    
    nods:Set[Coord] = set()
    
    for sign in [-1,1]:
        n=0
        while True:
            node = p1[0]+sign*n*(p1[0]-p2[0]), p1[1] + sign*n*(p1[1]-p2[1])
            if shape[0]<=node[0] or node[0]<0 or shape[1]<=node[1] or node[1]<0:
                break
            nods=nods.union({node})
            n+=1
    return nods


if __name__ == '__main__':
    with open('8/data.txt','r') as fr:
        lines = fr.read().splitlines()
    n_lines= [list(line) for line in lines]
    a_map = np.array(n_lines)
    n_map = np.zeros(a_map.shape)
    c_ants = set(a_map[np.where(a_map != '.')]) # antenas classes
    
    nodes_s:Set[Coord]=set()
    for c in c_ants:
        coords = list(zip(*np.where(a_map==c)))
        pairs_a = list(it.combinations(coords, 2))
        for p in pairs_a:
            nodes_s= nodes_s.union(nodes(p[0], p[1], n_map.shape))
    for node in nodes_s:
        n_map[node] = 1
    print(n_map)
    print(len(nodes_s))