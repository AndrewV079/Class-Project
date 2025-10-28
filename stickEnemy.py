import pyglet
import random

enemies = []

def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

enemy_image = pyglet.resource.image('Basic_human_drawing.png')
center_image(enemy_image)



def spawn_Enemy(amount):
    for i in range(amount):
        enemy_x = random.randint(500, 2000)
        enemy_y = random.randint(200, 1200)
        new_Enemy = pyglet.sprite.Sprite(enemy_image
                                        , enemy_x, enemy_y)
        enemies.append(new_Enemy)
    return enemies

