import re


if __name__ == '__main__':
    with open('3/data.txt', 'r') as file:
        file_str = file.read()
    
    mul_pattern = r'mul\(\d*,\d*\)'
    mul_strs = re.findall(mul_pattern, file_str)

    t_sum = 0
    for mul_s in mul_strs:
        nums = [int(u) for u in re.findall(r'\d*,\d*',mul_s)[0].split(',')]
        t_sum += (nums[0] * nums[1])
    print(f'{t_sum=}')
    
    #========# 
    # part 2 #
    #========#

    m2_pattern =r"mul\(\d*,\d*\)|do\(\)|don't\(\)"
    mul2_strs = re.findall(m2_pattern, file_str)
    #print(mul2_strs)

    t2_sum = 0 
    do = True
    for op in mul2_strs:
        if 'mul' in op and do:
            nums = [int(u) for u in re.findall(r'\d*,\d*',op)[0].split(',')]
            t2_sum += (nums[0] * nums[1])
            continue
        elif op == "don't()":
            do = False 
        elif op == "do()":
            do = True
    print(f'{t2_sum=}')