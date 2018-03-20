from math_utilite import sign, col, det_myfigures
from move import all_possible_moves, exist_moves, check_field_on_shah
from show_move import start_parameter_2, move
from field import trans_field, print_field, make_field
import cProfile

value = {6 : 0,
         1 : 100,
         3 : 300,
         4 : 300,
         2 : 500,
         5 : 900}

w_pawn = [[ 0, 0, 0, 0, 0, 0 ,0 ,0],
          [ 4, 4, 4, 0, 0, 4, 4, 4],
          [ 6, 8, 2,10,10, 2, 8, 6],
          [ 6, 8,12,16,16,12, 8, 6],
          [ 8,12,16,24,24,16,12, 8],
          [12,16,24,32,32,24,16,12],
          [12,16,24,32,32,24,16,12],
          [ 0, 0, 0, 0, 0, 0, 0, 0]]

b_pawn = list(reversed(w_pawn))


def evaluation(position):
    field = position[0]
    player = position[1]
    w_figures = det_myfigures(field, 1)
    b_figures = det_myfigures(field, -1)
    w_figs = [fig for fig in w_figures.values()]
    b_figs = [fig for fig in b_figures.values()]
    figures = [w_figs.count(fig)-b_figs.count(-fig) for fig in range(1,7)]
    evaluate = 0
    for fig, kilk in enumerate(figures,1):
        evaluate += kilk*value[abs(fig)]
    for c in w_figures:
        if w_figures[c] == 1:
            evaluate += w_pawn[c[0]][c[1]]
    for c in b_figures:
        if b_figures[c] == -1:
            evaluate -= b_pawn[c[0]][c[1]]
    return evaluate*player


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
            player *= -1
            position, nextpos = detpos(field, player)
            tmp = -alphabeta(nextpos, depth-1, -beta, -alpha)
            start_parameter_2(position[2])    
            move(field, pos[1], pos[0], fig=fig, d=-1)
            player *= -1
            if tmp > alpha:
                alpha = tmp
                if depth == maxdepth:
                    bmove = pos
    unfigures = det_myfigures(field, -player)
    if possibles != [] or check_field_on_shah(field, player, unfigures):
        return alpha
    else:
        return 0         

transfig = {'Q' : 5,
            'R' : 2,
            'B' : 4,
            'N' : 3,}

def ftf(field, pos):
    return field[pos[1][0]][pos[1][1]], transfig[pos[2]] if pos[2] in ('Q', 'R', 'B', 'N') else 'p'

def detpos(field, player):
    from show_move import cell_king, castling_control, trans, take_on_aisle
    return (field, player, (cell_king, castling_control, trans, take_on_aisle)), (field, player, (cell_king, castling_control, False, take_on_aisle)),
    
def testing(position):
    global maxdepth, bmove, s
    bmove = 0
    s = 0
    player = position[1]
    start_parameter_2(position[2])
    maxdepth = 3
    score2 = alphabeta(position, maxdepth, -1001, 1001)
    print(s)
    print(score2*player / 100, bmove)
    return bmove

def testing_testing():
    testing((trans_field(), 1, ({1 : (0, 4),
                                         -1 : (7, 4)},
                                        {1 : (0, 0, 0),
                                         -1 : (0, 0, 0)},
                                        False,
                                        ('l', 8))))
if __name__=='__main__':   
    cProfile.run('testing_testing()')





        
