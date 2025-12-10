import pyglet
import math

class Arrow(pyglet.sprite.Sprite):
    def __init__(self,target_x, target_y, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dead = False
        self.speed = 10
        self.timer = 100
        self.angle_rad = -math.atan2((target_y - self.y) , (target_x - self.x))
        self.rotation = -math.degrees(self.angle_rad)
        self.x = self.x + math.cos(self.angle_rad) * (self.image.width / 2)
        self.y = self.y + math.sin(-self.angle_rad) * (self.image.height / 2)
        self.velocity_x = math.cos(self.angle_rad) * self.speed
        self.velocity_y = math.sin(self.angle_rad) * self.speed

    def update(self):
        self.x += self.velocity_x
        self.y -= self.velocity_y


    def clear(self):
        self.dead = True
