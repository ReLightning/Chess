def sign(a):
    if a==0:
        return 0
    if a>0:
        return 1
    else:
        return -1
    
def coords_to_square(target):
    return 'abcdefgh'[target[1]]+str(target[0]+1)

def square_to_coords(square, player):
    if square[2] == '0':
        y = 6 if square == '0-0 ' else 2
        x = 0 if player == 'w' else 7
        nruter = (x, y)
    else:
        nruter = (int(square[1])-1, ord(square[0])-ord('a'))
    return nruter

def graph_coord(target, flip):
    return (((flip*(target[1]-(flip-1)//2))%8)*80+120, ((flip*(target[0]-(flip-1)//2))%8)*80+120)

def det_target(x, y, flip):
    return (flip*(y//80-1)+(flip-1)//2)%8, (flip*(x//80-1)+(flip-1)//2)%8

player_colors = ('w', 'b')
def un(player):
    return 'w' if player == 'b' else 'b'

def col(player):
    return 1 if player == 'w' else -1

