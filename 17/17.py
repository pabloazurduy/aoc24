
from collections import namedtuple

OPERATIONS = {0:'adv', # int(A/2**comb)-> A
              1:'bxl', # XOR(B, literal(comb)) -> B
              2:'bst', # comb%8 -> B
              3:'jnz', # if A==0 -> pass, else: i = literal(comb) # i doesn't increase!!
              4:'bxc', # XOR(B,C)-> B 
              5:'out', # comb%8 -> RETURN 
              6:'bdv', # int(A/2**comb)-> B
              7:'cdv', # int(A/2**comb)-> C
}


Prog = namedtuple('Prog', ['a','b','c','p'])

def run_program(p:Prog):
    a,b,c,program = p.a, p.b, p.c, p.p
    def val(cb):
        nonlocal a, b, c 
        if cb <=3:
            return cb 
        if cb==4:
            return a
        if cb==5:
            return b
        if cb==6:
            return c        
    i=0
    while i < len(program): # while pointer i still on the tape
        cb = program[i+1]
        op = program[i]
        
        if op in [0,6,7]:
            v = int(a/2**val(cb))
            if op == 0:
                a= v 
            if op == 6:
                b =v
            if op ==7:
                c=v 
        i += 2 
    p.a, p.b, p.c = a,b,c


if __name__ == '__main__':
    with open('17/test.txt', 'r') as file:
        lines = file.read().splitlines()
    
    a = int(lines[0].split(': ')[1])
    b = int(lines[1].split(': ')[1])
    c = int(lines[2].split(': ')[1])

    program = [int(x) for x in lines[4].split(': ')[1].split(',')]

    print(A,B,C,program)