from typing import List, Tuple, Set, Dict
import itertools as it 
from collections import defaultdict

type Coord = Tuple[int,int]

R90 = {(0,1):(-1,0),
       (-1,0):(0,-1),
       (0,-1):(1,0),
       (1,0):(0,1)
}
def perp_dir(p_in:Coord, p_out:Coord) -> Tuple[int,int]:
    gr = (p_in[0]-p_out[0], p_in[1]-p_out[1])
    return R90[gr]


def move_forward(p_in:Coord, p_out:Coord):
    d = perp_dir(p_in, p_out)
    np_in = (p_in[0] + d[0], p_in[1] + d[1])
    np_out = (p_out[0] + d[0], p_out[1] + d[1])
    return np_in, np_out

def rotate(p_in:Coord, p_out:Coord, interior:List[Coord], outside:Dict[Coord, List[Coord]], taboo:List[Tuple[Coord,Coord]]) :
    for ext_flag in [True, False]: 
        for rd in [(-1,1), (1,1), (1,-1), (-1,-1)]:        
            if ext_flag: 
                # rotate exterior
                np_out = (p_out[0] + rd[0], p_out[1]+ rd[1])
                np_in = p_in
            else:
                # rotate interior
                np_in = (p_in[0] + rd[0], p_in[1]+ rd[1])
                np_out = p_out

            print(p_in, p_out, rd, np_in, np_out, np_in in interior, np_out in outside[np_in])
            if np_in in interior and np_out in outside[np_in] and (np_in, np_out) not in taboo:
                return np_in, np_out
    
    raise ValueError()
    
def bounds_from_start(i_in:Coord, i_out:Coord, 
                      interior:List[Coord], 
                      exterior:List[Coord], 
                      outside:Dict[Coord, List[Coord]],
                      taboo:List[Tuple[Coord, Coord]] #pairs of in, out that already visited
                      ):
    p_in, p_out = i_in, i_out # set first point 
    n_bounds = 0 #count is initialized on 0
    while True:
        # try to move forward
        np_in, np_out = move_forward(p_in, p_out)  
        if (np_in in interior and np_out in exterior): 
            # if I can move forward then move 
            p_in, p_out = np_in, np_out # move
            print(f'move forward {p_in, p_out}') 
        else:
            # if I can't move forward: then rotate
            np_in, np_out = rotate(p_in, p_out, interior, outside, taboo)
            print(f'rotate {p_in, p_out, np_in, np_out}')
            p_in, p_out = np_in, np_out # move
            n_bounds+=1 
        taboo.append((p_in,p_out))
        if p_in == i_in and p_out == i_out:
            break
    
    return n_bounds, taboo

def count_bounds(outside:Dict[Coord, List[Coord]]) -> int:
    exterior = list(it.chain.from_iterable(outside.values()))
    interior = list(outside.keys())
    
    # create border pairs
    border_pairs = []
    for k in outside: 
        border_pairs.extend([(k, p) for p in outside[k]])
    
    taboo =  []
    bounds = 0
    while len(set(border_pairs) - set(taboo))>0:
        # set initial points (one interior, one exterior)
        i_in, i_out = list(set(border_pairs) - set(taboo))[0]
        bnds, vis = bounds_from_start(i_in, i_out, interior, exterior, outside, taboo)
        print(i_in, i_out , bnds)
        bounds +=bnds
        taboo.extend(vis)

    return bounds


def search_region(pt:Coord, gmap:List[List[str]]):
    region = set()
    perim = dict()
    outside = defaultdict(lambda: list())

    def search(pt: Tuple[int, int]):
        nonlocal region 
        nonlocal perim
        nonlocal gmap 
        nonlocal outside

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
                outside[(pt[0],pt[1])].append((npi,npj)) 
    search(pt)
    n_bounds = count_bounds(outside)

    return region, perim, n_bounds 


if __name__ == '__main__':
    with open('12/data_t3.txt', 'r') as file:
        lines = file.read().splitlines() 
    gmap = []
    for l in lines:
        gmap.append(list(l))
    
    visited:Set[Coord]=set()
    total_cost = 0
    total_area = 0
    for pt in it.product(range(len(gmap)), range(len(gmap[0]))):
        if pt in visited:
            continue

        reg, per, n_bounds = search_region(pt, gmap)
        visited |= reg
        area = len(reg)
        cost = area*n_bounds
        total_cost += cost
        total_area += area 
        print(f'{gmap[pt[0]][pt[1]]} {str(pt):<10} a:{area:>4} n_sides:{n_bounds:>4} c:{cost:>5}')
    
    print(f'{total_cost = }')
    print(f'{total_area = }')