import pyglet
from pyglet.window import key, mouse
import PlayerClass
import stickEnemy
import Projectile
import Melee
import random

if __name__ == '__main__':
    #tracks if game is active and what objects exist, except for unique objects
    game_Active = False
    game_objects = []
    #sets image anchor to center of image
    def center_image(image):
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
    #window and image set up
    window = pyglet.window.Window(2000, 1400)
    character = pyglet.resource.image('player.png')
    attack_image = pyglet.resource.image('sword.jpg')
    projectile_image = pyglet.resource.image('arrow2.jpg')
    enemy_image = pyglet.resource.image('Basic_human_drawing.png')
    #adjust image anchors
    center_image(character)
    center_image(attack_image)
    center_image(projectile_image)
    center_image(enemy_image)
    #set up player and melee attack objects and keyboard controls
    playerObject = PlayerClass.Player(character, x= 500, y=1000)
    meleeObject = Melee.Sword(attack_image, playerObject.x + 50, playerObject.y)
    meleeObject.scale = .25
    playerObject.scale = .75
    keys = key.KeyStateHandler()

    #enemy spawn command
    def spawn_Enemy(amount, player_x, player_y):
        for i in range(amount):
            enemy_x = random.randint(100, 1900)
            enemy_y = random.randint(200, 1200)
            while (enemy_x <= (player_x + 500) and enemy_x >= (player_x - 500)) or (
                    enemy_y <= (player_y + 500) and enemy_y >= (player_y - 500)):
                enemy_x = random.randint(500, 1500)
                enemy_y = random.randint(200, 1200)
            new_Enemy = stickEnemy.Enemy( enemy_image, enemy_x, enemy_y)
            new_Enemy.scale = .5
            game_objects.append(new_Enemy)


    #create a projectile for player
    def fire(start_x, start_y, target_x, target_y):
        attack = Projectile.Arrow(target_x, target_y, projectile_image, start_x, start_y)
        attack.scale = .5
        game_objects.append(attack)

    #draws all objects
    @window.event
    def on_draw():
        window.clear()
        if game_Active:
            if playerObject.state['alive']:
                playerObject.draw()
            if meleeObject.active:
                meleeObject.draw()
            for object in game_objects:
                object.draw()



    @window.event
    def on_key_press(symbol, modifiers):
        #player movement
        playerObject.on_key_press(symbol, modifiers)
        #player melee attack
        if symbol == key.L and playerObject.cooldown == 0:
            playerObject.start_attack()
            meleeObject.active = True
            meleeObject.timer = 30

        #game start
        if symbol == key.ENTER:
            global game_Active
            game_Active = True

    @window.event
    def on_key_release(symbol, modifiers):
        playerObject.on_key_release(symbol, modifiers)


    @window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == mouse.LEFT and playerObject.bow_cooldown == 0:
            fire(playerObject.x ,playerObject.y, x, y)
            playerObject.bow_cooldown = 30



    def update(dt):
        if game_Active and playerObject.state['alive']:
            #runs an internal timer to the melee object, which controls how long it is active
            meleeObject.update()
            #player hit detection
            if not playerObject.state['hit']:
                for object in game_objects:
                    if isinstance(object, stickEnemy.Enemy):
                        if (object.x <= playerObject.x + 248 and object.x >= playerObject.x - 248) and (
                                object.y <= playerObject.y + 409 and object.y >= playerObject.y - 409):
                            playerObject.stats['health'] -= 5
                            playerObject.state['hit'] = True
                            break
            #offsets the melee object based on the direction the player last looked.
            if meleeObject.active:
                if playerObject.lastKey == key.D:
                    meleeObject.x = playerObject.x + 75
                    meleeObject.y = playerObject.y
                if playerObject.lastKey == key.A:
                    meleeObject.x = playerObject.x - 75
                    meleeObject.y = playerObject.y
                if playerObject.lastKey == key.S:
                    meleeObject.x = playerObject.x
                    meleeObject.y = playerObject.y - 75
                if playerObject.lastKey == key.W:
                    meleeObject.x = playerObject.x
                    meleeObject.y = playerObject.y + 75
            #player death detection
            if playerObject.stats['health'] <= 0:
                playerObject.state['alive'] = False

            #player damage state reset
            if playerObject.state['hit']:
                pyglet.clock.schedule_once(playerObject.reset_hit, 1)

            #loop to check for game action of every non-player object
            for object in game_objects:
                if isinstance(object, Projectile.Arrow):
                    object.timer -= 1
                    object.update()

                if isinstance(object, stickEnemy.Enemy):
                    object.move(playerObject)
                    if meleeObject.active:
                        if ((object.x <= meleeObject.x + 363 and object.x >= meleeObject.x - 363) and
                                (object.y >= meleeObject.y - 414 and object.y >= meleeObject.y - 414)):
                            object.dead = True
                    for x in range(game_objects.index(object), len(game_objects)):
                        if isinstance(game_objects[x], Projectile.Arrow):
                            if ((object.x <= game_objects[x].x + 194 and object.x >= game_objects[x].x - 194) and
                                    (object.y <= game_objects[x].y + 185 and object.y >= game_objects[x].y - 185)):
                                object.dead = True
                                game_objects[x].dead = True
                                break

                #removes the object from the list game_Objects if it is dead
                if object.dead:
                    game_objects.remove(object)

    #enemy spawner
    def enemy_spawn_timer(dt):
        if game_Active:
            spawn_Enemy(1,playerObject.x, playerObject.y)

    #all projectiles made by the player have an internal timer, this tracks timer,
    #when the timer runs out the projectile is cleared and removed from game_Objects
    def clear_projectile_timer(dt):
        if game_Active:
            for object in game_objects:
                if isinstance(object, Projectile.Arrow):
                    if object.timer == 0:
                        game_objects.remove(object)

    #runs every single update function that runs the game
    pyglet.clock.schedule_interval(playerObject.update, 1/60)
    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.clock.schedule_interval(enemy_spawn_timer, 1)
    pyglet.clock.schedule_interval(clear_projectile_timer, 1/60)

    #create game window on run
    pyglet.app.run()