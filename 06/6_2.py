from typing import Tuple, List
import numpy as np

def move_up(origin:Tuple[int,int], board:np.ndarray, trace:np.ndarray, orient:int):
    # move up, 
    obstacles = np.where(board[:origin[0],origin[1]] =='#')[0]
    if len(obstacles)>0:
        l_up = int(obstacles[-1]) # first apparition 
        new_origin = (l_up+1, origin[1])  # if len(l_up) > 0 
    else:
        new_origin=(0,origin[1])

    trace[new_origin[0]:origin[0]+1,origin[1]] = 1

    # update origin
    board[origin] = '.'
    board[new_origin] = '^'

    # rotate 90 degrees 
    trace = np.rot90(trace)
    board = np.rot90(board)
    orient = (orient+1)%4

    return board, trace, orient  


def is_finish(trace:np.ndarray)-> bool:
    border_sum = np.sum(trace[:,0] + trace[:,-1] + trace[-1,:] + trace[0,:])
    return  border_sum > 0 

if __name__ == '__main__':
    with open('6/data.txt', 'r') as file:
        lines = file.read().splitlines() 
    board_list = [list(l) for l in lines]
    board = np.array(board_list)
    trace = np.zeros(board.shape)
    orient = 0

    loops_count =0
    empty_places = np.where(board=='.')
    empty_places_tp = [(int(empty_places[0][i]), int(empty_places[1][i])) for i in range(len(empty_places[0]))]
    for (i,j) in empty_places_tp:
        print(i,j)
        board[i,j] = '#'
        
        origins:List[Tuple[int, int]] = []
        while not is_finish(trace):
            origin_t = np.where(board=='^')
            origin = (int(origin_t[0][0]), int(origin_t[1][0]))
            if (origin,orient) in origins:
                loops_count+=1 
                print('loop found ')
                break 
            else:
                origins.append((origin, orient))
            board, trace, orient = move_up(origin, board, trace, orient)
        
        # reset board
        board = np.array(board_list)
        trace = np.zeros(board.shape)
        orient = 0

    print(f'{loops_count = }')