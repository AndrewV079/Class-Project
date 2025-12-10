import pyglet
from pyglet.window import key

class Player(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.keys = key.KeyStateHandler()
        self.direction = {'left': False, 'right': False, 'up': False , 'down': False}
        self.stats = {'health' : 100, 'movespeed' : 10}
        self.state = {'alive' : True,  'attacking' : False, 'hit' : False}
        self.facing = {'left': True, 'right': False, 'up': False, 'down': False}
        self.lastKey = key.D
        self.cooldown = 0
        self.bow_cooldown = 0


    def on_key_press(self, symbol, modifiers):
        if symbol == key.A:
            self.direction['left'] = True
            self.lastKey = key.A
        if symbol == key.D:
            self.direction['right'] = True
            self.lastKey = key.D
        if symbol == key.W:
            self.direction['up'] = True
            self.lastKey = key.W
        if symbol == key.S:
            self.direction['down'] = True
            self.lastKey = key.S

    def on_key_release(self, symbol, modifiers):
        if symbol == key.A:
            self.direction['left'] = False
        if symbol == key.D:
            self.direction['right'] = False
        if symbol == key.W:
            self.direction['up'] = False
        if symbol == key.S:
            self.direction['down'] = False

    def start_attack(self):
        if not self.state['attacking'] and self.cooldown == 0:
            self.state['attacking'] = True
            self.cooldown = 100
            pyglet.clock.schedule_once(self.end_attack, 1)

    def end_attack(self, dt):
        self.state['attacking'] = False


    def reset_hit(self, dt):
        if self.state['hit']:
            self.state['hit'] = False

    def update(self, dt):
        if self.direction['left']:
            self.x -= self.stats['movespeed']
        if self.direction['right']:
            self.x += self.stats['movespeed']
        if self.direction['up']:
            self.y += self.stats['movespeed']
        if self.direction['down']:
            self.y -= self.stats['movespeed']
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.bow_cooldown > 0:
            self.bow_cooldown -= 1