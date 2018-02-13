import cocos
from math_utilite import un
from field import print_field
import interface
from move import check_field_on_shah, possible_moves_without_shah


def makepgn(self):
    file = open('Утилиты/standart.txt')
    standtag = file.read()
    file.close()
    file = open('База партий/file.pgn', 'w', encoding='utf-8')
    notation = ' '.join(self.notation)
    notation = standtag + notation
    file.write(notation)
    file.close()

def start_notation(self):
    self.notation_view = cocos.sprite.Sprite('Image/Utilites/Notation.png')
    self.notation_view.position = 1150, 418
    self.add(self.notation_view)

def upnotation(self, det, fig, beat, distins):
    det = det_update(det, fig, self.target, self.activ, beat)
    interface.det_mate(self=self)
    det = det_shah_mate(det, self.field, self.player, self.labels)
    if distins != []:
        det = det_distinctness(det, distins, self.activ)
    view_notation(self, det)

def det_update(det, fig, target, activ, beat):
    if fig != 'p':
        if det[0] != '0':
            det = chr(ord(fig)-32)+det
    else:
        if target[1] - activ[1] !=0:
            det = 'abcdefgh'[activ[1]] + det[:3]
            det = det[0] + '×' + det[1:]
        if det[-1] in ('q','r','b','n'):
            det = det[:-1] + chr(ord(det[-1])-32)
        if det[-1] == 'a':
            det = det[:-1]
    if beat != '_' and fig != 'p':
        det = det[0] + '×' + det[1:]
    return det

def det_shah_mate(det, field, player, labels):
    figures = {(x, y) : field[x][y] for x in range(8) for y in range(8) if field[x][y][0]==un(player)}
    if check_field_on_shah(field, player, figures):
        if 'mate' in labels:
            det += '#'
        else:
            det+= '+'
    return det

def det_distinctness(det, distins, activ):
    xs = False
    ys = False
    for x, y in distins:
        xs = xs or activ[0] == x
        ys = ys or activ[1] == y
    if ys:
        det = det[0] + str(activ[0]+1) + det[1:]
    if xs or (not xs and not ys):
        det = det[0] + 'abcdefgh'[activ[1]] + det[1:]
    return det

def view_notation(self, det):
    if self.player == 'b':
        self.notation.append(str(self.numstep)+'.'+ det)
    else:
        self.notation.append(det)
    if self.textview_notation != '':
        self.textview_notation.kill()
    notation = ' '.join(self.notation)
    self.textview_notation = cocos.text.Label(notation, color=(0,0,0,255), multiline=True, width=400)
    self.textview_notation.position = 960, 634
    self.add(self.textview_notation)

    
def distinctness(self):
    distins = []
    fig = self.field[self.activ[0]][self.activ[1]]
    if not fig[1] in ('k', 'p'):
        distin = [(x, y) for x in range(8) for y in range(8) if self.field[x][y] == fig]
        for figure in distin:
            if self.target in possible_moves_without_shah(self.field, figure, self.player) and figure != self.activ:
                distins.append(figure)
        return distins
    else:
        return []
        
    
