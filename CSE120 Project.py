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



    window = pyglet.window.Window(2000, 1400)
    character = pyglet.resource.image('images (1).jpg')
    attack_image = pyglet.resource.image('furina_image.png')
    center_image(character)
    center_image(attack_image)
    playerObject = PlayerClass.Player(character, x= 1500, y=1000)


    keys = key.KeyStateHandler()



    @window.event
    def on_draw():
        window.clear()
        if game_Active:
            if playerObject.state['alive']:
                playerObject.draw()
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
            if not playerObject.state['hit']:
                for enemy in enemies:
                    if (enemy.x <= playerObject.x + 500 and enemy.x >= playerObject.x - 500) and (
                            enemy.y <= playerObject.y + 500 and enemy.y >= playerObject.y - 500):
                        playerObject.stats['health'] -= 10.
                        playerObject.state['hit'] = True
            if playerObject.stats['health'] <= 0:
                playerObject.state['alive'] = False
            if playerObject.state['attacking']:
                for enemy in enemies:
                    if (enemy.x <= playerObject.x + 500 and enemy.x >= playerObject.x - 500) and (enemy.y <= playerObject.y + 500 and enemy.y >= playerObject.y - 500):
                        enemies.remove(enemy)


    def enemy_spawn_timer(dt):
        if game_Active:
            stickEnemy.spawn_Enemy(1,playerObject.x, playerObject.y)




    pyglet.clock.schedule_interval(playerObject.update, 1/60)
    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.clock.schedule_interval(enemy_spawn_timer, 1)
    pyglet.app.run()
