from math_utilite import sign, coords_to_square, col
from field import print_field
from show_move import *


def start_parameter_1():
    global cell_king, castling_control, trans, take_on_aisle
    cell_king = {1 : (0, 4),
                 -1 : (7, 4)}
    castling_control = {1 : (0, 0, 0),
                        -1 : (0, 0, 0)}
    trans = False
    take_on_aisle = ('l', 8)
    
def king_moves():
    return ((1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1))
def queen_moves():
    return rook_moves() + bishop_moves()
def rook_moves():
    return ((1,0), (-1,0), (0,1), (0,-1))
def bishop_moves():
    return ((1,1), (-1,1), (1,-1), (-1,-1))
def knight_moves():
    return ((-2,-1), (-1,-2), (1,-2), (-2,1), (-1,2), (2,-1), (1,2), (2,1))
def pawn_moves():
    return ((1,0), (2,0), (1,1), (1,-1))

def castling(field, player):
    from show_move import castling_control
    hor = 0 if player == 1 else 7
    castl = [side for side in (-1, 1)
             if castling_control[player][0] == 0 and castling_control[player][side] == 0 and
             (side == -1 and field[hor][5] == field[hor][6] == 0 or
              side == 1 and field[hor][3] == field[hor][2] == field[hor][1] == 0)]
    return castl
             

move_rules = {6: king_moves,
              5: queen_moves,
              2: rook_moves,
              4: bishop_moves,
              3: knight_moves,
              1: pawn_moves}

value = {0 : 0,
         6 : 20,
         1 : 1,
         3 : 2.5,
         4 : 3,
         2 : 5,
         5 : 10}

def check_field_on_shah(field, player, figures, cell_king=0, kf=(8, 8)):
    if cell_king == 0:
        from show_move import cell_king
    for targ in figures:
        if det_shah(field, targ, cell_king[player], abs(figures[targ])):
            return True
    return False

def det_shah(field, target, ck, figure):
    x, y = target
    return shah_fig[figure](x, y, ck, field, figure)

def det_p_shah(x, y, ck, field, figure):
    color = sign(field[x][y])
    return (ck[0]-x, abs(ck[1]-y)) == (color, 1)

def det_kn_shah(x, y, ck, field, figure):
    for nex in move_rules[figure]():
        if ck == (x+nex[0], y+nex[1]):
            return True
    return False

def det_brq_shah(x, y, ck, field, figure):
    nex = (ck[0] - x, ck[1] - y)
    if nex[0] == 0 or nex[1] == 0 or nex[0]==nex[1] or nex[0]==-nex[1]:
        nex = (sign(nex[0]), sign(nex[1]))
        if nex in move_rules[figure]():
            cel = (x+nex[0], y+nex[1])
            while ck != cel:
                if not (-1<cel[0]<8 and -1<cel[1]<8) or field[cel[0]][cel[1]] != 0:
                    return False
                cel = (cel[0]+nex[0], cel[1]+nex[1])
            return True
    return False

shah_fig = { 1 : det_p_shah,
             2 : det_brq_shah,
             3 : det_kn_shah,
             4 : det_brq_shah,
             5 : det_brq_shah,
             6 : det_kn_shah}

def possible_p_moves(field, target, color, figure):
    from show_move import take_on_aisle
    return [(target[0]+color*x, target[1]+y) for x, y in pawn_moves()
                if (y == 0 and field[target[0]+color][target[1]] == 0 and (x==1 or
                                                                          (x==2 and target[0]*color % 7 == 1
                                                                                and field[target[0]+2*color][target[1]] == 0))) or
                   (y != 0 and -1<target[1]+y<8 and (field[target[0]+color][target[1]+y] * color < 0) or
                               take_on_aisle == (-color, target[1] + y) and (target[0] * color) % 7 == 4)]

def possible_kn_moves(field, target, player, figure):
    return [(target[0]+nex[0], target[1]+nex[1]) for nex in move_rules[figure]()
            if -1<target[0]+nex[0]<8 and -1<target[1]+nex[1]<8 and field[target[0]+nex[0]][target[1]+nex[1]]*player <= 0]

def possible_brq_moves(field, target, player, figure):
    pm = [] 
    for nex in (move_rules[figure]()):
        cel = (target[0]+nex[0], target[1]+nex[1])
        while -1<cel[0]<8 and -1<cel[1]<8 and field[cel[0]][cel[1]] == 0:
            pm.append(cel)
            cel = (cel[0]+nex[0], cel[1]+nex[1])
        if -1<cel[0]<8 and -1<cel[1]<8 and field[cel[0]][cel[1]]*player < 0:
            pm.append(cel)
    return pm

