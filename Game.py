import pygame as pg
import random
import os
import sys
pg.init()

# colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
lime = (0,255,0)
hunter = (63,122,77)
magenta = (255,0,144)
yellow = (255,255,0)
orange = (255,165,0)
red_orange = (255,83,73)

# game variables
score = 0
lives = 5
level_count = 1
bullet_rate = 60 # how many clicks for 2 bullets to spawn
bullet_speed = 40 # how many clicks for bullet to get to player
spawn_bullets = True
game_over = False
level_complete = False

# path names
current_path = os.path.dirname(sys.executable) # sys.executable
images_path = os.path.join(current_path, "images")
sounds_path = os.path.join(current_path, "sounds")

# resource path creator
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# window and display properties
win_width = 500
win_height = 600
mspf = 40 # milliseconds per frame
win = pg.display.set_mode((win_width, win_height))
pg.display.set_caption("Galaxy Explorer")
bg = pg.image.load(resource_path("images/background.png"))

# sounds and music
laser_sound = pg.mixer.Sound(resource_path("sounds/laser.wav"))
impact_sound = pg.mixer.Sound(resource_path("sounds/impact.wav"))
hit_sound = pg.mixer.Sound(resource_path("sounds/hit.wav"))
music = pg.mixer.music.load(resource_path("sounds/music.wav"))
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.1)

# redraws the background image
def redraw_background():
    win.blit(bg, (0,0))   
    
# class which represents the player character
class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(resource_path("images/ship.png"))
        self.rect = self.image.get_rect()

        self.rect.x = int(win_width * 0.5) - int(self.rect.width * 0.5)
        self.rect.y = win_height - 100
        self.vel = 15

