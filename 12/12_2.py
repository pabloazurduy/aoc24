from typing import List, Tuple, Set
import itertools as it 

def search_region(pt:Tuple[int,int], gmap:List[List[str]]):
    region = set()
    perim = dict()

    def search(pt: Tuple[int, int]):
        nonlocal region 
        nonlocal perim
        nonlocal gmap 

        region |= set([pt])

        for i,j in [(0,1),(0,-1),(1,0),(-1,0)]:
            npi, npj = pt[0] + i, pt[1] + j
            if (0<= npi < len(gmap) and 
                0<= npj < len(gmap[0]) and 
                gmap[npi][npj] == gmap[pt[0]][pt[1]] 
                ):
                if (npi,npj) not in region:
                    search((npi,npj)) # if is the same region then search for new 
            else:
                perim[(pt[0],pt[1])] = perim.get((pt[0],pt[1]), 0) + 1  
    search(pt)
    return region, perim 

if __name__ == '__main__':
    with open('12/data.txt', 'r') as file:
        lines = file.read().splitlines() 
    gmap = []
    for l in lines:
        gmap.append(list(l))
    
    visited:Set[Tuple[int,int]]=set()
    total_cost = 0
    total_area = 0
    for pt in it.product(range(len(gmap)), range(len(gmap[0]))):
        if pt in visited:
            continue

        reg, per = search_region(pt, gmap)
        visited |= reg
        area = len(reg)
        perim = sum(per.values())
        cost = area*perim
        total_cost += cost
        total_area += area 
        if area > 1:
            print(f'{gmap[pt[0]][pt[1]]} {str(pt):<10} a:{area:>4} p:{perim:>4} c:{cost:>5} {[(u,v) for u,v in per.items() if v==4]}')
    
    print(f'{total_cost = }')
    print(f'{total_area = }')