from typing import List, Any

def expand(slots:List[int]) -> List[Any]:
    mem:List[Any] = []
    for i,v in enumerate(slots):
        a = [(i//2)]*v if i%2==0 else ['.']*v
        mem.extend(a) 
    return mem

def expand_nested(slots:List[int]) -> List[List[Any]]:
    mem:List[Any] = []
    for i,v in enumerate(slots):
        if v>0:
            a = [(i//2)]*v if i%2==0 else ['.']*v
            mem.append(a) 
    return mem

def compress(lmem:List[Any]) -> List[Any]:
    i = 0
    j = len(lmem)-1
    while i<j: 
        if lmem[i] != '.':
            i+=1
            continue
        if lmem[j] == '.':
            j-=1
            continue
        if lmem[i] == '.' and lmem[j] != '.': 
            lmem[i], lmem[j] = lmem[j], lmem[i]
        print(f'{i/len(lmem):.3f},{j/len(lmem):.3f}')
    return lmem

def compress_2(lmem:List[List[Any]]) -> List[Any]:
    i = 0 
    j = len(lmem)-1
    while j>0: 
        if i>j: # no possible to move, so next file 
            i = 0
            j -=1
        if '.' not in lmem[i] :
            i+=1
            continue
        if '.' in lmem[j]:
            j-=1
            continue
        if '.' in lmem[i] and '.' not in lmem[j]:
            #swap if possible, otherwise move to next empty space   
            lj = len(lmem[j])
            li = len(lmem[i])
            if lj <= li:
                ni0, ni1, nj = lmem[j], lmem[i][lj:], lmem[i][:lj]
                lmem[j] = nj
                lmem[i:i+1] = [ni0, ni1]
                i=0
            elif i<j:
                i+=1

        print(f'{i/len(lmem):.3f},{j/len(lmem):.3f}')
    
    # consolidate
    clmem:List[Any] = []
    for l in lmem:
        for k in l:
            clmem.append(k)
    return clmem    



def checksum(lmem:List[Any]) -> int:
    s=0
    for i,v in enumerate(lmem):
        if v != '.':
            s += i*int(v)
    return s 


if __name__ == '__main__':
    with open('9/data.txt','r') as fr:
        line = fr.read()
    slots = [int(s) for s in list(line)]
    mem = expand(slots)
    print(f'{len(mem) = } ')
    #print(mem)
    memc = compress(mem)
    print(checksum(memc))

    # part 2 
    mem = expand_nested(slots)
    print(f'{len(mem) = } ')
    memc = compress_2(mem)
    print(checksum(memc))
