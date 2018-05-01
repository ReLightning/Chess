from field import trans_field, print_field
from move import possible_moves, all_possible_moves
from math_utilite import *
from show_move import start_parameter_2
import cocos
from cocos.actions import *
import interface
import notation
from engine import testing




class graph(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self):
        super(graph, self).__init__()
        interface.start_parameter(self)
        interface.start_graph(self)
        
    #словарь функций  
    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons == 1:
            if self.red == ():
                if 80<=x<=720 and 80<=y<=720:
                    interface.click_board(self, x, y)
                if 65<=x<=180 and 22<=y<=50:
                    interface.button_click(self, -1, 'Заново', (120, 40))
                if 185<=x<=300 and 22<=y<=50:
                    interface.button_click(self, -1, 'Редактор', (240, 40))
                if 305<=x<=420 and 22<=y<=50:
                    interface.button_click(self, -1, 'Сохранить', (360, 40))
                if 425<=x<=540 and 22<=y<=50:
                    interface.button_click(self, -1, 'Старт', (480, 40))
                if 960<=x<=1115 and y<=634:
                    notation.det_step(self, x, y)
            else:
                if 80<=x<=720 and 80<=y<=720:
                    self.target = det_target(x, y, self.flip)
                    target = self.target
                    if target in self.sprites:
                        self.sprites.pop(target).kill()
                    if self.chosen != 'none':
                        interface.redfigadd(self)
                    self.field[target[0]][target[1]] = self.redfig
        if buttons == 4 and 80<=x<=720 and 80<=y<=720:
            interface.flipboard(self, self.flip)
            self.flip *= -1
            
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.activ != (8, 8):
            self.sprites[self.activ].do(Place((x, y)))
        
    #словарь функций
    def on_mouse_release(self, x, y, buttons, modifiers):
        if buttons == 1:
            if self.name != '':
                if 65<x<180 and 22<y<50 and self.name == 'Заново':
                    self.butagain()
                if 185<x<300 and 22<y<50 and self.name == 'Редактор':
                    self.butredactor()
                if 305<=x<=420 and 22<=y<=50 and self.name == 'Сохранить':
                    notation.makepgn(self)
                if 425<=x<=540 and 22<=y<=50 and self.name == 'Старт':
                    notation.load_start_position(self)
                interface.button_click(self, 1, self.name, self.pos)
            elif self.red != ():
                if 800<x<960 and 80<y<660:
                    self.redactor(x, y)
            elif self.activ != (8, 8): 
                self.chose_cage(x, y)
    #
    def on_key_press(self, key, modifiers):
        if key == 65361:
            num = str(self.numstep-1)+'_wb'[self.player]
            if num!='0w':
                interface.fieldsubs(self, num)
                notation.det_step(self, 0, 0, True, num)
        if key == 65363:
            num = str(self.numstep)+'_wb'[self.player]
            if num in self.positions:
                interface.fieldsubs(self, num)
                notation.det_step(self, 0, 0, True, num)
                
    def chose_fig(self, x, y):
        global poss_moves, det_moves
        field = self.field
        self.activ = self.target
        interface.shelladd(self)
        self.remove(self.sprites[self.activ])
        self.add(self.sprites[self.activ], z=1)
        self.sprites[self.activ].do(Place((x, y)))
        unfigures = det_myfigures(field, -self.player)
        possibles = possible_moves(field, self.target, self.player, unfigures)
        poss_moves = [possible[:2] for possible in possibles]
        det_moves = [possible[-1] for possible in possibles]
            
    def chose_cage(self, x, y):
        global poss_moves, det_moves
        self.target = det_target(x, y, self.flip)
        target = self.target
        if target not in poss_moves or not (80<=x<=720 and 80<=y<=720):
            self.sprites[self.activ].do(Place(graph_coord(self.activ, self.flip)))
            self.add(self.sprites[self.activ], z=0)
            self.sprites.pop('shell').kill()
            self.activ = (8, 8)
        else:
            det = det_moves[poss_moves.index(target)]
            interface.graph_move(self, det)
            
    def butagain(self):
        if 'mate' in self.labels:
            self.labels.pop('mate').kill()
        self.field = trans_field()
        for figure in self.sprites:
            self.sprites[figure].kill()
        self.sprites = {}
        interface.figureadd(self)
        self.player = 1
        self.activ = (8, 8)
        self.numstep = 1
        if self.textview_notation != []:
            for step in self.textview_notation.items():
                step[1].kill()
            self.textview_notation = []
        self.notation = []
        start_parameter_2(par=({1 : (0, 4),
                                -1 : (7, 4)},
                               {1 : (0, 0, 0),
                                -1 : (0, 0, 0)},
                               False,
                               ('l', 8)))
        from show_move import cell_king, castling_control, take_on_aisle
        self.positions = {'0b' : (trans_field(), (cell_king, castling_control, False, take_on_aisle))}

    def butredactor(self):
        t_player = 'Белые' if self.player == 1 else 'Чёрные'
        self.red = cocos.sprite.Sprite('Image/Utilites/Edit-Figure.png')
        self.red.position = 880, 368
        label = cocos.text.Label(text='Ходят:'+t_player, position=(820,643), color=(0,0,0,255))
        self.add(label, z=1)
        self.labels['player'] = label
        self.add(self.red)

    def redactor(self, x, y):
        if 870<x<930 and 635<y<658:
            self.player *= -1
            t_player = 'Белые' if self.player == 1 else 'Чёрные'
            self.labels['player'].kill()
            label = cocos.text.Label('Ходят:'+t_player, position=(820,643), color=(0,0,0,255))
            self.add(label)
            self.labels['player'] = label
        if 943<x<960 and 639<y<658:
            interface.closered(self)
        if 800<x<960 and 80<y<640:
            interface.det_chosen(self, x, y)
            
                                                
def demgraph():
    cocos.director.director.init(fullscreen=True)
    main_scene = cocos.scene.Scene(graph())
    cocos.director.director.run(main_scene)
        
    
demgraph()



