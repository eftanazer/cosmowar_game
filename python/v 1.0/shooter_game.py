from pygame import *
from random import randint
from time import time as timer
#подгружаем отдельно функции для работы со шрифтом
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))


font2 = font.Font(None, 36)


#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


#нам нужны такие картинки:
img_back = "galaxy.jpg" #фон игры
img_bullet = "bullet.png" #пуля
img_hero = "rocket.png" #герой
img_ast = "asteroid.png"
img_enemy = "ufo.png" #враг
score = 0 #сбито кораблей
life = 3
goal = 22 #столько кораблей нужно сбить для победы
lost = 0 #пропущено кораблей
max_lost = 5 #проиграли, если пропустили столько
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)


       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed


       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))


#класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
   def update(self):
       keys = key.get_pressed()
       if keys[K_a] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_d] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)


#класс спрайта-врага  
class Enemy(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       global lost
       #исчезает, если дойдёт до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1

class Aster(GameSprite):
   def update(self):
       self.rect.y += self.speed
       #исчезает, если дойдёт до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0

#класс спрайта-пули  
class Bullet(GameSprite):
   # движение врага
   def update(self):
       self.rect.y += self.speed
       # исчезает, если дойдет до края экрана
       if self.rect.y < 0:
           self.kill()
#создаём окошко
win_width = 700
win_height = 500
clocker = time.Clock()
display.set_caption(str(clocker.get_fps()))
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
#создаём спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 20)
#создание группы спрайтов-врагов
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Aster(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 9))
    asteroids.add(asteroid)

#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
rel = False
fire_num = 0
finish = False
#основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
while run:
   clocker.tick()
   #событие нажатия на кнопку Закрыть
   for e in event.get():
       if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
           run = False
       #событие нажатия на пробел - спрайт стреляет
       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               if fire_num < 7 and rel == False:
                   fire_num += 1
                   fire_sound.play()
                   ship.fire()
               if fire_num >= 7 and rel == False:
                   last = timer()
                   rel = True
 #сама игра: действия спрайтов, проверка правил игры, перерисовка
   if not finish:
       #обновляем фон
       window.blit(background,(0,0))

       #производим движения спрайтов
       ship.update()
       monsters.update()
       bullets.update()
       asteroids.update()


       #обновляем их в новом местоположении при каждой итерации цикла
       ship.reset()
       monsters.draw(window)
       bullets.draw(window)
       asteroids.draw(window)

       #перезарядка
       if rel == True:
           now = timer()
           if now - last < 2:
               reloader = font2.render('охладите своё ********', True, (255, 0, 0))
               window.blit(reloader, (250, 450))
           else:
               fire_num = 0
               rel = False
       #проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
       collides = sprite.groupcollide(monsters, bullets, True, True)
       for c in collides:
           #этот цикл повторится столько раз, сколько монстров подбито
           score = score + 1
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)


       #возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
       if sprite.spritecollide(ship, asteroids, False):
           sprite.spritecollide(ship, asteroids, True)
           life -=1

       if life == 0 or max_lost <= lost or  sprite.spritecollide(ship, monsters, False):
           finish = True #проиграли, ставим фон и больше не управляем спрайтами.
           window.blit(lose, (200, 200))


       #проверка выигрыша: сколько очков набрали?
       if score >= goal:
           finish = True
           window.blit(win, (200, 200))


       #пишем текст на экране
       text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))


       text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 50))

       if life == 3:
          life_color = (0, 200, 0)
       if life == 2:
           life_color = (0, 0, 200)
       if life == 1:
           life_color = (200, 0, 0)
       text_life = font1.render(str(life), 1, life_color)
       window.blit(text_life, (650, 20))

       display.update()
   #бонус: автоматический перезапуск игры
   else:
       finish = False
       score = 0
       lost = 0
       life = 3
       fire_num = 0
       rel = False
       for b in bullets:
           b.kill()
       for m in monsters:
           m.kill()
       for a in asteroids:
           a.kill()


       time.delay(3000)
       for i in range(1, 6):
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)
       for i in range(1, 3):
           asteroid = Aster(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 9))
           asteroids.add(asteroid)
      


   time.delay(50)
