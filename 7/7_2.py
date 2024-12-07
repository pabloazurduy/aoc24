from typing import List 


def calib(nums:List[int], rt:int, target) -> bool:
    
    if len(nums)==0:
        return rt==target
    
    if rt > target:
        return False
        
    return (calib(nums[1:], rt=(rt + nums[0]), target=target) or 
            calib(nums[1:], rt=(rt * nums[0]), target=target) or 
            calib(nums[1:], rt=int(f'{rt}{nums[0]}'), target=target)
            )
    

if __name__ == '__main__':
    with open('7/data.txt', 'r') as file:
        lines = file.read().splitlines() 
    
    rsum = 0
    for line in lines:
        line_s = line.split(' ')    
        target = int(line_s[0].replace(':', ''))
        nums = [int(n) for n in line_s[1:]]
        
        if calib(nums, rt=0, target=target):
            rsum += target
            print(rsum, target)