from pygame import *
from random import choice
mixer.init()
font.init()

#створи вікно гри
TILESIZE = 45
MAP_WIDTH, MAP_HEIGHT = 15, 15
WIDTH, HEIGHT = TILESIZE*MAP_WIDTH, TILESIZE*MAP_HEIGHT
FPS = 60

font1 = font.SysFont('Roboto', 30)
font2 = font.SysFont('Roboto', 30)


mixer.music.load('jungles.ogg')
mixer.music.set_volume(0.2)
mixer.music.play(loops=-1)

kick_sound = mixer.Sound('kick.ogg')
kick_sound.play()
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption('Доганялки')
clock = time.Clock() #game timer

bg = image.load("floor_bg.png")
bg = transform.scale(bg, (WIDTH, HEIGHT)) #resize bg

hero = image.load('hero.png')
enemy = image.load('cyborg.png')

treasure_img = image.load("treasure.png")
skeleton_img = image.load('Skeleton.png')
wall1_img = image.load('wall1.png')
wall2_img = image.load('wall2.png')
wall3_img = image.load('wall3.png')
wall4_img = image.load('wall4.png')
wall5_img = image.load('wall5.png')
wall6_img = image.load('wall6.png')
wall7_img = image.load('wall7.png')
floor_img = image.load('floor.png')

sprites = sprite.Group()
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, width=60, height=60, x=100, y=250):
        super().__init__()
        self.image = transform.scale(sprite_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        sprites.add(self)
    def draw(self, window):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    
    def __init__(self, sprite_image, width=60, height=60, x=100, y=250):
        super().__init__(sprite_image,TILESIZE,TILESIZE, x, y)
        sprites.remove(self)
        self.hp = 100
        self.damage = 20
        self.coins = 0
        self.speed = 5

    def update(self):
        global hp_text
        self.old_pos = self.rect.x, self.rect.y
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
           self.rect.y -= self.speed
        if keys[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        collidelist = sprite.spritecollide(self, walls, False)
        if len(collidelist) > 0:
            self.rect.x, self.rect.y = self.old_pos

        collidelist = sprite.spritecollide(self, enemys, False)
        if len(collidelist) > 0:
            self.hp -= 20
            hp_text = font1.render(f'HP:{self.hp}', True, (255, 255, 255))
            self.rect.x, self.rect.y = self.start_x, self.start_y
            

enemys = sprite.Group()
class Enemy(GameSprite):
    def __init__(self, x, y):
        super().__init__(enemy, TILESIZE, TILESIZE, x, y)
        self.hp = 100
        self.damage = 20
        self.speed = 1
        self.dir_list = ['left', 'right', 'up', 'down']
        self.dir = choice(self.dir_list)
        enemys.add(self)

    def update(self):
        self.old_pos = self.rect.x, self.rect.y
        if self.dir == 'right':
            self.rect.x += self.speed
        if self.dir == 'left':
            self.rect.x -= self.speed
        if self.dir == 'up':
            self.rect.y -= self.speed
        if self.dir == 'down':
            self.rect.y += self.speed

        collidelist = sprite.spritecollide(self, walls, False)
        if len(collidelist) > 0:
            self.rect.x, self.rect.y = self.old_pos
            self.dir = choice(self.dir_list)

walls = sprite.Group()
class Wall1(GameSprite):
    def __init__(self, x, y):
        super().__init__(wall1_img, TILESIZE, TILESIZE, x, y)      
        walls.add(self)

class Wall2(GameSprite):
    def __init__(self, x, y):
        super().__init__(wall2_img, TILESIZE, TILESIZE, x, y)      
        walls.add(self)

class Wall3(GameSprite):
    def __init__(self, x, y):
        super().__init__(wall3_img, TILESIZE, TILESIZE, x, y)      
        walls.add(self)

class Wall4(GameSprite):
    def __init__(self, x, y):
        super().__init__(wall4_img, TILESIZE, TILESIZE, x, y)      
        walls.add(self)

class Wall5(GameSprite):
    def __init__(self, x, y):
        super().__init__(wall5_img, TILESIZE, TILESIZE, x, y)      
        walls.add(self)

class Wall6(GameSprite):
    def __init__(self, x, y):
        super().__init__(wall6_img, TILESIZE, TILESIZE, x, y)      
        walls.add(self)


class Wall7(GameSprite):
    def __init__(self, x, y):
        super().__init__(wall7_img, TILESIZE, TILESIZE, x, y)      
        walls.add(self)

player = Player(hero)
hp_text = font1.render(f'HP:{player.hp}', True, (255, 255, 255))
finish_text = font2.render('Game Over!', True, (255, 0, 15))
treasure = None
with open('map.txt', 'r') as file:
    x, y = 0, 0
    map = file.readlines()
    for row in map:
        floor = GameSprite(floor_img, TILESIZE, TILESIZE, x,y)
        for symbol in row:
            floor = GameSprite(floor_img, TILESIZE, TILESIZE, x,y)
            if symbol == '1':
                Wall1(x, y)
            if symbol == '2':
                Wall2(x,y)
            if symbol == '3':
                Wall3(x,y)
            elif symbol == 's':
                skeleton = GameSprite(skeleton_img, TILESIZE+50, TILESIZE, x, y)
            elif symbol == 'P':

                player.rect.x = x
                player.rect.y = y
                player.start_x, player.start_y = player.rect.x, player.rect.y
            elif symbol == "e":
                Enemy(x, y)
            elif symbol == 't':
                treasure = GameSprite(treasure_img, TILESIZE, TILESIZE, x, y)
            elif symbol == '4':
                Wall4(x,y)
            elif symbol == '5':
                Wall5(x,y)
            elif symbol == '6':
                Wall6(x,y)
            elif symbol == '7':
                Wall7(x,y)
            x += TILESIZE
        y+=TILESIZE
        x = 0

finish = False
while True:
#оброби подію «клік за кнопкою "Закрити вікно"»
    for e in event.get():
        if e.type == QUIT:
            quit()
    
    window.blit(bg, (0,0))
    sprites.draw(window)
    if not finish == True:
        enemys.update()
        player.update()

    if player.hp <= 0:
        finish = True

    if sprite.collide_rect(player, treasure):
        finish = True
        finish_text = font2.render('U Won!', True, (255, 0, 15))
    if finish:
        window.blit(finish_text, (500, 500))
    window.blit(hp_text, (10, 10))
    player.draw(window)

    display.update()
    clock.tick(FPS)