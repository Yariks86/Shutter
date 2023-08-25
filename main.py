from pygame import *
from random import randint
import time as tajm
init()

W = 880
H = 1050

window = display.set_mode((W, H))#Створення вікна
display.set_caption("Shutter")
display.set_icon(image.load('ahz8ip50iaw21.jpg'))

back = transform.scale(image.load('ahz8ip50iaw21.jpg'), (W, H))
#clock = time.Clock()#лічильник кадрів

not_exploded = 0

exploded = 0

mixer.init()#підключати звуки
mixer.music.load('X2.mp3')
mixer.music.set_volume(0.4)
mixer.music.play()
fire_snd = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('None', 50)
font2 = font.SysFont('None', 50)

# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        super().__init__()
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    # метод, що малює героя у вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        # global player_rect
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed

        if keys_pressed[K_d] and self.rect.x < W-140:
            self.rect.x += self.speed
        # player_rect = self.rect.x + 50

    def fire(self):
        
        bullet1 = Bullet('arab.jpg', self.rect.x + 50, 800, 40, 40, 5)
        bullets.add(bullet1)
        # keys_pressed = key.get_pressed()

        # if keys_pressed[K_SPACE]:
            
            # bullet1.rect.x = player_rect
            # bullet1.rect.y = self.rect.y
            # print(player_rect)
            # bullet1.reset()
            # bullet1.update()

class Enemy(GameSprite):
    def update(self):
        global not_exploded
        if self.rect.y >= 1000:
            self.rect.y = -200
            self.rect.x = randint(0, 780)
            not_exploded += 1
        self.rect.y += self.speed

class pendosi(Enemy):
    def update(self):
        if self.rect.y >= 1000:
            self.rect.y = randint(-1000, -500)
            self.rect.x = randint(0, 680)
        self.rect.y += self.speed




class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


a = 3



hero = Player('media.png', 370, 800, 120, 200, 7)
bullets = sprite.Group()


skyscraper = sprite.Group()
for i in range(6):
    enemy1 = Enemy('kisspng.png', randint(0, 680), randint(-500, 0), 100, 100, randint(2, 5))
    skyscraper.add(enemy1)

pendosis = sprite.Group()
for i in range(2):
    pendosis1 = pendosi('cartoon.png', randint(0, 680), randint(-1500, -750), 100, 100, randint(5, 7))
    pendosis.add(pendosis1)


number1 = GameSprite('free1.png', -200, 100, 200, 200, 0)
number3 = GameSprite('free3.png', 0, 100, 200, 200, 0)
number2 = GameSprite('free2.png', -200, 100, 200, 200, 0)

i = 0
game = True
finish = False
num_fire = 0
rel_time = False
while game:
    time.delay(10)
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 10 and rel_time is False:
                    num_fire += 1
                    hero.fire()
                    fire_snd.play()
                if num_fire > 10 and rel_time is False:
                    rel_time = True
                    last_time = tajm.time()

    if not finish:
        window.blit(back, (0, 0))
        hero.reset()
        hero.update()
        # enemy1.reset()
        # enemy1.update()
        skyscraper.draw(window)
        skyscraper.update()
        pendosis.draw(window)
        pendosis.update()
        number1.reset()
        number2.reset()
        number3.reset()
        bullets.draw(window)
        bullets.update()

        if rel_time:
            new_time = tajm.time()
            if new_time - last_time < 2.5:
                reload_txt = font1.render('Намаз!!!', True, (100, 255, 255))
                window.blit(reload_txt, (W/2-70, H/2))
            else:
                rel_time = False
                num_fire = 0

        not_exploded_txt = font1.render('Not exploded: ' + str(not_exploded), 1, (200, 50, 50))
        window.blit(not_exploded_txt, (10, 10))
        exploded_txt = font2.render('Exploded: ' + str(exploded), 1, (50, 200, 50))
        window.blit(exploded_txt, (10, 50))

        if sprite.spritecollide(hero, skyscraper, True):
            a -= 1
            enemy1 = Enemy('kisspng.png', randint(0, 680), -200, 100, 100, randint(2, 4))
            skyscraper.add(enemy1)

        if sprite.spritecollide(hero, pendosis, True):
            a -= 1
            pendosis1 = Enemy('cartoon.png', randint(0, 680), randint(-1500, -750), 100, 100, randint(5, 7))
            pendosis.add(pendosis1)

        sprite.groupcollide(bullets, pendosis, True, False)

        collides = sprite.groupcollide(bullets, skyscraper, True, True)
        for col in collides:
            exploded +=1
            enemy1 = Enemy('kisspng.png', randint(0, 680), -200, 100, 100, randint(2, 4))
            skyscraper.add(enemy1)  


        if exploded >= 101:
            win = font2.render('Халяль!!!', True, (0, 255, 0))
            window.blit(win, (W/2-150, H/2))
            finish = True

        if a <= 0 or not_exploded >= 10:
            lose = font2.render('Харам!!!', True, (0, 255, 0))
            window.blit(lose, (W/2-50, H/2))
            finish = True
        
        if a == 3:
            number1.rect.x = -200
            number3.rect.x = 0
        if a == 2:
            number3.rect.x = -200
            number2.rect.x = 0
        if a == 1:
            number2.rect.x = -200
            number1.rect.x = 0
    


    keys_pressed1 = key.get_pressed()
    if keys_pressed1[K_r]:
        a = 3
        exploded = 0
        not_exploded = 0

        for m in skyscraper:
            m.kill()

        for b in bullets:
            b.kill()
        
        for k in pendosis:
            k.kill()

        for i in range(8):
            enemy1 = Enemy('kisspng.png', randint(0, 680), randint(-500, 0), 100, 100, randint(2, 5))
            skyscraper.add(enemy1)
        for i in range(2):
            pendosis1 = pendosi('cartoon.png', randint(0, 680), randint(-1500, -750), 100, 100, randint(5, 7))
            pendosis.add(pendosis1)
        finish = False
        print('r')
        

    display.update()


