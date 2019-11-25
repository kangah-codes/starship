"""
Player script
"""
import pygame
import math
import random
from powerups import *

__author__ = "Joshua Akangah"

playerImages = [
    # type 1
    pygame.image.load("../assets/Player/playerShip1_blue.png"),
    pygame.image.load("../assets/Player/playerShip1_orange.png"),
    pygame.image.load("../assets/Player/playerShip1_green.png"),
    pygame.image.load("../assets/Player/playerShip1_red.png"),
    # type 2
    pygame.image.load("../assets/Player/playerShip2_blue.png"),
    pygame.image.load("../assets/Player/playerShip2_orange.png"),
    pygame.image.load("../assets/Player/playerShip2_green.png"),
    pygame.image.load("../assets/Player/playerShip2_red.png"),
    # type 3
    pygame.image.load("../assets/Player/playerShip3_blue.png"),
    pygame.image.load("../assets/Player/playerShip3_orange.png"),
    pygame.image.load("../assets/Player/playerShip3_green.png"),
    pygame.image.load("../assets/Player/playerShip3_red.png"),
    # damage images
    # player 1 damage
    pygame.image.load("../assets/Damage/playerShip1_damage1.png"),
    pygame.image.load("../assets/Damage/playerShip1_damage2.png"),
    pygame.image.load("../assets/Damage/playerShip1_damage3.png"),
    # player 2 damage
    pygame.image.load("../assets/Damage/playerShip2_damage1.png"),
    pygame.image.load("../assets/Damage/playerShip2_damage2.png"),
    pygame.image.load("../assets/Damage/playerShip2_damage3.png"),
    # player 3 damage
    pygame.image.load("../assets/Damage/playerShip3_damage1.png"),
    pygame.image.load("../assets/Damage/playerShip3_damage2.png"),
    pygame.image.load("../assets/Damage/playerShip3_damage3.png"),
    # fire image
    pygame.image.load("../assets/Effects/fire16.png"),
    # gun
    [
        pygame.image.load("../assets/Ship_Guns/gun00.png"),
        pygame.image.load("../assets/Ship_Guns/gun05.png"),
        pygame.image.load("../assets/Ship_Guns/gun08.png"),
        pygame.image.load("../assets/Ship_Guns/gun09.png"),
    ]
]


