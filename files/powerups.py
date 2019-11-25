__author__ = "Joshua Akangah"
import pygame
import math 
import random

powerupImages = [
    # bolt
    pygame.image.load("../assets/Power-ups/bolt_silver.png"),
    pygame.image.load("../assets/Power-ups/bolt_gold.png"),
    # pills
    pygame.image.load("../assets/Power-ups/pill_red.png"),
    pygame.image.load("../assets/Power-ups/pill_yellow.png"),
    pygame.image.load("../assets/Power-ups/pill_green.png"),
    # shield
    pygame.image.load("../assets/Power-ups/shield_gold.png"),
    # star credits
    pygame.image.load("../assets/Power-ups/star_bronze.png"),
    pygame.image.load("../assets/Power-ups/star_gold.png"),
    pygame.image.load("../assets/Power-ups/star_gold.png"),

]

class Shield(pygame.sprite.Sprite):
    def __init__(self, player): 
        pygame.sprite.Sprite.__init__(self)
        self.shieldImage3 = pygame.image.load("../assets/Effects/shield1.png")
        self.shieldImage2 = pygame.image.load("../assets/Effects/shield2.png")
        self.shieldImage1 = pygame.image.load("../assets/Effects/shield3.png")
        self.image = self.shieldImage1
        # self.x = player.pos.x+player.rect.width/2-self.shieldImage.get_rect().width/2
        # self.y = player.pos.y-self.shieldImage.get_rect().height/4
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.player = player

    def update(self):
        self.rect.x, self.rect.y = self.player.pos.x+self.player.rect.width/2-self.rect.width/2, self.player.pos.y-self.rect.height/4
        self.mask = pygame.mask.from_surface(self.image)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, typeOf, spawnX, spawnY):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            pygame.image.load("../assets/Lasers/laserBlue01.png"),
            pygame.transform.flip(pygame.image.load("../assets/Lasers/laserRed01.png"), False, True),
            pygame.transform.scale(pygame.image.load("../assets/Lasers/laserBlue10.png"), (15, 15)),
            pygame.transform.scale(pygame.image.load("../assets/Lasers/laserRed10.png"), (15,15))
        ]
        self.type = typeOf
        if self.type == 1:
            self.image = self.images[0]
        else:
            self.image = self.images[1]
        self.speed = 15
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(spawnX, spawnY)
        self.bType = "Bullet"
        self.delayTime = 0

    def update(self, display, player=None):
        # self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos.x, self.pos.y

        if self.images.index(self.image) in (2, 3):
            self.delayTime += 1
            if self.delayTime >= 10:
                self.kill()

        else:
            if self.type == 1:
                self.pos.y -= self.speed
                if self.pos.y + self.rect.height < 0:
                    self.kill()
            else:
                self.pos.y += self.speed
                if self.pos.y > 600:
                    self.kill()+self.rect.height