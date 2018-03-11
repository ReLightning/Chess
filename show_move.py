from field import print_field
from math_utilite import sign, col


def start_parameter_2(par = ({1 : (0, 4),
                              -1 : (7, 4)},
                             {1 : (0, 0, 0),
                              -1 : (0, 0, 0)},
                             False,
                             ('l', 8))):
    global cell_king, castling_control, trans, take_on_aisle
    cell_king = par[0]
    castling_control = par[1]
    trans = par[2]
    take_on_aisle = par[3]
    
def det_cell_king(field):
    global cell_king
    cell_king = {sign(field[x][y]):(x, y) for x in range(8) for y in range(8) if abs(field[x][y])==6}
    return cell_king

def det_castling_control(field):
    global castling_control
    for color in (1, -1):
        hor = 0 if color == 1 else 7
        dk = 0 if field[hor][4] == 6*color else 1
        dlr = 0 if field[hor][0] == 2*color else 1
        drr = 0 if field[hor][-1] == 2*color else 1
        castling_control[color] = (dk, dlr, drr)
    return castling_control
    
    
def king_and_castling(field, color, old, new, d):
    global cell_king, castling_control
    cell_king[color] = (new[0], new[1])
    storlg=new[1]-old[1]
    if abs(storlg) == 2:
        storlg = sign(storlg)
        rp = 7 if storlg*d == 2 else 0
        field[new[0]][new[1]-storlg] = 2*color if d == 1 else 0
        field[new[0]][rp] = 0 if d == 1 else 2*color
        cont = castling_control[color]    
        castling_control[color] = (cont[0], cont[1]-storlg+d, cont[2]+storlg+d)
    castling_control[color] = (castling_control[color][0]+d, castling_control[color][1], castling_control[color][2])

def rook(field, color, old, new, d):
    global castling_control
    hor = 0 if color == 1 else 7
    cont = castling_control[color]
    x, y = old if d == 1 else new
    if x == hor and y % 7 == 0:
        castling_control[color] = (cont[0], cont[1] + d*(-sign(y-3)+1), cont[2] + d*(sign(y-3)+1))

def trans_pawn(color, old):
    return True if (old[0] * color) % 7 == 6 else False

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
        if field[new[0]][new[1]] == 0 and d == 1:
            field[old[0]][new[1]] = 0
        if fig == 0 and d == -1:
            field[new[0]][old[1]] = -color

def move(field, old, new, fig=0, d=1, trans_fig=1, main=0):
    global trans, take_on_aisle
    color = sign(field[old[0]][old[1]])
    figure = abs(field[old[0]][old[1]])
    if figure == 2:
        rook(field, color, old, new, d)
    if figure == 6:
        king_and_castling(field, color, old, new, d)
    if trans == True:
        figure = 1
        trans = False
    if figure == 1:
        trans = trans_pawn(color, old) if d == 1 else False 
        if trans == True:  
            figure = trans_fig    
        take_on_aisle_move(field, color, old, new, fig, d, main)
    if main == 1:
        trans = False
    field[new[0]][new[1]] = color*figure
    field[old[0]][old[1]] = fig



