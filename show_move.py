from field import print_field
from math_utilite import sign, un, col
import copy


def start_parameter_2(par = ({'w' : (0, 4),
                              'b' : (7, 4)},
                             {'w' : (0, 0, 0),
                              'b' : (0, 0, 0)},
                             False,
                             ('l', 8))):
    global cell_king, castling_control, trans, take_on_aisle
    cell_king = par[0]
    castling_control = par[1]
    trans = par[2]
    take_on_aisle = par[3]
    
def det_cell_king(field):
    global cell_king
    cell_king = {field[x][y][0]:(x, y) for x in range(8) for y in range(8) if field[x][y][1]=='k'}
    return cell_king

def det_castling_control(field):
    global castling_control
    for color in ('w', 'b'):
        hor = 0 if color == 'w' else 7
        dk = 0 if field[hor][4] == (color, 'k') else 1
        dlr = 0 if field[hor][0] == (color, 'r') else 1
        drr = 0 if field[hor][-1] == (color, 'r') else 1
        castling_control[color] = (dk, dlr, drr)
    return castling_control
    
    
def king_and_castling(field, color, old, new, d):
    global cell_king, castling_control
    cell_king[color] = (new[0], new[1])
    storlg=new[1]-old[1]
    if abs(storlg) == 2:
        storlg = sign(storlg)
        rp = 7 if storlg*d == 2 else 0
        field[new[0]][new[1]-storlg] = (color, 'r') if d == 1 else ('_', '_')
        field[new[0]][rp] = ('_', '_') if d == 1 else (color, 'r')
        cont = castling_control[color]    
        castling_control[color] = (cont[0], cont[1]-storlg+d, cont[2]+storlg+d)
    castling_control[color] = (castling_control[color][0]+d, castling_control[color][1], castling_control[color][2])

def rook(field, color, old, new, d):
    global castling_control
    hor = 0 if color == 'w' else 7
    cont = castling_control[color]
    x, y = old if d == 1 else new
    if x == hor and y % 7 == 0:
        castling_control[color] = (cont[0], cont[1] + d*(-sign(y-3)+1), cont[2] + d*(sign(y-3)+1))

def trans_pawn(color, old):
    return True if (old[0] * col(color)) % 7 == 6 else False

def take_on_aisle_pawn(color, old, new):
    global take_on_aisle
    if abs(new[0]-old[0]) == 2:
        take_on_aisle = (color, new[1])
    else:
        take_on_aisle = ('l', 8)
    return take_on_aisle

def take_on_aisle_move(field, color, old, new, fig, d, main):
    global take_on_aisle
    if main == 1:
        take_on_aisle_pawn(color, old, new)
    if abs(old[1]-new[1]) == 1:
        if field[new[0]][new[1]][0] == '_' and d == 1:
            field[old[0]][new[1]] = ('_', '_')
        if fig == ('_', '_') and d == -1:
            field[new[0]][old[1]] = (un(color), 'p')

def move(field, old, new, fig=('_','_'), d=1, trans_fig='p', main=0):
    global trans, take_on_aisle
    color, figure= field[old[0]][old[1]]
    if figure == 'r':
        rook(field, color, old, new, d)
    if figure == 'k':
        king_and_castling(field, color, old, new, d)
    if trans == True:
        figure = 'p'
        trans = False
    if figure == 'p':
        trans = trans_pawn(color, old) if d == 1 else False 
        if trans == True:  
            figure = trans_fig    
        take_on_aisle_move(field, color, old, new, fig, d, main)
    if main == 1:
        trans = False
    field[new[0]][new[1]] = (color, figure)
    field[old[0]][old[1]] = fig


