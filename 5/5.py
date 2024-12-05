from collections import defaultdict
from typing import Dict, List

def correct_pages(rules:Dict[int,List[int]], up:List[int])-> None:
    pass
if __name__ == '__main__':
    with open('5/data_test.txt', 'r') as file:
        lines = file.readlines()      
    
    rules:Dict[int,List[int]] = defaultdict(list)
    updates: List[int] = []
    for line in lines:
        if '|' in line:
            rnum=line.split('|')
            rules[int(rnum[0])].append(int(rnum[1]))
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
                    correct_pages(rules, up)
                    break
        if correct:
            total += up[len(up)//2]
        else:
            total_2 += up[len(up)//2]
        
    print(f'{total}')
    print(f'{total_2}')


