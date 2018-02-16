from math_utilite import sign, un, col
from move import all_possible_moves, exist_moves, check_field_on_shah
from show_move import start_parameter_2, move
from field import trans_field, print_field
import cProfile

value = {'k' : 0,
         'p' : 1,
         'n' : 2.5,
         'b' : 3,
         'r' : 5,
         'q' : 10}

def evaluation(position):
    field = position[0]
    player = position[1]
    figures = {(x, y): field[x][y] for x in range(8) for y in range(8) if field[x][y][0]!='_'}
    evaluate = 0
    for x,y in figures:
        fig = field[x][y]
        color = col(fig[0])*col(player)
        evaluate += color*value[fig[1]]
    return evaluate


def alphabeta(position, depth, alpha, beta):
    global s, bmove
    if depth == 0:
        return evaluation(position)
    field, player = position[:-1]
    start_parameter_2(position[2])
    possibles = all_possible_moves(field, player)
    for pos in possibles:
        if alpha < beta:
            fig, trans_fig = ftf(field, pos)
            s += 1
            move(field, pos[0], pos[1], trans_fig=trans_fig)
            player = un(player)
            position, nextpos = detpos(field, player)
            tmp = -alphabeta(nextpos, depth-1, -beta, -alpha)
            start_parameter_2(position[2])    
            move(field, pos[1], pos[0], fig=fig, d=-1)
            player = un(player)
            if tmp > alpha:
                alpha = tmp
                if depth == maxdepth:
                    bmove = pos
    figures = {(x, y): field[x][y] for x in range(8) for y in range(8) if field[x][y][0]==un(player)}  
    if possibles != [] or check_field_on_shah(field, player, figures):
        return alpha
    else:
        return 0         

def ftf(field, pos):
    return field[pos[1][0]][pos[1][1]], pos[2] if pos[2] in ('q', 'r', 'b', 'n') else 'p'

def detpos(field, player):
    from show_move import cell_king, castling_control, trans, take_on_aisle
    return (field, player, (cell_king, castling_control, trans, take_on_aisle)), (field, player, (cell_king, castling_control, False, take_on_aisle)),
    
def testing(position):
    global maxdepth, bmove, s
    bmove = 0
    s = 0
    start_parameter_2(position[2])
    maxdepth = 4
    score2 = alphabeta(position, 4, -1001, 1001)
    print(s)
    return bmove

def testing_testing():
    testing((trans_field(), 'b', ({'w' : (0, 4),
                                         'b' : (7, 4)},
                                        {'w' : (0, 0, 0),
                                         'b' : (0, 0, 0)},
                                        False,
                                        ('l', 8))))
if True:   
    cProfile.run('testing_testing()')



        
