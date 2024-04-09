from pygame import * 
from random import randint
font.init()
font1 = font.SysFont('Arial', 36)

font2 = font.SysFont("Arial", 80)
lost = 0
score = 0
win = font2.render('YOU WIN!', True, (255, 0, 255))
lose = font2.render('YOU LOSE!', True, (180, 0, 0))
mixer.init()
mixer.music.load("C:/Users/hudacin/AppData/Local/Programs/Algoritmika/vscode/data/extensions/algoritmika.algopython-20220124.142703.0/temp/shooter/space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("C:/Users/hudacin/AppData/Local/Programs/Algoritmika/vscode/data/extensions/algoritmika.algopython-20220124.142703.0/temp/shooter/fire.ogg")
class GameSprite(sprite.Sprite):
    # class constructor
    def __init__(self, player_image, player_x, player_y,size_x, size_y, player_speed):
        super().__init__()
        # every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        # every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
                bullet = Bullet("C:/Users/hudacin/AppData/Local/Programs/Algoritmika/vscode/data/extensions/algoritmika.algopython-20220124.142703.0/temp/shooter/bullet.png",self.rect.centerx, self.rect.top, 30, 30, 15)
                bullets.add(bullet)
                fire_sound.play() 



class Enemy(GameSprite):    
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_height -80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

FPS = 60
win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption("Shooter")
clock = time.Clock()
background = transform.scale(image.load("C:/Users/hudacin/AppData/Local/Programs/Algoritmika/vscode/data/extensions/algoritmika.algopython-20220124.142703.0/temp/shooter/galaxy.jpg"),(win_width,win_height))
player = Player("C:/Users/hudacin/AppData/Local/Programs/Algoritmika/vscode/data/extensions/algoritmika.algopython-20220124.142703.0/temp/shooter/player.png", 5, win_height - 100, 70, 80, 5)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy("C:/Users/hudacin/AppData/Local/Programs/Algoritmika/vscode/data/extensions/algoritmika.algopython-20220124.142703.0/temp/shooter/enemy.png", randint(80, win_width - 80), -40, 60, 70, randint(1, 5))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(1,4):
    asteroid = Enemy("C:/Users/hudacin/AppData/Local/Programs/Algoritmika/vscode/data/extensions/algoritmika.algopython-20220124.142703.0/temp/shooter/asteroid.png",randint(80, win_width - 80), -40, 60, 70, randint(1, 5))
    asteroids.add(asteroid)
bullets = sprite.Group()
lives = 4
finish = False
game = True
end = win
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False   

        if e.type == KEYDOWN and e.key == K_SPACE:
            player.fire()
    window.blit(background,(0,0))
    text_score = font1.render("Score: " + str(score), True, (255, 255, 255))
    window.blit(text_score, (10, 20))
    lives_text = font1.render("Životy: " + str(lives), True, (155,0,155))
    window.blit(lives_text, (10, 80))
    text_lose = font1.render("Missed: " + str(lost), True, (255, 255, 255))
    window.blit(text_lose, (10, 50))        
    if not finish:

        
        collides = sprite.groupcollide(monsters,bullets, False,True)
        for c in collides:
            score += 1
            c.rect.x = randint(80,win_width - 80)
            c.rect.y = 0
            c.speed = randint(1,3)

        if sprite.spritecollide(player,monsters,True) or lost >= 10:
            lost = 0
            lives -= 1
        
        if sprite.spritecollide(player,asteroids,True):
            lives -= 1

        if lives == 0:
            finish = True
            end = lose
        
        #win checking: how many points scored?
        if score >= 10:
            finish = True
            end = win
       
        asteroids.draw(window)
        asteroids.update()
        player.update()
        player.reset()
        bullets.draw(window)
        bullets.update()
        monsters.draw(window)
        monsters.update()
        #for monster in monsters:
        #    monster.update()
        #    monster.reset()
    else:
        window.blit(end, (200, 200))

    display.update()
    clock.tick(FPS)