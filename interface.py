import cocos
from cocos.actions import *
from move import check_field_on_shah, exist_moves, field_legal
from show_move import det_cell_king, det_castling_control, move, start_parameter_2
from math_utilite import *
from field import trans_field, print_field
import notation
import copy
from engine import testing
import cProfile

colors = {'w' : 'White-',
          'b' : 'Black-'}
figures = {'k': 'King',
           'q': 'Queen',
           'r': 'Rook',
           'b': 'Bishop',
           'n': 'Knight',
           'p': 'Pawn'}
redcolors = {1 : 'w',
             0 : 'b'}
redfigures = {0 : 'none',
              1 : 'k',
              2 : 'q',
              3 : 'r',
              4 : 'b',
              5 : 'n',
              6 : 'p',}

actbut = {1 : 'Image/Buttons/noactiv ',
          -1 : 'Image/Buttons/activ '}

def start_parameter(self):
    self.field = trans_field()
    self.player = 'w'
    self.numstep = 1
    self.sprites = {}
    self.buttons = {}
    self.labels = {}
    self.name = ''
    self.pos = ()
    self.red = ()
    self.chosen = 'none'
    self.redfig = ('_','_')
    self.flip = 1
    self.activ = (8, 8)
    self.notation = []
    self.textview_notation = ''
    start_parameter_2()
    from show_move import cell_king, castling_control, take_on_aisle
    self.positions = {'0b' : (trans_field(), (cell_king, castling_control, False, take_on_aisle))}
    

def start_graph(self):
    boardadd(self)
    figureadd(self)
    button_click(self, 1, 'Заново', (120, 40))
    button_click(self, 1, 'Редактор', (240, 40))
    button_click(self, 1, 'Сохранить', (360, 40))
    notation.start_notation(self)
    
