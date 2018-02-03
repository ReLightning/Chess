from math_utilite import sign

value = {'k' : 0,
         'p' : 1,
         'n' : 2.5,
         'b' : 3,
         'r' : 5,
         'q' : 10}

def evaluation(position):
    field = position[0]
    player = position[1]
    figures = {(x, y): field[x][y] for x in range(8) for y in range(8) if field[x][y][0]!='_'}
    evaluate = 0
    for x,y in figures:
        fig = field[x][y]
        color = sign(ord(fig[0])-ord('l'))
        evaluate += color*value[fig[1]]
    return evaluate
