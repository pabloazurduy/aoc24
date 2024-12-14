from typing import List , Tuple, Set
import numpy as np

def n_trail(init:Tuple[int, int], nmap:np.ndarray ):
    ends:Set[Tuple[int, int]] = set()

    def trail(init:Tuple[int, int], nmap:np.ndarray):
        nonlocal ends
        if nmap[init] == 9:
            ends = ends | set([init])
            return 
        valid_np:List[Tuple[int,int]]= []
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx = init[0]+dx
            ny = init[1]+dy
            if (0<=nx <nmap.shape[0] and 
                0<=ny <nmap.shape[1] and 
                nmap[nx, ny] == nmap[init]+1):
                valid_np.append((nx,ny))
                trail((nx,ny), nmap)
    trail(init, nmap)
    return len(ends)

if __name__ == '__main__':
    with open('10/data.txt', 'r') as file:
        lines = file.read().splitlines() 
    
    lmap:List[List[int]] = []
    for l in lines:
        lmap.append([int(v) if v.isnumeric() else -1 for v in list(l) ])
    
    nmap = np.vstack(lmap)
    locs = np.where(nmap==0)
    zeroes = list(zip(locs[0], locs[1]))
    score=0
    for zero in zeroes:
        score+= n_trail(zero, nmap)
    print(score)