def flipboard(self, flip):
    for figure in self.sprites:
        sprite = self.sprites[figure]
        sprite.do(Place((120+80*((-flip*figure[1]-(flip+1)//2)%8), 120+80*((-flip*figure[0]-(flip+1)//2)%8))))

def boardadd(self):
    sprite = cocos.sprite.Sprite('Image/Utilites/Board.jpeg') 
    sprite.position = 400, 400
    self.add(sprite, z=0)

def figureadd(self):
    field = self.field
    figuras = {(x, y): field[x][y] for x in range(8) for y in range(8) if field[x][y][0]!='_'}
    for x, y in figuras:
        figure = field[x][y]
        sprite = cocos.sprite.Sprite('Image/Figures/'+colors[figure[0]]+figures[figure[1]]+'.png')
        sprite.position = graph_coord((x, y), self.flip)
        sprite.scale = 0.5
        self.add(sprite, z=0)
        self.sprites[(x, y)] = sprite

def fieldsubs(self, num):
    for figure in self.sprites:
        self.sprites[figure].kill()
    self.sprites = {}
    posit = self.positions[num]
    self.field = posit[0]
    self.player = un(num[-1])
    start_parameter_2(par=posit[1])
    self.numstep = int(num[:-1]) if num[-1] == 'w' else int(num[:-1])+1
    figureadd(self)
    
    
def figadd(self):
    sprite = cocos.sprite.Sprite(self.chosen)
    sprite.position = graph_coord(self.target, self.flip)
    sprite.scale = 0.5
    self.add(sprite)
    self.sprites[self.target] = sprite

def shelladd(self):
    sprite = cocos.sprite.Sprite('Image/Utilites/Shell.png')
    sprite.position = graph_coord(self.activ, self.flip)
    self.sprites['shell'] = sprite
    self.add(sprite, z=0)

def graph_move(self, det):
    target = self.target
    beat = self.field[target[0]][target[1]][0]
    fig = self.field[self.activ[0]][self.activ[1]][1]
    distin = notation.distinctness(self)
    positions = copy.deepcopy(self.positions)
    move(self.field, self.activ, target, trans_fig='q', main=1)
    self.positions = positions
    addpositions(self)
    if 'shell' in self.sprites:
        self.sprites.pop('shell').kill()
    sprite = self.sprites[self.activ]
    sprite.do(Place(graph_coord(target, self.flip)))
    if target in self.sprites.keys():
        self.sprites[target].kill()
    self.sprites[(target[0], target[1])] = sprite
    self.sprites.pop(self.activ)
    step_deviation(self, det[2:], sprite)
    self.player = un(self.player)
    notation.upnotation(self, det, fig, beat, distin)
    if self.player == 'w':
        self.numstep += 1
    else:
        if False:
            num = self.positions[str(self.numstep)+'w']
            bmove = testing((num[0],'b',num[1]))
            self.activ = bmove[0]
            self.target = bmove[1]
            graph_move(self, bmove[2])
    self.activ = (8, 8)
    
def button_click(self, act, name, pos):
    sprite = cocos.sprite.Sprite(actbut[act]+name+ '.png')
    sprite.position = pos
    self.add(sprite)
    self.buttons[name] = sprite
    if act == 1:
        self.name = ''
        self.pos = ()
    if act == -1:
        self.name = name
        self.pos = pos

def det_mate(self):
    field = self.field
    player = self.player
    unfigures = {(x, y): field[x][y] for x in range(8) for y in range(8) if field[x][y][0]==un(player)}
    if not exist_moves(field, player, unfigures):
        if check_field_on_shah(field, player, unfigures):
            label = cocos.text.Label('Мат', font_size=48, position=(400, 400), color=(255,0,0,255))
            self.add(label)
            self.labels['mate'] = label
        else:
            label = cocos.text.Label('Пат', font_size=48, position=(400, 400), color=(255,0,0,255))
            self.add(label)
            self.labels['mate'] = label

def step_deviation(self, det, sprite):
    target = self.target
    if det == '0' or det =='0-0':
        sprite = self.sprites[(target[0], target[1]-(3*len(det)-5)//2)]
        sprite.do(Place(graph_coord((self.activ[0], self.activ[1]-len(det)+2), self.flip)))
        self.sprites[(self.activ[0], self.activ[1]-len(det)+2)] = sprite
        self.sprites.pop((target[0], target[1]-(3*len(det)-5)//2))
    if det in ('q','r','b','n'):
        sprite.kill()
        sprite = cocos.sprite.Sprite('Image/Figures/'+colors[self.player]+figures[det]+'.png')
        sprite.position = graph_coord(target, self.flip)
        sprite.scale = 0.5
        self.sprites[target] = sprite
        self.add(sprite)
    if det == 'a':
        self.sprites.pop((target[0]-sign(ord(self.player) - ord('l')), target[1])).kill()

def closered(self):
    ck = det_cell_king(self.field)
    cc = det_castling_control(self.field)
    if field_legal(self.field, self.player):
        self.red.kill()
        self.red = ()
        self.labels['player'].kill()
        if 'mate' in self.labels:
            self.labels.pop('mate').kill()
        if self.textview_notation != '':
            self.textview_notation.kill()
            self.textview_notation = ''
        self.notation = []
        self.positions = {'0b' : (self.field, (ck, cc, False, ('l',8)))}
        self.numstep = 1
        self.chosen = 'none'

def addpositions(self):
    from show_move import cell_king, castling_control, take_on_aisle
    self.positions[str(self.numstep)+self.player] = (self.field, (cell_king, castling_control, False, take_on_aisle))


        
def detchosen(self, x, y):            
    chosen = ((960-x)//80, (640-y)//80)
    self.redfig = (redcolors[chosen[0]], redfigures[chosen[1]]) if chosen[1] != 0 else ('_','_')
    self.chosen = 'Image/Figures/'+colors[redcolors[chosen[0]]]+figures[redfigures[chosen[1]]]+'.png' if chosen[1] != 0 else 'none'

def click_board(self, x, y):
    self.target = det_target(x, y, self.flip)
    target = self.target
    if self.field[target[0]][target[1]][0]==self.player:
        self.chose_fig(x, y)
        
        
    
