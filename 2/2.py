from typing import List


def is_safe(line:List[int])-> bool:
    # The levels are either all increasing or all decreasing.
    # Any two adjacent levels differ by at least one and at most three.
    d1 = [line[i] - line[i+1] for i in range(len(line)-1)]   
    mad1 = max(d1)
    mid1 = min(d1)
    if (   (mad1 >0 and mid1 >0 and mad1 <=3 and mid1 >=1) 
        or (mad1 <0 and mid1 <0 and abs(mad1) >=1 and abs(mid1) <=3)):
        print(d1, line)
        return True 
    return False 

def is_safe_dampener(line:List[int]) -> bool:
    if is_safe(line):
        return True 
    else:
        for i in range(len(line)):
            line_copy = line.copy()
            line_copy.pop(i)
            if is_safe(line_copy):
                return True
    return False

if __name__ == '__main__':
    with open('2/data.txt', 'r') as file:
        lines = file.readlines()                  
    safe_count =0
    safe_count_d = 0
    for line in lines:
        line_list = line.split()
        line_int = [int(x) for x  in line_list if x.isnumeric()]
        if is_safe(line_int):
            safe_count +=1
        if is_safe_dampener(line_int):
            safe_count_d +=1

    print(safe_count)
    print(safe_count_d)