from move import possible_moves, all_possible_moves
from math_utilite import *
from field import *    
from show_move import *


field = trans_field()
player = 'w'
k=0
while True:
    print('Поле:')
    print_field(field)
    all_possible_moves(field, player)
    print('Ходит: ', player)
    square = input('Выберите фигуру: ')+' '
    x, y = coords = square_to_coords(square, player)
    if field[x][y][0]=='_':
        print('Там нет фигуры!')
        continue
    if field[x][y][0]!=player:
        print('Не ваша фигура!')
        continue
    poss_moves = [possible[2] for possible in possible_moves(field, coords, player)]
    if poss_moves == []:
        print('Эта фигура ходов не имеет!')
        continue
    while True:
        print('Возможные ходы:')
        print(' '.join(poss_moves))
        m = input('Введите свой ход: ')
        if m not in poss_moves:
            print('Нет такого хода')
        else:
            break
    m += ' '
    move(field, coords, square_to_coords(m, player), trans_fig=m[2], main=1)
    player = 'w' if player=='b' else 'b'
   
