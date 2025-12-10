import pyglet

class Sword(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dead = False
        self.active = False
        self.timer = 0

    def update(self):
        if self.active and self.timer > 0:
            self.timer -= 1
        if self.timer == 0:
            self.deactivate()

    def deactivate(self):
        self.active = False