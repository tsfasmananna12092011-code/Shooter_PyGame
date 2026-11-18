from pygame import *
import random
from time import time as timer

width = 700
height = 500
window = display.set_mode((width, height))
background = transform.scale(image.load('pictures/galaxy.jpg'),(width, height))

clock = time.Clock()
FPS = 50

missed = 0
score = 0
num_fire = 0
rel_time = False

font.init()
font1 = font.Font(None, 40)




class GameSprite(sprite.Sprite):
    def __init__(self, filename, x, y, speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(filename),(width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def appear(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# ПЕРЕМЕЩЕНИЕ
class Player(GameSprite): 
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
        #if keys[K_SPACE]:
            #self.fire()
    
    def fire(self):
        bullet = Bullet('pictures/bullet.png', self.rect.centerx, self.rect.top, 10, 15,15)
        bullet2 = Bullet('pictures/bullet.png', self.rect.right, self.rect.bottom, 10, 15,15)
        bullet3 = Bullet('pictures/bullet.png', self.rect.left, self.rect.bottom, 10, 15,15)
        bullets.add(bullet)
        bullets.add(bullet2)
        bullets.add(bullet3)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()


class Asteroid(GameSprite):
    def update(self):
            self.rect.y += self.speed
            global missed
            






class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y > height:
            self.rect.x = random.randint(80, width-80)
            self.rect.y = -70
            missed = missed + 1
            print(missed)
            self.speed =  random.randint(2,6 )
        
        
        

asteroids = sprite.Group()
monsters = sprite.Group()



rocket = Player('pictures/rocket.png', width//2-80, height-90, 20, 90, 80)     
for i in range(4):
    number = random.randint(80, width-80)
    speedex = random.randint(1,4)
    new_x = number
    alien = Enemy('pictures/ufo.png', new_x ,0, speedex, 70,70)
    monsters.add(alien)

asteroid1 = Asteroid('pictures/asteroid.png', 150, -150, 5, 250, 250 )
asteroids.add(asteroid1)





game = True
finish = False
while game:

    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if rel_time == False and num_fire <= 15:
                    rocket.fire()
                    num_fire += 1  

                if rel_time == False and num_fire > 15:
                    last_time = timer()
                    rel_time = True
        if e.type == QUIT:
            game = False
   
   
    window.blit(background,(0,0))
    rocket.appear()
    monsters.draw(window)
    bullets.draw(window)
    missed_text = font1.render(f'ПРОПУЩЕНО: {missed}',True, (255,255,255))
    score_text = font1.render(f'СЧЁТ: {score}',True, (255,255,255))
    fire_text = font1.render(f'ВЫСТРЕЛЫ: {num_fire}',True, (255,255,255))
    window.blit(missed_text,(20,20))
    window.blit(score_text,(20,50))
    window.blit(fire_text,(20,80))
    if not finish:
        rocket.update()
        monsters.update()
        bullets.update()
        #display.update()

        if rel_time == True:
            new_time = timer()
            if (new_time - last_time) < 3:
                stop_text = font1.render(f'ВЫСТРЕЛЫ ОРГАНИЧЕНЫ',True, (255,255,255))
                window.blit(stop_text,(20,100))
            else:
                rel_time = False
                num_fire = 0


        if score >= 20:
            score1_text = font1.render('ПОБЕДА!',True, (255,255,255))
            window.blit(score1_text,(200,200))
            display.update()
            finish = True
       
        if missed >= 5 or sprite.spritecollide(rocket, monsters, True):
            missed1_text = font1.render('ВЫ ПРОИГРАЛИ :(',True, (255,255,255))
            window.blit(missed1_text,(150,200))
            display.update()
            finish = True

        if score >= 10:
            #asteroid1 = Asteroid('pictures/asteroid.png', 150, 0, 4, 150, 150 )
            asteroids.draw(window)
            asteroids.update()
            if sprite.spritecollide(rocket, asteroids, True):
                finish = True
            #if finish == True:
                missed1_text = font1.render('ВЫ ПРОИГРАЛИ :(',True, (255,255,255))
                window.blit(missed1_text,(150,200))
                display.update()
           
        


        
        
        collid = sprite.groupcollide(bullets, monsters,True, True) 
        for i in collid:
            score += 1
            number = random.randint(80, width-80)
            new_x = number
            alien = Enemy('pictures/ufo.png', new_x ,0, 3, 70,70)
            monsters.add(alien)

    
            
    
    




    display.update()
    clock.tick(FPS)











