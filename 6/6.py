from typing import Tuple
import numpy as np

def move_up(origin:Tuple[int,int], board:np.ndarray, trace:np.ndarray):
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

    return board, trace 


def is_finish(trace:np.ndarray)-> bool:
    border_sum = np.sum(trace[:,0] + trace[:,-1] + trace[-1,:] + trace[0,:])
    return  border_sum > 0 

if __name__ == '__main__':
    with open('6/data.txt', 'r') as file:
        lines = file.read().splitlines() 
    board_list = [list(l) for l in lines]
    board = np.array(board_list)
    trace = np.zeros(board.shape)

    while not is_finish(trace):
        origin_t = np.where(board=='^')
        origin = (int(origin_t[0][0]), int(origin_t[1][0]))
        board, trace = move_up(origin, board, trace)
        # print(board)
        # print(trace)
    np.where((board == '#') &( trace==1))
    print(trace.sum(), origin)