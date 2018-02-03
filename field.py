cell_king = {'w' : (0, 4),
             'b' : (7, 4)}
castling_control = {'w' : (0, 0, 0),
                    'b' : (0, 0, 0)}
trans = False
take_on_aisle = ('l', 8)

def make_field():
    return list(reversed([['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br',],
                          ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp',],
                          ['__', '__', '__', '__', '__', '__', '__', '__',],
                          ['__', '__', '__', '__', '__', '__', '__', '__',],
                          ['__', '__', '__', '__', '__', '__', '__', '__',],
                          ['__', '__', '__', '__', '__', '__', '__', '__',],
                          ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp',],
                          ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr',]]))

def trans_field():
    return [[(color, figure) for color, figure in row] for row in make_field()]

def print_field(field): 
    print('\n'.join(reversed([' '.join('{}{}'.format(color, figure) for color, figure in row) for row in field])))


            
            
