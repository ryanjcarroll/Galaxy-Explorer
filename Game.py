import pygame as pg
import random
pg.init()

##colors
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

##game variables
score = 0
lives = 5
level_count = 1
bullet_rate = 20 ##how many clicks for 2 bullets to spawn
bullet_speed = 20 ##how many clicks for bullet to get to player
spawn_bullets = True

##window and display properties
win_width = 500
win_height = 600
win = pg.display.set_mode((win_width, win_height))
pg.display.set_caption("Space Lasers Game") 
bg = pg.image.load("images/background.png")

##sounds and music
laser_sound = pg.mixer.Sound("sounds/laser.wav")
impact_sound = pg.mixer.Sound("sounds/impact.wav")
hit_sound = pg.mixer.Sound("sounds/hit.wav")
music = pg.mixer.music.load("sounds/music.mp3")
pg.mixer.music.play(-1)

##redraws the background image
def redraw_background():
    win.blit(bg, (0,0))
    
##class which represents the player character
class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("images/ship.png")
        self.rect = self.image.get_rect()

        self.rect.x = int(win_width * 0.5) - int(self.rect.width * 0.5)
        self.rect.y = win_height - 100
        self.vel = 15

##class which represents fired bullets
class Bullet(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        self.image = pg.Surface([5,10])
        self.image.fill(hunter)
        self.rect = self.image.get_rect()  
        self.vel = 25
        laser_sound.play()
        
    def update(self):
        self.rect.y -= self.vel

##class which represents enemy-fired bullets
class EnemyBullet(pg.sprite.Sprite):
    def __init__(self):
        global bullet_vel
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface([5,20])
        self.image.fill(magenta)
        self.rect = self.image.get_rect()  
        self.vel = int(win_height / bullet_speed)
        
    def update(self):
        self.rect.y += self.vel

##class which represents enemies
class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)

        rand_int = random.randint(1,16)
        self.image = pg.image.load("images/asteroid" + str(rand_int) + ".png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

##enemy which drops extra points on death
class EnemyExtraPoints(Enemy):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
    
        self.image = pg.Surface([30,30])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

##extra points capsule
class Extra_points(pg.sprite.Sprite):
    def __init__self(x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([10,10])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vel = 10
    def update():
        self.rect.y += self.vel
        
##class represents the health bar of the player
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

        if(lives == 4): ##this happens before lives is updated
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

##sets the scoreboard text
def set_score(score):
    smallfont = pg.font.Font(None, 25)
    text = smallfont.render("Score: "  + str(score), True, white)
    win.blit(text, [5,win_height - 30])
    
##method runs when the player is hit by a bullet
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

##utility method for displaying banner text
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

##displays a banner message to the screen
def message_display(text, size):
    font = pg.font.Font(None, size)
    TextSurf, TextRect = text_objects(text, font)
    TextRect.center = (int(win_width / 2), int(win_height / 2))
    win.blit(TextSurf, TextRect)    

##pause functionality
def pause():
    paused = True
    while(paused):
        pg.time.delay(80)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    paused = False
        redraw_background
        sprite_list.draw(win)
        message_display("Paused - Escape to continue.", 36)
        pg.display.update()
                

##sprite list
player_list = pg.sprite.Group()
sprite_list = pg.sprite.Group()
bullet_list = pg.sprite.Group()
enemy_list = pg.sprite.Group()
enemy_bullet_list = pg.sprite.Group()
special_enemy_list = pg.sprite.Group()

##create health bar
health_bar = HealthBar()
sprite_list.add(health_bar)

##create player sprite
player = Player()
player_list.add(player)
sprite_list.add(player)

##create enemy sprites
def spawn_enemies():
    spawn_x = 50
    spawn_y = 50

    while(spawn_x < win_width - 50):
        while(spawn_y < win_height - 300):
            enemy = Enemy(spawn_x, spawn_y)
            sprite_list.add(enemy)
            enemy_list.add(enemy)

            spawn_y += 50
        spawn_y = 50
        spawn_x += 50

spawn_enemies()

##draw initial sprites
redraw_background()
sprite_list.draw(win)
pg.display.update()

##countdown to game start
def countdown(num):
    count_from = num
    current_count = num

    message_display("Level " + str(level_count), 72)
    pg.display.update()
    pg.time.delay(1000)
    redraw_background()
    sprite_list.draw(win)
    pg.display.update()
        
    for i in range(count_from, 0, -1):
        message_display(str(current_count), 72)
        pg.display.update()
        pg.time.delay(1000)
        redraw_background()
        sprite_list.draw(win)
        current_count -= 1
        
countdown(3)

##main game loop
run = True
level_complete = False
game_over = False
count = 0   
first_x = player.rect.x
while run:
    pg.time.delay(80)
    
    ##check if level is completed
    if(level_complete and len(bullet_list) == 0 and len(enemy_bullet_list) == 0):
        spawn_enemies()
        pg.display.update()
        spawn_bullets = True
        level_complete = False

        ##increase difficulty of next level
        level_count += 1
        bullet_rate = int(bullet_rate * 0.9)
        bullet_speed = int(bullet_speed * 0.95)
        player_list.add(player)
        countdown(3)
        
    ##count 10k ticks and then reset
    if count > 10000:
        count = 0
    else:
        count += 1

    ##event detections
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

    ##keypress detections
    keys = pg.key.get_pressed()
    
    if keys[pg.K_LEFT]:
        if(player.rect.x > 0):
            player.rect.x -= player.vel
    if keys[pg.K_RIGHT]:
        if(player.rect.x < win_width - player.rect.width):
            player.rect.x += player.vel

    ##spawn enemy bullets
    if spawn_bullets:
        ##spawn enemy bullets ahead of the player
        if count % bullet_rate == 0:
            eb = EnemyBullet()
            eb.rect.y = 0

            ##if player is moving left, right, or neither
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
                       
            ##add bullet to game
            enemy_bullet_list.add(eb)
            sprite_list.add(eb)               

        ##spawn enemy bullets based on the player's average movement
        if count % bullet_rate == int(bullet_rate / 2):
            eb = EnemyBullet()
            eb.rect.y = 0
            
            ##find how far the player has moved since last iteration
            second_x = player.rect.x
            diff_x = second_x - first_x

            ##calculate average velocity and expected pos 10 clicks from now
            avg_vel = float(diff_x) / 10
            x_side = (avg_vel / float(eb.vel)) * (player.rect.y - eb.rect.y)
            eb.rect.x = player.rect.x + int(x_side) + int(player.rect.width /2)

            if(eb.rect.x > win_width):
                eb.rect.x = win_width - 10
            if(eb.rect.x < 0):
                eb.rect.x = 10

            ##set first_x for the next iteration
            first_x = second_x
           
            ##add bullet to game
            enemy_bullet_list.add(eb)
            sprite_list.add(eb)
        
    ##update sprites
    sprite_list.update()

    ##bullet mechanics 
    for bullet in bullet_list:
        if(bullet.rect.y < bullet.rect.height):
            bullet.vel *= -1
            bullet.image.fill(red)
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

    ##enemy bullet mechanics
    for bullet in enemy_bullet_list:
        if(bullet.rect.y > win_height + bullet.rect.height):
            enemy_bullet_list.remove(bullet)
            sprite_list.remove(bullet)
        elif(pg.sprite.spritecollide(bullet, player_list, False)):
            enemy_bullet_list.remove(bullet)
            sprite_list.remove(bullet)
            hit_by_bullet()
    
    ##refresh window and sprite
    redraw_background()
    sprite_list.draw(win)
    set_score(score)

    ##check if game is over
    if(game_over):
        message_display("Game Over", 96)
        spawn_bullets = False
        player_list.remove(player)
    
    pg.display.update()
    
pg.quit()