class Player(pygame.sprite.Sprite):
    def __init__(self, typeOf, variation):
        """
        param type: The type of ship going to be used by player
        param variation: The color of the ship. Each type has 4 color variations
        variation should be from 1-3
        """
        pygame.sprite.Sprite.__init__(self)
        self.type = typeOf
        self.variation = variation
        if self.type == 1:
            self.damageImage1 = playerImages[12]
            self.damageImage2 = playerImages[13]
            self.damageImage3 = playerImages[14]
            self.life = 5
            self.bullets = 10
            if self.variation == 1:
                self.image = playerImages[0]
            elif self.variation == 2:
                self.image = playerImages[1]
            elif self.variation == 3:
                self.image = playerImages[2]
            else:
                self.image = playerImages[3]
        elif self.type == 2:
            self.damageImage1 = playerImages[15]
            self.damageImage2 = playerImages[16]
            self.damageImage3 = playerImages[17]
            self.life = 8
            self.bullets = 15
            if self.variation == 1:
                self.image = playerImages[4]
            elif self.variation == 2:
                self.image = playerImages[5]
            elif self.variation == 3:
                self.image = playerImages[6]
            else:
                self.image = playerImages[7]
        else:
            self.damageImage1 = playerImages[18]
            self.damageImage2 = playerImages[19]
            self.damageImage3 = playerImages[20]
            self.life = 10
            self.bullets = 25
            if self.variation == 1:
                self.image = playerImages[8]
            elif self.variation == 2:
                self.image = playerImages[9]
            elif self.variation == 3:
                self.image = playerImages[10]
            else:
                self.image = playerImages[11]
        # shield
        self.shieldTimer = 0
        self.shield = False
        self.shields = 1
        self.pos = pygame.math.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5
        self.damageLevel = 0
        self.fire = playerImages[21]
        self.fire_rect = self.fire.get_rect()
        self.delay = 0
        self.missiles = 0
        self.score = 0
        self.tempShield = Shield(self)
        shieldGroup.add(self.tempShield)

    def move(self):
        keyPress = pygame.key.get_pressed()
        mousePress = pygame.mouse.get_pressed()

        if keyPress[pygame.K_a]:
            self.pos.x -= self.speed

        if keyPress[pygame.K_d]:
            self.pos.x += self.speed

        if mousePress[0]:
            self.delay += 1
            if self.delay >= 5:
                if self.type == 1:
                    bulletGroup.add(Bullet(1, self.pos.x+self.rect.width/2 - 4.5, self.pos.y))
                elif self.type == 2:
                    bulletGroup.add(Bullet(1, self.pos.x+18, self.pos.y-10))
                    bulletGroup.add(Bullet(1, self.pos.x+self.rect.width-27, self.pos.y-10))
                elif self.type == 3:
                    bulletGroup.add(Bullet(1, self.pos.x+21, self.pos.y))
                    bulletGroup.add(Bullet(1, self.pos.x+self.rect.width/2 - 4.5, self.pos.y-27))
                    bulletGroup.add(Bullet(1, self.pos.x+self.rect.width-30, self.pos.y))
                self.delay = 0

    def update(self):
        self.pos = pygame.math.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        """ bug """
        #self.rect.midbottom = self.pos
        self.rect.x, self.rect.y = self.pos.x, self.pos.y
        shieldGroup.update()

        for powerup in powerupGroup:
            if pygame.sprite.collide_mask(self, powerup):
                if powerup.type == "bolt":
                    self.missiles += powerup.effect
                elif powerup.type == "pill":
                    self.life += powerup.effect
                elif powerup.type == "shield":
                    self.shields += 1
                else:
                    self.score += powerup.effect
                powerup.kill()

        for missile in enemybulletGroup:
            if not self.shield:
                if missile.type not in (1, 3):
                    if pygame.sprite.collide_mask(self, missile):
                        if missile.type == 4:
                            self.life -= missile.damage
                            missile.image = missile.smoke_image
                        else:
                            self.life -= 1
                            missile.image = missile.smoke_image
            else:
                pygame.sprite.groupcollide(shieldGroup, enemybulletGroup, False, True)

    def draw(self, display):
        if self.type == 1:
            display.blit(pygame.transform.flip(playerImages[22][0], False, True), ((self.pos.x+self.rect.width/2)-(playerImages[22][0].get_rect().width/2), self.pos.y - playerImages[22][0].get_rect().height/2))
            display.blit(self.fire, ((self.pos.x+self.rect.width/2) - self.fire_rect.width/2, self.pos.y + self.rect.height))

        elif self.type == 2:
            display.blit(pygame.transform.flip(playerImages[22][1], False, True), (self.pos.x+self.rect.width/6, self.pos.y+5))
            display.blit(pygame.transform.flip(playerImages[22][1], True, True), (self.pos.x+self.rect.width/1.5, self.pos.y+5))
            display.blit(self.fire, ((self.pos.x+self.rect.width/4) - self.fire_rect.width/2, self.pos.y + self.rect.height - 5))
            display.blit(self.fire, ((self.pos.x+self.rect.width) - self.fire_rect.width*2.6, self.pos.y + self.rect.height - 5))

        else:
            display.blit(pygame.transform.flip(playerImages[22][3], False, True), (self.pos.x+self.rect.width/8, self.pos.y+5))
            display.blit(pygame.transform.flip(playerImages[22][2], False, True), ((self.pos.x+self.rect.width/2)-(playerImages[22][2].get_rect().width/2), self.pos.y - playerImages[22][2].get_rect().height/2))
            display.blit(pygame.transform.flip(playerImages[22][3], True, True), (self.pos.x+self.rect.width/1.5, self.pos.y+5))
            display.blit(self.fire, ((self.pos.x+self.rect.width/5) - self.fire_rect.width/2, self.pos.y + self.rect.height - 10))
            display.blit(self.fire, ((self.pos.x+self.rect.width) - self.fire_rect.width*1.8, self.pos.y + self.rect.height - 10))

        # draw the player before damage images
        display.blit(self.image, self.pos)

        if self.damageLevel == 1:
            display.blit(self.damageImage1, self.pos)
        elif self.damageLevel == 2:
            display.blit(self.damageImage2, self.pos)
        elif self.damageLevel == 3:
            display.blit(self.damageImage3, self.pos)

        if self.shield:

            self.shieldTimer += 1

            if self.shieldTimer >= 0 and self.shieldTimer < 360:
                self.tempShield.shieldImage = self.tempShield.shieldImage1
            elif self.shieldTimer >= 360 and self.shieldTimer < 720:
                self.tempShield.shieldImage = self.tempShield.shieldImage2
            elif self.shieldTimer >= 720:
                self.tempShield.shieldImage = self.tempShield.shieldImage3

            #display.blit(self.tempShield.image, (self.pos.x+self.rect.width/2-self.tempShield.rect.width/2, self.pos.y-self.tempShield.rect.height/4))
            shieldGroup.draw(display)
            if self.shieldTimer >= 360*3:
                self.shieldTimer = 0
                self.shield = False
