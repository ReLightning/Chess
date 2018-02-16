from math_utilite import sign, coords_to_square, un, col
from field import print_field
from show_move import *

def start_parameter_1():
    global cell_king, castling_control, trans, take_on_aisle
    cell_king = {'w' : (0, 4),
                 'b' : (7, 4)}
    castling_control = {'w' : (0, 0, 0),
                        'b' : (0, 0, 0)}
    trans = False
    take_on_aisle = ('l', 8)
    
def king_moves():
    return ((1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1))
def queen_moves():
    return rook_moves() + bishop_moves()
def rook_moves():
    return ((1,0), (-1,0), (0,1), (0,1))
def bishop_moves():
    return ((1,1), (-1,1), (1,-1), (-1,-1))
def knight_moves():
    return ((-2,-1), (-1,-2), (1,-2), (-2,1), (-1,2), (2,-1), (1,2), (2,1))
def pawn_moves():
    return ((1,0), (2,0), (1,1), (1,-1))

def castling(field):
    from show_move import castling_control
    colors = {'w' : 0, 'b' : 7}
    castl = [(color, side) for color in colors for side in (0, 1)
             if castling_control[color][0] == 0 and castling_control[color][side+1] == 0 and
             (side == 0 and field[colors[color]][5][0] == field[colors[color]][6][0] == '_' or
              side == 1 and field[colors[color]][3][0] == field[colors[color]][2][0] == field[colors[color]][1] == '_')]
    return [(color, ('0-0','0-0-0')[side]) for color, side in castl]
             

move_rules = {'k': king_moves,
              'q': queen_moves,
              'r': rook_moves,
              'b': bishop_moves,
              'n': knight_moves,
              'p': pawn_moves}

value = {'_' : 0,
         'k' : 20,
         'p' : 1,
         'n' : 2.5,
         'b' : 3,
         'r' : 5,
         'q' : 10}

def check_field_on_shah(field, player, figures):
    from show_move import cell_king
    for x, y in figures:
        if field[x][y][0] == un(player) and cell_king[player] in possible_moves_without_shah(field, (x, y), un(player)):
            return True
    return False


def possible_pawn_moves_without_shah(field, target, player):
    from show_move import take_on_aisle
    color = col(player)
    return [(target[0]+color*x, target[1]+y) for x, y in pawn_moves()
                if (y == 0 and field[target[0]+color][target[1]][0] == '_' and (x==1 or
                                                                               (x==2 and target[0]*color % 7 == 1
                                                                                and field[target[0]+2*color][target[1]][0] == '_'))) or
                   (y != 0 and -1<target[1]+y<8 and (field[target[0]+color][target[1]+y][0] == un(player) or
                               take_on_aisle == (un(player), target[1] + y) and (target[0] * color) % 7 == 4))]
    
def possible_moves_without_shah(field, target, player):
    figure = field[target[0]][target[1]][1]
    if figure=='p':
        all_moves = possible_pawn_moves_without_shah(field, target, player)
        return all_moves
    if figure == 'n' or figure == 'k':
        return [(target[0]+nex[0], target[1]+nex[1]) for nex in move_rules[figure]()
                 if -1<target[0]+nex[0]<8 and -1<target[1]+nex[1]<8 and field[target[0]+nex[0]][target[1]+nex[1]][0] != player]
    pm = [] 
    for nex in (move_rules[figure]()):
        cel = (target[0]+nex[0], target[1]+nex[1])
        while -1<cel[0]<8 and -1<cel[1]<8 and field[cel[0]][cel[1]][0] == '_':
            pm.append(cel)
            cel = (cel[0]+nex[0], cel[1]+nex[1])
        if -1<cel[0]<8 and -1<cel[1]<8 and field[cel[0]][cel[1]][0] == un(player):
            pm.append(cel)
    return pm
    
def possible_ordinary_moves(field, target, player, figures):
    poss_ordinary = []
    for x, y in possible_moves_without_shah(field, target, player):
        fig = field[x][y]
        trans = trans_pawn(player, target) and field[target[0]][target[1]][1] == 'p'
        move(field, target, (x, y))
        if not check_field_on_shah(field, player, figures):
            if not trans:
                if field[x][y][1] == 'p' and target[1]-y != 0 and fig[0] == '_':
                    poss_ordinary.append((x, y, coords_to_square((x, y))+'a'))
                else:
                    poss_ordinary.append((x, y, coords_to_square((x, y))))
            else:
               for pot_fig in ('q','r','b','n'):
                   poss_ordinary.append((x, y, coords_to_square((x, y))+pot_fig))
        move(field, (x, y), target, fig, -1)
    return poss_ordinary

def possible_castling(field, target, figures, player):
    figure = field[target[0]][target[1]][1]
    poss_castl = []
    for x, y in [(target[0], target[1]+2*(-1)**('0-0', '0-0-0').index(castl)) for castl in ('0-0', '0-0-0') if figure == 'k' and ((player, castl) in castling(field))]:
        if not check_field_on_shah(field, player, figures):
            move(field, target, (x, 4+sign(y-4)))
            if not check_field_on_shah(field, player, figures):
                move(field, (x, 4+sign(y-4)), target, d=-1)
                move(field, target, (x, y))
                if not check_field_on_shah(field, player, figures):
                    poss_castl.append((x, y, ('0-0', '0-0-0')[(sign(y-4)-1)//2]))
                move(field, (x, y), target, d=-1)
            else:
                move(field, (x, 4+sign(y-4)), target, d=-1)           
    return poss_castl

def possible_moves(field, target, player, unfigures):
    poss_ordinary = possible_ordinary_moves(field, target, player, unfigures)
    poss_castl = possible_castling(field, target, unfigures, player)
    return poss_ordinary + poss_castl

def exist_moves(field, player, unfigures):
    figures = {(x, y): field[x][y] for x in range(8) for y in range(8) if field[x][y][0]==player}
    for figure in figures:
        for pm in possible_moves(field, figure, player, unfigures):
            return True
    return False

def all_possible_moves(field, player):
    figures = {(x, y): field[x][y] for x in range(8) for y in range(8) if field[x][y][0]==player}
    unfigures = {(x, y): field[x][y] for x in range(8) for y in range(8) if field[x][y][0]==un(player)}
    apm = []
    for target in figures:
        for tpm in possible_moves(field, target, player, unfigures):
            delval = value[field[tpm[0]][tpm[1]][1]] - value[field[target[0]][target[1]][1]] if field[tpm[0]][tpm[1]][1] != '_' else -30
            apm.append((delval, target, tpm[:2], tpm[2][-1]))
    return sortka(apm)

def sortka(apm):
    apm.sort()
    apm = [(d1,d2,d3) for _,d1,d2,d3 in apm]
    apm.reverse()
    return apm

def field_legal(field, player):
    figures = {(x, y): field[x][y] for x in range(8) for y in range(8) if field[x][y][0]==player}
    kings = [field[x][y][0] for x in range(8) for y in range(8) if field[x][y][1]=='k']
    return (kings == ['w', 'b'] or kings == ['b', 'w']) and not check_field_on_shah(field, un(player), figures)


    
        
