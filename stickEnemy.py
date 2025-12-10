import pyglet
import random

class Enemy(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = {'alive' : True, 'hit': False, 'see_target' : False}
        self.stats = {'health' : 100, 'movespeed' : 5}
        self.dead = False

    def move(self, target):
        if self.x > target.x:
            self.x -= self.stats['movespeed']
        if self.x < target.x:
            self.x += self.stats['movespeed']
        if self.y > target.y:
            self.y -= self.stats['movespeed']
        if self.y < target.y:
            self.y += self.stats['movespeed']