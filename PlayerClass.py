import pyglet
from pyglet.window import key

class Player(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.keys = key.KeyStateHandler()
        self.direction = {'left': False, 'right': False, 'up': False , 'down': False}
        self.stats = {'health' : 100}
        self.state = {'alive' : True,  'attacking' : False, 'hit' : False}
        self.cooldown = 0


    def on_key_press(self, symbol, modifiers):
        if symbol == key.A:
            self.direction['left'] = True
        if symbol == key.D:
            self.direction['right'] = True
        if symbol == key.W:
            self.direction['up'] = True
        if symbol == key.S:
            self.direction['down'] = True


    def on_key_release(self, symbol, modifiers):
        if symbol == key.A:
            self.direction['left'] = False
        if symbol == key.D:
            self.direction['right'] = False
        if symbol == key.W:
            self.direction['up'] = False
        if symbol == key.S:
            self.direction['down'] = False

    def start_attack(self, attack_image):
        if not self.state['attacking'] and self.cooldown == 0:
            self.state['attacking'] = True
            attack_image.scale = .25
            self.cooldown = 300
            self.image = attack_image
            self.scale = .25
            pyglet.clock.schedule_once(self.end_attack, 1)

    def end_attack(self, dt):
        self.state['attacking'] = False
        self.image = pyglet.resource.image('images (1).jpg')
        self.scale = 1

    def update(self, dt):
        if self.direction['left']:
            self.x -= 10
        if self.direction['right']:
            self.x += 10
        if self.direction['up']:
            self.y += 10
        if self.direction['down']:
            self.y -= 10
        if self.cooldown > 0:
            self.cooldown -= 1
