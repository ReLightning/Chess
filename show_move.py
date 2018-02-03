from field import print_field
from math_utilite import sign
import copy

defpar = ({'w' : (0, 4),
           'b' : (7, 4)},
          {'w' : (0, 0, 0),
          'b' : (0, 0, 0)},
          ('l', 8))
def start_parameter_2(par = ({'w' : (0, 4),
                              'b' : (7, 4)},
                             {'w' : (0, 0, 0),
                              'b' : (0, 0, 0)},
                             ('l', 8))):
    global cell_king, castling_control, trans, take_on_aisle
    cell_king = par[0]
    castling_control = par[1]
    trans = False
    take_on_aisle = par[2]
    
def det_cell_king(field):
    global cell_king
    cell_king = {field[x][y][0]:(x, y) for x in range(8) for y in range(8) if field[x][y][1]=='k'}
    
def king_and_castling(field, color, old, new, d):
    global cell_king, castling_control
    cell_king.update({color : (new[0], new[1])})
    storlg=new[1]-old[1]
    if abs(storlg) == 2:
        if d==1:
            field[new[0]][new[1]-sign(storlg)] = (color, 'r')
            field[new[0]][int(3.5+3.5*sign(storlg))] = ('_', '_')
        if d==-1:
            field[new[0]][new[1]-sign(storlg)] = ('_', '_')
            field[new[0]][int(3.5-3.5*sign(storlg))] = (color, 'r')
        cont = castling_control[color]    
        castling_control.update({color : (cont[0], cont[1]+d*(sign(storlg)*d+1), cont[2]+d*(-sign(storlg)*d+1))})    
    castling_control.update({color : (castling_control[color][0]+d, castling_control[color][1], castling_control[color][2])})

def rook(field, color, old, new, d):
    if (old[0] % 7 == 0 and old[1] % 7 == 0 and d == 1) or (new[0] % 7 == 0 and new[1] % 7 == 0 and d == -1):
        cont = castling_control[color]
        if (old[0] % 7 == 0 and old[1] % 7 == 0 and d == 1):
            castling_control.update({color : (cont[0], cont[1] + (sign(old[1]-3)+1), cont[2] + (-sign(old[1]-3)+1) )})
        if (new[0] % 7 == 0 and new[1] % 7 == 0 and d == -1):
            castling_control.update({color : (cont[0], cont[1] - (sign(new[1]-3)+1), cont[2] - (-sign(new[1]-3)+1) )})

def trans_pawn(color, old):
    col = sign(ord(color) - ord('l'))
    return True if (old[0] * col) % 7 == 6 else False

def take_on_aisle_pawn(color, old, new):
    global take_on_aisle
    if abs(new[0]-old[0]) == 2:
        take_on_aisle = (color, new[1])
    else:
        take_on_aisle = ('l', 8)
    return take_on_aisle

def take_on_aisle_move(field, color, old, new, fig, d, main):
    global take_on_aisle
    uncolor = 'w' if color=='b' else 'b'
    if main == 1:
        take_on_aisle_pawn(color, old, new)
    if abs(old[1]-new[1]) == 1:
        if field[new[0]][new[1]][0] == '_' and d == 1:
            field[old[0]][new[1]] = ('_', '_')
        if fig == ('_', '_') and d == -1:
            field[new[0]][old[1]] = (uncolor, 'p')

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