moves_fig = {1 : possible_p_moves,
             2 : possible_brq_moves,
             3 : possible_kn_moves,
             4 : possible_brq_moves,
             5 : possible_brq_moves,
             6 : possible_kn_moves}

def possible_moves_without_shah(field, target, player):
    figure = abs(field[target[0]][target[1]])
    return moves_fig[figure](field, target, player, figure)
    
def possible_ordinary_moves(field, target, player, figures):
    poss_ordinary = []
    for x, y in possible_moves_without_shah(field, target, player):
        fig = field[x][y]
        trans = trans_pawn(player, target) and abs(field[target[0]][target[1]]) == 1
        move(field, target, (x, y))
        from show_move import cell_king
        beat = (x, y) in figures
        if beat:
            del figures[(x, y)]
        if not check_field_on_shah(field, player, figures, cell_king):
            if not trans:
                if abs(field[x][y]) == 1 and target[1]-y != 0 and fig == 0:
                    poss_ordinary.append((x, y, coords_to_square((x, y))+'a'))
                else:
                    poss_ordinary.append((x, y, coords_to_square((x, y))))
            else:
               for pot_fig in ('Q','R','N','B'):
                   poss_ordinary.append((x, y, coords_to_square((x, y))+pot_fig))
        move(field, (x, y), target, fig, -1)
        if beat:
            figures[(x, y)] = field[x][y]
    return poss_ordinary

def possible_castling(field, target, figures, player):
    figure = abs(field[target[0]][target[1]])
    poss_castl = []
    if figure == 6:
        for side in castling(field, player):
            hor = 0 if player == 1 else 7
            from show_move import cell_king
            if not check_field_on_shah(field, player, figures, cell_king):
                field[hor][4] = 0
                field[hor][4-side] = 6*player
                cell_king[player] = (hor, 4-side)
                if not check_field_on_shah(field, player, figures, cell_king):
                    field[hor][4-side] = 0
                    field[hor][4-2*side] = 6*player
                    cell_king[player] = (hor, 4-2*side)
                    if not check_field_on_shah(field, player, figures, cell_king):
                        field[hor][4-2*side] = 0
                        field[hor][4] = 6*player
                        poss_castl.append((hor, 4-2*side, ('','0-0-0', '0-0')[side]))
                field[hor][4-2*side] = 0
                field[hor][4-side] = 0
                field[hor][4] = 6*player
                cell_king[player] = (hor, 4)
    return poss_castl

def possible_moves(field, target, player, unfigures):
    poss_ordinary = possible_ordinary_moves(field, target, player, unfigures)
    poss_castl = possible_castling(field, target, unfigures, player)
    return poss_ordinary + poss_castl

def exist_moves(field, player, unfigures):
    figures = [(x, y) for x, row in enumerate(field) for y, fig in enumerate(row) if fig*player > 0]
    for fig in figures:
        if possible_moves(field, fig, player, unfigures) != []:
            return True
    return False

def all_possible_moves(field, player):
    figures = [(x, y) for x, row in enumerate(field) for y, fig in enumerate(row) if fig*player > 0]
    unfigures = {(x, y):fig for x, row in enumerate(field) for y, fig in enumerate(row) if fig*player < 0}
    apm = []
    for target in figures:
        for tpm in possible_moves(field, target, player, unfigures):
            delval = value[abs(field[tpm[0]][tpm[1]])] - value[abs(field[target[0]][target[1]])] if abs(field[tpm[0]][tpm[1]]) != 0 else -30
            apm.append((delval, target, tpm[:2], tpm[2][-1]))
    return sortka(apm)

def sortka(apm):
    apm.sort()
    apm = [(d1,d2,d3) for _,d1,d2,d3 in apm]
    apm.reverse()
    return apm

def field_legal(field, player):
    figures = {(x, y): fig for x, row in enumerate(field) for y, fig in enumerate(row) if fig*player > 0}
    kings = [sign(field[x][y]) for x in range(8) for y in range(8) if abs(field[x][y])==6]
    return (kings == [1, -1] or kings == [-1, 1]) and not check_field_on_shah(field, -player, figures)


    
        
