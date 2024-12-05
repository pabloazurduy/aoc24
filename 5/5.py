from collections import defaultdict
from typing import Dict, List, Tuple
import networkx as nx

def correct_pages(up:List[int], order:List[int]) -> List[int]:
    return sorted(up, key=lambda x:order.index(x))

def topological_sort(rules_tuples:List[Tuple[int,int]]) -> List[int]:
    gr = nx.DiGraph(rules_tuples)
    return list(nx.topological_sort(gr))


if __name__ == '__main__':
    with open('5/data.txt', 'r') as file:
        lines = file.readlines()      
    
    rules:Dict[int,List[int]] = defaultdict(list)
    rules_tuples:List[Tuple[int,int]] = []
    updates: List[int] = []
    for line in lines:
        if '|' in line:
            rnum=line.split('|')
            rule = (int(rnum[0]),int(rnum[1]))
            rules[rule[0]].append(rule[1])
            rules_tuples.append(rule)
        elif line[0].isnumeric():
            nums = [int(k) for k in line.replace('\n','').split(',') if k.isnumeric()]
            updates.append(nums)
    
    total = 0
    total_2 =0
    for up in updates:
        correct = True 
        for i, p in enumerate(up):
            if p in rules: 
                if len(set(up[:i]) & set(rules[p])) >0:
                    print(f'{up} breaks {set(up[:i]) & set(rules[p])}')
                    correct =  False
                    # topological sort 
                    tps_list = topological_sort([r for r in rules_tuples if len(set(r) & set(up))>1])
                    up = correct_pages(up, tps_list)
                    break
        if correct:
            total += up[len(up)//2]
        else:
            total_2 += up[len(up)//2]
        
    print(f'{total}')
    print(f'{total_2}')


