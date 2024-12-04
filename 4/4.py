from typing import List, Tuple
import numpy as np
import re 

def find_xmas(line:'np.array') -> int:
    findsr = re.findall(r'XMAS', ''.join(line))
    findsl = re.findall(r'SAMX', ''.join(line))
    return len(findsr)+ len(findsl)

def find_d_xmas(matrix:'np.array') -> bool:
    dm = ''.join(np.diagonal(matrix))
    idm = ''.join(np.diagonal(np.fliplr(matrix)))
    return dm in ('MAS', 'SAM') and idm in ('MAS', 'SAM')    
    

if __name__ == '__main__':
    with open('4/data.txt', 'r') as file:
        file_lines = file.readlines()
 
    
    matrix:List[List[str]] = []
    for i,line in enumerate(file_lines):
        matrix.append(list(line.replace('\n','')))

    matrix_nd = np.vstack(matrix)
    #matrix_nd = matrix_nd[0:5,0:5]
    n_rows = len(matrix_nd)
    n_columns = len(matrix_nd[0])

    # part one 
    counter_1 = 0
    for i in range(n_rows): # row
        counter_1+=find_xmas(matrix_nd[i,:])
    for j in range(n_columns): #column
        counter_1+=find_xmas(matrix_nd[:,j])
    for d in range(-n_columns, n_columns+1):
        counter_1+=find_xmas(matrix_nd.diagonal(d, axis1=0,axis2=1))
    for d in range(-n_rows, n_rows+1):    
        counter_1+=find_xmas(np.fliplr(matrix_nd).diagonal(d, axis1=0,axis2=1))
    print(f'{counter_1=}')

    # part two 
    counter_2 = 0
    for i in range(1,n_rows-1): # row
        for j in range(1,n_columns-1): # columns 
            if matrix_nd[i,j]=='A':
                if find_d_xmas(matrix_nd[i-1:i+2,j-1:j+2]):
                    counter_2 += 1
    print(f'{counter_2=}')
    

            

