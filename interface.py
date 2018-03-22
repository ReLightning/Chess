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

colors = {1 : 'White-',
          -1 : 'Black-'}
figures = {6: 'King',
           5: 'Queen',
           2: 'Rook',
           4: 'Bishop',
           3: 'Knight',
           1: 'Pawn'}

redfig= {0 : 0,
         1 : 6,
         2 : 5,
         3 : 2,
         4 : 4,
         5 : 3,
         6 : 1,}

actbut = {1 : 'Image/Buttons/noactiv ',
          -1 : 'Image/Buttons/activ '}

def start_parameter(self):
    self.field, self.player = trans_field(), 1
    self.numstep = 1
    self.sprites, self.buttons, self.labels = {}, {}, {}
    self.name, self.pos = '', ()
    self.red, self.chosen, self.redfig = (), 'none', 0
    self.flip, self.activ = 1, (8, 8)
    self.notation, self.textview_notation = [], ''
    start_parameter_2()
    from show_move import cell_king, castling_control, take_on_aisle
    self.positions = {'0b' : (trans_field(), (cell_king, castling_control, False, take_on_aisle))}
    

def start_graph(self):
    boardadd(self)
    figureadd(self)
    button_click(self, 1, 'Заново', (120, 40))
    button_click(self, 1, 'Редактор', (240, 40))
    button_click(self, 1, 'Сохранить', (360, 40))
    button_click(self, 1, 'Старт', (480, 40))
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
    figs = det_figures(self.field)
    for cell in figs:
        fig = figs[cell]
        sprite = cocos.sprite.Sprite('Image/Figures/'+colors[sign(fig)]+figures[abs(fig)]+'.png')
        sprite.position = graph_coord(cell, self.flip)
        sprite.scale = 0.5
        self.add(sprite, z=0)
        self.sprites[cell] = sprite
        
#?
def fieldsubs(self, num):
    for figure in self.sprites:
        self.sprites[figure].kill()
    self.sprites = {}
    posit = self.positions[num]
    self.field = posit[0]
    self.player = -1 if num[-1] == 'w' else 1
    start_parameter_2(par=posit[1])
    self.numstep = int(num[:-1]) if num[-1] == 'w' else int(num[:-1])+1
    figureadd(self)
    
    
def redfigadd(self):
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

#?
def graph_move(self, det):
    target = self.target
    beat = sign(self.field[target[0]][target[1]])
    fig = abs(self.field[self.activ[0]][self.activ[1]])
    distin = notation.distinctness(self)
    positions = copy.deepcopy(self.positions)
    move(self.field, self.activ, target, trans_fig=5, main=1)
    self.positions = positions
    addpositions(self)
    dem_change(self, det)
    self.player *= -1
    notation.upnotation(self, det, fig, beat, distin)
    if self.player == 1:
        self.numstep += 1
    self.activ = (8, 8)

def dem_change(self, det):
    if 'shell' in self.sprites:
        self.sprites.pop('shell').kill()
    sprite = self.sprites[self.activ]
    sprite.do(Place(graph_coord(self.target, self.flip)))
    if self.target in self.sprites.keys():
        self.sprites[self.target].kill()
    self.sprites[(self.target[0], self.target[1])] = sprite
    self.sprites.pop(self.activ)
    step_deviation(self, det[2:], sprite)


def button_click(self, act, name, pos):
    sprite = cocos.sprite.Sprite(actbut[act]+name+'.png')
    sprite.position = pos
    self.add(sprite)
    self.buttons[name] = sprite
    self.name, self.pos = ('', ()) if act+1 else (name, pos)

#?
def det_mate(self):
    field = self.field
    player = self.player
    unfigures = det_myfigures(field, -player)
    if not exist_moves(field, player, unfigures):
        if check_field_on_shah(field, player, unfigures):
            label = cocos.text.Label('Мат', font_size=48, position=(400, 400), color=(255,0,0,255))
            self.add(label)
            self.labels['mate'] = label
        else:
            label = cocos.text.Label('Пат', font_size=48, position=(400, 400), color=(255,0,0,255))
            self.add(label)
            self.labels['mate'] = label

transfig = {'Q' : 5,
            'R' : 2,
            'B' : 4,
            'N' : 3}

def dev_cast(self, det):
    target = self.target
    activ = self.activ
    sprite = self.sprites[(target[0], target[1]-(3*len(det)-5)//2)]
    sprite.do(Place(graph_coord((activ[0], activ[1]-len(det)+2), self.flip)))
    self.sprites[(activ[0], activ[1]-len(det)+2)] = sprite
    self.sprites.pop((target[0], target[1]-(3*len(det)-5)//2))

def dev_trans(self, det, sprite):
    sprite.kill()
    sprite = cocos.sprite.Sprite('Image/Figures/'+colors[self.player]+figures[transfig[det]]+'.png')
    sprite.position = graph_coord(self.target, self.flip)
    sprite.scale = 0.5
    self.sprites[target] = sprite
    self.add(sprite)

def dev_aisle(self):
    self.sprites.pop((self.target[0]-self.player, self.target[1])).kill()
    
#словарь    
def step_deviation(self, det, sprite):
    if det == '0' or det =='0-0':
        dev_cast(self, det)
    if det in ('Q','R','B','N'):
        dev_trans(self, det, sprite)
    if det == 'a':
        dev_aisle(self)
        

def closered(self):
    if field_legal(self.field, self.player):
        delete_view_red(self)
        default_par(self)

def delete_view_red(self):
    self.red.kill()
    self.red = ()
    self.labels['player'].kill()
    if 'mate' in self.labels:
        self.labels.pop('mate').kill()
    if self.textview_notation != '':
        self.textview_notation.kill()
        self.textview_notation = ''
        
def default_par(self):
    self.notation = []
    self.numstep = 1
    self.chosen = 'none'
    ck = det_cell_king(self.field)
    cc = det_castling_control(self.field)
    self.positions = {'0b' : (self.field, (ck, cc, False, ('l',8)))}

        
def addpositions(self):
    from show_move import cell_king, castling_control, take_on_aisle
    self.positions[str(self.numstep)+'_wb'[self.player]] = (self.field, (cell_king, castling_control, False, take_on_aisle))


        
def det_chosen(self, x, y):            
    chosen = (sign(880-x), (640-y)//80)
    self.redfig = chosen[0]*redfig[chosen[1]]
    self.chosen = 'Image/Figures/'+colors[chosen[0]]+figures[redfig[chosen[1]]]+'.png' if chosen[1] != 0 else 'none'

def click_board(self, x, y):
    self.target = det_target(x, y, self.flip)
    target = self.target
    if self.field[target[0]][target[1]]*self.player > 0:
        self.chose_fig(x, y)
        
        
    