# class which represents fired bullets
class Bullet(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        self.image = pg.image.load(resource_path("images/bullet.png"))
        self.rect = self.image.get_rect()  
        self.vel = 25
        laser_sound.play()
        
    def update(self):
        self.rect.y -= self.vel

# class which represents enemy-fired bullets
class EnemyBullet(pg.sprite.Sprite):
    def __init__(self):
        global bullet_vel
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(resource_path("images/bullet_enemy.png"))
        self.rect = self.image.get_rect()  
        self.vel = int(win_height / bullet_speed)
        
    def update(self):
        self.rect.y += self.vel

# class which represents enemies
class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, num):
        pg.sprite.Sprite.__init__(self)
       
        ran = random.randint(1,4)
        self.image = pg.image.load(resource_path("images/asteroid") + str(num) + "." + str(ran) + ".png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
# class represents the health bar of the player
class HealthBar(pg.sprite.Sprite):
    width = win_width - 10
    height = 35
    
    def __init__(self):
        width = self.width
        height = self.height
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([width, height])
        self.image.fill(lime)
        self.rect = self.image.get_rect()
        self.rect.x = 5
        self.rect.y = 5
        
    def lose_life(self):
        width = self.width
        height = self.height
        new_width = self.rect.width - int(self.rect.width / lives)
        if(new_width == 0):
            new_width = 5
        
        self.image = pg.Surface([new_width, height])

        if(lives == 4): # this happens before lives is updated
            self.image.fill(yellow)
        elif(lives ==3):
            self.image.fill(orange)
        elif(lives == 2):
            self.image.fill(red_orange)
        elif(lives == 1):
            self.image.fill(red)
        else:
            self.image.fill(lime)
        self.rect = self.image.get_rect()
        self.rect.x = 5
        self.rect.y = 5

# create enemy sprites
def spawn_enemies():
    spawn_x = 50
    spawn_y = 50

    # pick two asteroid types to spawn
    asteroid_numbers = random.sample(range(1,7),2)

    while(spawn_x < win_width - 50):
        while(spawn_y < win_height - 300):
            ran = random.choice(asteroid_numbers)
            enemy = Enemy(spawn_x, spawn_y, ran)
            sprite_list.add(enemy)
            enemy_list.add(enemy)

            spawn_y += 50
        spawn_y = 50
        spawn_x += 50

# sets the scoreboard text
def set_score(score):
    smallfont = pg.font.Font(None, 25)
    text = smallfont.render("Score: "  + str(score), True, white)
    win.blit(text, [5,win_height - 30])

# sets the level text
def set_level(level):
    smallfont = pg.font.Font(None, 25)
    text = smallfont.render("Level: "  + str(level), True, white)
    width = text.get_rect().width
    win.blit(text, [win_width - 5 - width,win_height - 30])
    
# method runs when the player is hit by a bullet
def hit_by_bullet():
    global lives
    global game_over
    impact_sound.play()
    if lives > 1:
        health_bar.lose_life()
        lives -= 1
        print("Hit by bullet: ", lives, " lives remaining")
    else:
        health_bar.lose_life()
        game_over = True

# utility method for displaying banner text
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

# displays a banner message to the screen
def message_display(text, size):
    font = pg.font.Font(None, size)
    TextSurf, TextRect = text_objects(text, font)
    TextRect.center = (int(win_width / 2), int(win_height / 2))
    win.blit(TextSurf, TextRect)    

# pause functionality
def pause():
    global game_over
    if(not game_over):
        paused = True
        while(paused):
            pg.time.delay(80)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        paused = False
            redraw_background()
            sprite_list.draw(win)
            message_display("Paused", 72)

            font = pg.font.Font(None, 38)
            TextSurf, TextRect = text_objects("Esc to continue", font)
            TextRect.center = (int(win_width / 2), int(3 * win_height / 5))
            win.blit(TextSurf, TextRect)    
            pg.display.update()
    else:
        main_menu()
                
# intro menu
def main_menu():
    intro_run = True
    count = 0
    while(intro_run):
        pg.time.delay(80)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    intro_run = False

        redraw_background()

        font = pg.font.Font(None, 80)
        TextSurf, TextRect = text_objects("Galaxy Explorer", font)
        TextRect.center = (int(win_width / 2), int(win_height / 3))
        win.blit(TextSurf, TextRect)    

        if(count == 20):
            font = pg.font.Font(None, 36)
            TextSurf, TextRect = text_objects("Press Space to Begin", font)
            TextRect.center = (int(win_width / 2), int(win_height / 2))
            win.blit(TextSurf, TextRect)
        elif(count < 20):
            count += 1
        
        pg.display.update()
    initialize_game()
    countdown(3)
    main_loop()

# creates all game assets needed to run the main loop
def initialize_game():

    global player_list, sprite_list, bullet_list, enemy_list, enemy_bullet_list
    global health_bar, player
    global level_count, score, lives
    global game_over, level_complete
    global spawn_bullets, bullet_rate, bullet_speed

    level_count, score, lives = level_count, score, lives
    game_over, level_complete = game_over, level_complete
    spawn_bullets, bullet_rate, bullet_speed = spawn_bullets, bullet_rate, bullet_speed

    # sprite list
    player_list = pg.sprite.Group()
    sprite_list = pg.sprite.Group()
    bullet_list = pg.sprite.Group()
    enemy_list = pg.sprite.Group()
    enemy_bullet_list = pg.sprite.Group()

    # create health bar
    health_bar = HealthBar()
    sprite_list.add(health_bar)

    # create player sprite
    player = Player()
    player_list.add(player)
    sprite_list.add(player)

    spawn_enemies()

    # draw initial sprites
    redraw_background()
    sprite_list.draw(win)
    pg.display.update()

# countdown to game start
def countdown(num):

    clock = pg.time.Clock()
    
    run_countdown = True
    count_from = num
    current_count = num
    time_elapsed = 0
    
    while(run_countdown):
        pg.time.delay(mspf)
        dt = clock.tick()
        time_elapsed += dt

        if(time_elapsed < 1000):
            redraw_background()
            set_score(score)
            set_level(level_count)
            sprite_list.draw(win)
            message_display("Level " + str(level_count), 72)
            pg.display.update()
        elif(time_elapsed < 2000):
            redraw_background()
            set_score(score)
            set_level(level_count)
            sprite_list.draw(win)
            message_display("3", 72)
            pg.display.update()
        elif(time_elapsed < 3000):
            redraw_background()
            set_score(score)
            set_level(level_count)
            sprite_list.draw(win)
            message_display("2", 72)
            pg.display.update()
        elif(time_elapsed < 4000):
            redraw_background()
            set_score(score)
            set_level(level_count)
            sprite_list.draw(win)
            message_display("1", 72)
            pg.display.update()
        else:
            run_countdown = False  

# main game loop
def main_loop():
    #global variables
    global spawn_bullets, bullet_rate, bullet_speed
    global score, lives, level_count
    global game_over, level_complete
    global mspf
    
    # main game loop
    run = True
    count = 0   
    first_x = player.rect.x
    while run:
        pg.time.delay(mspf)
        
        # check if level is completed
        if(level_complete and len(bullet_list) == 0 and len(enemy_bullet_list) == 0):
            spawn_enemies()
            pg.display.update()
            spawn_bullets = True
            level_complete = False

            # increase difficulty of next level
            level_count += 1
            bullet_rate = int(bullet_rate * 0.9)
            bullet_speed = int(bullet_speed * 0.95)
            player_list.add(player)
            countdown(3)
            
        # count 10k ticks and then reset
        if count > 10000:
            count = 0
        else:
            count += 1

        # event detections
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif(event.type == pg.KEYDOWN):
                if(event.key == pg.K_ESCAPE):
                    pause() 
                elif(event.key == pg.K_SPACE):
                    if(spawn_bullets):
                        bullet = Bullet()
                        bullet.rect.x = player.rect.x + int(float(player.rect.width) / 2)
                        bullet.rect.y = player.rect.y
                           
                        sprite_list.add(bullet)
                        bullet_list.add(bullet)
                elif(event.key == pg.K_r):
                    if(game_over):
                        initialize_game()
                        countdown(3)
                        main_loop()

        # keypress detections
        keys = pg.key.get_pressed()
        
        if keys[pg.K_LEFT]:
            if(player.rect.x > 0):
                player.rect.x -= player.vel
        if keys[pg.K_RIGHT]:
            if(player.rect.x < win_width - player.rect.width):
                player.rect.x += player.vel

        # spawn enemy bullets
        if spawn_bullets:
            # spawn enemy bullets ahead of the player
            if count % bullet_rate == 0:
                eb = EnemyBullet()
                eb.rect.y = 0

                # if player is moving left, right, or neither
                if keys[pg.K_LEFT]:
                    x_left = (float(player.vel)/float(eb.vel)) * (player.rect.y - eb.rect.y)
                    eb.rect.x = int(player.rect.x - x_left) + int(player.rect.width /2)
                    if(eb.rect.x < 0):
                        eb.rect.x = 10
                elif keys[pg.K_RIGHT]:
                    x_right = (float(player.vel)/float(eb.vel)) * (player.rect.y - eb.rect.y)
                    eb.rect.x = int(player.rect.x + x_right) + int(player.rect.width /2)
                    if(eb.rect.x > win_width):
                        eb.rect.x = win_width - 10
                else:
                    eb.rect.x = player.rect.x + int(player.rect.width /2)
                           
                # add bullet to game
                enemy_bullet_list.add(eb)
                sprite_list.add(eb)               

            # spawn enemy bullets based on the player's average movement
            if count % bullet_rate == int(bullet_rate / 2):
                eb = EnemyBullet()
                eb.rect.y = 0
                
                # find how far the player has moved since last iteration
                second_x = player.rect.x
                diff_x = second_x - first_x

                # calculate average velocity and expected pos 10 clicks from now
                avg_vel = float(diff_x) / 10
                x_side = (avg_vel / float(eb.vel)) * (player.rect.y - eb.rect.y)
                eb.rect.x = player.rect.x + int(x_side) + int(player.rect.width /2)

                if(eb.rect.x > win_width):
                    eb.rect.x = win_width - 10
                if(eb.rect.x < 0):
                    eb.rect.x = 10

                # set first_x for the next iteration
                first_x = second_x
               
                # add bullet to game
                enemy_bullet_list.add(eb)
                sprite_list.add(eb)
            
        # update sprites
        sprite_list.update()

        # bullet mechanics 
        for bullet in bullet_list:
            if(bullet.rect.y < bullet.rect.height):
                bullet.vel *= -1
                bullet.image = pg.image.load(resource_path("images/bullet_red.png"))
            elif(bullet.rect.y > win_height + bullet.rect.height):
                bullet_list.remove(bullet)
                sprite_list.remove(bullet)
            elif(pg.sprite.spritecollide(bullet, player_list, False)):
                bullet_list.remove(bullet)
                sprite_list.remove(bullet)
                hit_by_bullet()
            elif(pg.sprite.spritecollide(bullet, enemy_list, True)):
                sprite_list.remove(bullet)
                bullet_list.remove(bullet)
                hit_sound.play()
                score += 10
                if(len(enemy_list) == 0):
                    player_list.remove(player)
                    level_complete = True
                    spawn_bullets = False

        # enemy bullet mechanics
        for bullet in enemy_bullet_list:
            if(bullet.rect.y > win_height + bullet.rect.height):
                enemy_bullet_list.remove(bullet)
                sprite_list.remove(bullet)
            elif(pg.sprite.spritecollide(bullet, player_list, False)):
                enemy_bullet_list.remove(bullet)
                sprite_list.remove(bullet)
                hit_by_bullet()
        
        # refresh window, text, and sprites
        redraw_background()
        sprite_list.draw(win)
        set_level(level_count)
        if not game_over:
            set_score(score)

        # check if game is over
        if(game_over):
            message_display("Game Over", 96)

            font = pg.font.Font(None, 38)
            TextSurf, TextRect = text_objects("Score: " + str(score), font)
            TextRect.center = (int(win_width / 2), int(6 * win_height / 10))
            win.blit(TextSurf, TextRect)

            font = pg.font.Font(None, 30)
            TextSurf, TextRect = text_objects("Esc to main menu", font)
            TextRect.center = (int(win_width / 2), int(7 * win_height / 10))
            win.blit(TextSurf, TextRect)

            font = pg.font.Font(None, 30)
            TextSurf, TextRect = text_objects("R to restart", font)
            TextRect.center = (int(win_width / 2), int(15 * win_height / 20))
            win.blit(TextSurf, TextRect)

            spawn_bullets = False
            player_list.remove(player)
        
        pg.display.update()

# main execution runs in the following order:
# main_menu -> initialize_game -> countdown -> main_loop
main_menu()
