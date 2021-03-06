import cocos
from field import print_field
import interface
from move import check_field_on_shah, possible_moves_without_shah
from math_utilite import det_myfigures

notval = {2 : 'R',
          3 : 'N',
          4 : 'B',
          5 : 'Q',
          6 : 'K',}

def makepgn(self):
    file = open('Утилиты/standart.txt')
    standtag = file.read()
    file.close()
    file = open('База партий/file.pgn', 'w', encoding='utf-8')
    notation = ' '.join(self.notation)
    notation = standtag + notation
    file.write(notation)
    file.close()

def stepshell(self, num):
    if num != '0b':
        numstep, color = int(num[:-1]), num[-1]
        sprite = cocos.sprite.Sprite('Image/Utilites/Stepshell.png')
        pos = (980, 639 - 25*numstep) if color == 'w' else (1065, 639 - 25*numstep)
        sprite.position = pos
        self.add(sprite)
        self.sprites['stepshell'] = sprite
    
def det_step(self, x, y, yuo=False, nex=()):
    if nex == ():
        color = 'w' if x < 1035 else 'b'
        numstep = (650 - y) // 25
        num = (str(numstep)+color)
    else:
        num = nex
    if yuo:
        if 'stepshell' in self.sprites:
            self.sprites['stepshell'].kill()
        stepshell(self, num)
    elif num in self.textview_notation:
        interface.fieldsubs(self, num)
        stepshell(self, num)

def start_notation(self):
    self.notation_view = cocos.sprite.Sprite('Image/Utilites/Notation.png')
    self.notation_view.position = 1150, 418
    self.add(self.notation_view, z=0)

def upnotation(self, det, fig, beat, distins):
    det = det_update(det, fig, self.target, self.activ, beat)
    interface.det_mate(self=self)
    det = det_shah_mate(det, self.field, self.player, self.labels)
    if distins != []:
        det = det_distinctness(det, distins, self.activ)
    view_notation(self, det)

def det_update(det, fig, target, activ, beat):
    if fig != 1:
        if det[0] != '0':
            det = notval[fig]+det
    else:
        if target[1] - activ[1] !=0:
            det = 'abcdefgh'[activ[1]] + det[:3]
            det = det[0] + '×' + det[1:]
        if det[-1] == 'a':
            det = det[:-1]
    if beat != 0 and fig != 1:
        det = det[0] + '×' + det[1:]
    return det

def det_shah_mate(det, field, player, labels):
    unfigures = det_myfigures(field, -player)
    if check_field_on_shah(field, player, unfigures):
        if 'mate' in labels:
            det += '#'
        else:
            det+= '+'
    return det

def det_distinctness(det, distins, activ):
    xs = ys = False
    for x, y in distins:
        xs = xs or activ[0] == x
        ys = ys or activ[1] == y
    if ys:
        det = det[0] + str(activ[0]+1) + det[1:]
    if xs or (not xs and not ys):
        det = det[0] + 'abcdefgh'[activ[1]] + det[1:]
    return det

def view_notation(self, det):
    if self.player == -1:
        det = (str(self.numstep)+'.'+ det)
    self.notation.append(det)
    step = cocos.text.Label(det, color=(0,0,0,255))
    step.position = 960+(1+self.player)*50, 634-25*self.numstep,
    self.add(step, z=0)
    self.textview_notation[str(self.numstep)+'_bw'[self.player]] = step

    
def distinctness(self):
    distins = []
    fig = self.field[self.activ[0]][self.activ[1]]
    if not abs(fig) in (6, 1):
        distin = [(x, y) for x in range(8) for y in range(8) if self.field[x][y] == fig]
        for figure in distin:
            if self.target in possible_moves_without_shah(self.field, figure, self.player) and figure != self.activ:
                distins.append(figure)
        return distins
    else:

        return []
    
def load_start_position(self):
    file = open('Утилиты/start_position.txt', 'w')
    sp = print_field(self.field, 1)
    file.write(sp)
    
        
    
