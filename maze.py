from pygame import *
mixer.init()


#створи вікно гри
WIDTH, HEIGHT = 800, 600
FPS = 360

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
        super().__init__(sprite_image, width, height, x, y)
        self.hp = 100
        self.damage = 20
        self.coins = 0
        self.speed = 1

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

        

player = Player(hero)

while True:
#оброби подію «клік за кнопкою "Закрити вікно"»
    for e in event.get():
        if e.type == QUIT:
            quit()

    window.blit(bg, (0,0))
    player.update()
    player.draw(window)
    display.update()
    clock.tick(FPS)