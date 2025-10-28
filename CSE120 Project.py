import pyglet
from pyglet.window import key
import PlayerClass
import stickEnemy

if __name__ == '__main__':

    game_Active = False
    enemies = stickEnemy.enemies

    def center_image(image):
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2



    window = pyglet.window.Window(3000, 1400)
    character = pyglet.resource.image(image_here)
    attack_image = pyglet.resource.image(image_here)
    center_image(character)
    center_image(attack_image)
    playerObject = PlayerClass.Player(character, x= 1500, y=1000)


    keys = key.KeyStateHandler()
    hitBox = pyglet.shapes.Rectangle(playerObject.x-50, playerObject.y-50, 100, 100)
    player_Stats = {'health' : 100, 'alive' : True, 'attacking' : False}


    @window.event
    def on_draw():
        window.clear()
        if game_Active:
            if player_Stats['alive']:
                playerObject.draw()
                hitBox.draw()
            for enemy in enemies:
                enemy.draw()

    @window.event
    def on_key_press(symbol, modifiers):
        playerObject.on_key_press(symbol, modifiers)
        if symbol == key.L:
            playerObject.start_attack(attack_image)
        if symbol == key.ENTER:
            global game_Active
            game_Active = True



    @window.event
    def on_key_release(symbol, modifiers):
        playerObject.on_key_release(symbol, modifiers)

    def update(dt):
        if game_Active:
            hitBox.x = playerObject.x - 50
            hitBox.y = playerObject.y - 50
            if player_Stats['health'] <= 0:
                player_Stats['alive'] = False


    def enemy_spawn_timer(dt):
        if game_Active:
            stickEnemy.spawn_Enemy(1)



    pyglet.clock.schedule_interval(playerObject.update, 1/60)
    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.clock.schedule_interval(enemy_spawn_timer, 1)
    pyglet.app.run()

