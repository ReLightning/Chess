from math_utilite import sign, coords_to_square
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
    return [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
def queen_moves():
    return rook_moves() + bishop_moves()
def rook_moves():
    return [(0,a) for a in range(-7,8) if a!=0 ] + \
           [(a,0) for a in range(-7,8) if a!=0 ]
def bishop_moves():
    return [(a,a) for a in range(-7,8) if a!=0 ] + \
           [(-a,a) for a in range(-7,8) if a!=0 ]
def knight_moves():
    return [(-2,-1), (-1,-2), (1,-2), (-2,1), (-1,2), (2,-1), (1,2), (2,1)]
def pawn_moves():
    return [(a,0) for a in range(-2,3) if a!=0] + \
           [(a,rl) for a in (-1,1) for rl in (-1,1) if a!=0 and rl!=0]
def castling(field):
    from show_move import castling_control
    colors = ('w', 'b')
    castls = ('0-0', '0-0-0')
    return [(color, castl) for color in colors for castl in castls
            if field[int(3.5-3.5*(-1)**colors.index(color))][4] == (color, 'k')
            and field[int(3.5-3.5*(-1)**colors.index(color))][int(3.5+3.5*(-1)**castls.index(castl))] == (color, 'r')
            and castling_control[color][0] == 0 and castling_control[color][castls.index(castl)+1] == 0
            and not collision(field, (int(3.5-3.5*(-1)**colors.index(color)), 4), (int(3.5-3.5*(-1)**colors.index(color)), int(3.5+3.5*(-1)**castls.index(castl))))]

move_rules = {'k': king_moves,
              'q': queen_moves,
              'r': rook_moves,
              'b': bishop_moves,
              'n': knight_moves,
              'p': pawn_moves}

def check_field_on_shah(field, player, figures):
    from show_move import cell_king
    unplayer = 'w' if player=='b' else 'b'
    for x, y in figures:
        if field[x][y][0] == unplayer and cell_king[player] in possible_moves_without_shah(field, (x, y), unplayer):
            return True
    return False

def collision(field, start_coord, end_coord):
    dx=end_coord[0]-start_coord[0]
    dy=end_coord[1]-start_coord[1]
    if abs(dx)==abs(dy) or dx==0 or dy==0:
        for i in range(1,max(abs(dx),abs(dy))):
            if field[start_coord[0]+i*sign(dx)][start_coord[1]+i*sign(dy)]!=('_','_'):
                return True
    return False

def possible_pawn_moves_without_shah(field, target, player):
    from show_move import take_on_aisle
    unplayer = 'w' if player=='b' else 'b'
    color = sign(ord(player)-ord('l'))
    return [(color*x, y) for x, y in pawn_moves()
            if 0<=target[0]+x*color<=7 and 0<=target[1]+y<=7
            and  x in range((16-(target[0]*color)%7)//5)
            and ((y==0 and field[target[0]+x*color][target[1]+y][0]=='_')
                or (y!=0 and (field[target[0]+x*color][target[1]+y][0]==unplayer
                              or (take_on_aisle == (unplayer, target[1] + y) and (target[0] * color) % 7 == 4))))]
    
def possible_moves_without_shah(field, target, player):
    unplayer = 'w' if player=='b' else 'b'
    figure = field[target[0]][target[1]][1]
    figures = {(x, y): field[x][y] for x in range(8) for y in range(8) if field[x][y][0]==unplayer}
    if figure=='p':
        all_moves = possible_pawn_moves_without_shah(field, target, player)
    else:
        all_moves = move_rules[figure]()
    return [(target[0]+hor, target[1]+vert) for hor,vert in all_moves
            if 0<=target[0]+hor<=7 and 0<=target[1]+vert<=7
            and field[target[0]+hor][target[1]+vert][0]!=player
            and not collision(field, target, (target[0]+hor, target[1]+vert))]
    
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

def possible_moves(field, target, player):
    unplayer = 'w' if player=='b' else 'b'
    figures = {(x, y): field[x][y] for x in range(8) for y in range(8) if field[x][y][0]==unplayer}
    poss_ordinary = possible_ordinary_moves(field, target, player, figures)
    poss_castl = possible_castling(field, target, figures, player)
    return poss_ordinary + poss_castl

def exist_moves(field, player):
    figures = {(x, y): field[x][y] for x in range(8) for y in range(8) if field[x][y][0]==player}
    for figure in figures:
        for pm in possible_moves(field, figure, player):
            return True
    return False

def all_possible_moves(field, player):
    figures = {(x, y): field[x][y] for x in range(8) for y in range(8) if field[x][y][0]==player}
    apm = []
    for target in figures:
        for tpm in possible_moves(field, target, player):
            apm.append(field[target[0]][target[1]][1]+tpm[2])
    return apm

def field_legal(field, player):
    unplayer = 'w' if player == 'b' else 'b'
    figures = {(x, y): field[x][y] for x in range(8) for y in range(8) if field[x][y][0]==player}
    kings = [field[x][y][0] for x in range(8) for y in range(8) if field[x][y][1]=='k']
    return (kings == ['w', 'b'] or kings == ['b', 'w']) and not check_field_on_shah(field, unplayer, figures)


    
        
