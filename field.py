from math_utilite import sign
trans_value = {'_' : 0,
               'k' : 6,
               'q' : 5,
               'r' : 2,
               'b' : 4,
               'n' : 3,
               'p' : 1}

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
    from math_utilite import col
    return [[col(color)*trans_value[figure] for color, figure in row] for row in make_field()]


def print_field(field): 
    print('\n'.join(reversed([' '.join('{}'.format('_wb'[sign(fig)]+'_prnbqk'[abs(fig)]) for fig in row) for row in field])))




            
            
