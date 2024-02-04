from pygame import *
from random import choice
mixer.init()


#створи вікно гри
TILESIZE = 45
MAP_WIDTH, MAP_HEIGHT = 20, 15
WIDTH, HEIGHT = TILESIZE*MAP_WIDTH, TILESIZE*MAP_HEIGHT
FPS = 60


mixer.music.load('jungles.ogg')
mixer.music.set_volume(0.2)
mixer.music.play(loops=-1)

kick_sound = mixer.Sound('kick.ogg')
kick_sound.play()
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption('Доганялки')
clock = time.Clock() #game timer

bg = image.load("background.jpg")
bg = transform.scale(bg, (WIDTH, HEIGHT)) #resize bg

hero = image.load('hero.png')
enemy = image.load('cyborg.png')
wall = image.load('wall.png')


class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, width=60, height=60, x=100, y=250):
        super().__init__()
        self.image = transform.scale(sprite_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, window):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def __init__(self, sprite_image, width=60, height=60, x=100, y=250):
        super().__init__(sprite_image,TILESIZE,TILESIZE, x, y)
        self.hp = 100
        self.damage = 20
        self.coins = 0
        self.speed = 5

    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
           self.rect.y -= self.speed
        if keys[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed
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
class Wall(GameSprite):
    def __init__(self, x, y):
        super().__init__(wall, TILESIZE, TILESIZE, x, y)      
        walls.add(self)

player = Player(hero)

with open('map.txt', 'r') as file:
    x, y = 0, 0
    map = file.readlines()
    for row in map:
        for symbol in row:
            if symbol == 'w':
                Wall(x, y)
            elif symbol == 'P':
                player.rect.x = x
                player.rect.y = y
            elif symbol == "e":
                Enemy(x, y)
            x += TILESIZE
        y+=TILESIZE
        x = 0


while True:
#оброби подію «клік за кнопкою "Закрити вікно"»
    for e in event.get():
        if e.type == QUIT:
            quit()

    window.blit(bg, (0,0))
    walls.draw(window)
    enemys.draw(window)
    enemys.update()
    player.update()

    player.draw(window)
    display.update()
    clock.tick(FPS)