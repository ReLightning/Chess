from math_utilite import sign
trans_value = {'_' : 0,
               'k' : 6,
               'q' : 5,
               'r' : 2,
               'b' : 4,
               'n' : 3,
               'p' : 1}

def make_field():
    file = open('Утилиты/start_position.txt')
    r = file.read()
    sp = [[fig for fig in row.split(' ')] for row in r.split('\n')]
    return list(reversed(sp))

def trans_field():
    from math_utilite import col
    return [[col(color)*trans_value[figure] for color, figure in row] for row in make_field()]


def print_field(field):
    pos = '\n'.join(reversed([' '.join('{}'.format('_wb'[sign(fig)]+'_prnbqk'[abs(fig)]) for fig in row) for row in field]))
    print(pos)
    return pos




            
            
