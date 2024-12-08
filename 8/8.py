from typing import *
import numpy as np
import itertools as it

def nodes(p1:Tuple[int,int], p2:Tuple[int,int])-> Tuple[Tuple[int,int], Tuple[int,int]]:
    n1 = p1[0]+(p1[0]-p2[0]), p1[1] + (p1[1]-p2[1])
    n2 = p2[0]+(p2[0]-p1[0]), p2[1] + (p2[1]-p1[1])
    return n1,n2


if __name__ == '__main__':
    with open('8/data.txt','r') as fr:
        lines = fr.read().splitlines()
    n_lines= [list(line) for line in lines]
    a_map = np.array(n_lines)
    n_map = np.zeros(a_map.shape)
    c_ants = set(a_map[np.where(a_map != '.')]) # antenas classes
    
    nodes_s:Set[Tuple[int,int]]=set()
    for c in c_ants:
        coords = list(zip(*np.where(a_map==c)))
        pairs_a = list(it.combinations(coords, 2))
        for p in pairs_a:
            nodes_s= nodes_s.union({*nodes(p[0], p[1])})
    nodes_l = {p for p in nodes_s if a_map.shape[0]>p[0]>=0 and a_map.shape[1]>p[1]>=0}
    for node in nodes_l:
        n_map[node] = 1
    print(n_map)
    print(len(nodes_l))