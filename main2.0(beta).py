#GhostProject
#A multiplayer arcade shooter.

#
#   Copyright (C) 2010 Oliver Alves, Victor Peres, Vitor Paladini 
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


# -*- coding: utf-8 -*-

#import
import os, sys
import pygame
from pygame import *
from pygame import mixer
import spritesheet
import random
from SS import SpriteStripAnim

os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()
screen = pygame.display.set_mode((800,600))
gamestate = 1
escpressed = False

#options
def option1():
    global gamestate
    gamestate = 2
def option2():
    global gamestate
    gamestate = 0

class Button(pygame.sprite.Sprite):
    def __init__(self, image, coord, index):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = coord[0] - self.rect.width / 2; self.rect.y = coord[1] + (self.rect.height * index)

    def draw(self):
        screen.blit(self.image, self.rect)


class Menu():
    def __init__(self, bg,  *items):
        self.x = screen.get_width() /2; self.y = screen.get_height()/2
        self.items = items
        self.clock = pygame.time.Clock()
        self.buttons = []
        self.bg = pygame.image.load(bg)
        for i in self.items:
            self.buttons.append(Button("images/" + i[0] + ".png", (self.x, self.y), self.items.index(i)))
        pygame.mouse.set_visible(True)

    def update(self, fps):
        global gamestate
        global escpressed
        while gamestate == 1:
            self.clock.tick(fps)
            pygame.event.pump()
            kb = pygame.key.get_pressed()
            if kb[pygame.K_ESCAPE] and not escpressed:
                gamestate = 0
                break
            if not kb[pygame.K_ESCAPE]:
                escpressed = False
            
            mouse_rect = Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1,1)
            
            for b in self.buttons:
                if pygame.mouse.get_pressed()[0] == 1:
                    if b.rect.colliderect(mouse_rect):
                        self.items[self.buttons.index(b)][1]()

            self.draw()

    def draw(self):
        screen.fill((255,255,255))
        screen.blit(self.bg, self.bg.get_rect())
        for b in self.buttons:
            b.draw()
        pygame.display.flip()
    
class Mine(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pygame.image.load("images/mine.gif").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x; self.rect.y = y

    def draw(self):
        screen.blit(self.image, self.rect)

class PowerUp(pygame.sprite.Sprite):
    
    def __init__(self, image="images/healthPack.gif"):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = (random.randint(1,800) - self.rect.width) ; self.rect.y = (random.randint(1,600) - self.rect.height)
        self.gotPowerUp = False
    def draw(self):
        if self.gotPowerUp == False:
            screen.blit(self.image, self.rect)

class Background(pygame.sprite.Sprite):

    def __init__( self, image="images/BGHOME.png"):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()

    def draw(self):
        screen.blit(self.image, self.rect)
        
class Ghost(pygame.sprite.Sprite):
    
    def __init__(self,x,y,file):
        self.strip = SpriteStripAnim(file, (0,0,50,80), 8, (0,0,0),   True, 2)
        self.image = self.strip.images[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y
        self.alive = True
        self.flip = False
        self.hp = 200

    def move(self,dx,dy):
        self.rect.move_ip(dx, dy)
    
    def keepInBounds(self):
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + self.rect.width > screen.get_width():
            self.rect.x = screen.get_width() - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y + self.rect.height > screen.get_height():
            self.rect.y = screen.get_height() - self.rect.height
    
    def draw(self):
        screen.blit(self.image, self.rect)

class Shoot(pygame.sprite.Sprite):

    def __init__(self,x,y, flip):
        self.image = pygame.image.load("images/shoot.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y
        self.flip = flip

    def move(self,sx,sy):
        if self.flip:
            self.rect.move_ip(-sx, sy)
        else:
            self.rect.move_ip(sx, sy)


class Game:

    def __init__(self):        
        #ghosts!
        self.ghost = Ghost(20,80, 'images/ssGhostM.gif')

        self.ghostV = Ghost(20,300, 'images/ssGhostV.gif')
        
        self.bg = Background()
        self.powerup = PowerUp()
        
        #sounds
        pygame.mixer.music.load('sounds/bgm1.mp3')
        pygame.mixer.music.play(-1,0.0)
        self.sfx2 = pygame.mixer.Sound('sounds/shoot.wav')
        self.boom = pygame.mixer.Sound('sounds/boom.wav')
        self.boom.set_volume(1.0)
        
        self.shots = []
        self.hasShot = True
        
        self.shots2 = []
        self.hasShot2 = True

        self.mines = []
        self.maxMines = 3
        self.hasMined = True

        self.mines2 = []
        self.maxMines2 = 3
        self.hasMined2 = True
        
        self.shoot1 = pygame.image.load('images/shoot.png').convert_alpha()
        self.shoot2 = pygame.image.load('images/shootV.png').convert_alpha()
        self.count = 0
        self.count2 = 0
        
        #joystick
        if pygame.joystick.get_count() > 0:
            self.joy = pygame.joystick.Joystick(0)
            self.joy.init()
            self.axis = [0,0]
            self.hasJoy = True
        else:
            self.hasJoy = False

    def update(self, fps):
        self.clock = pygame.time.Clock()

        self.ghost.strip.iter()
        self.ghostV.strip.iter()

        self.ghost.image = self.ghost.strip.next()
        self.ghostV.image = self.ghostV.strip.next()
        global gamestate
        global escpressed
        while gamestate == 2:
            self.clock.tick(fps)
            pygame.event.pump()
            kb = pygame.key.get_pressed()
            self.count += 1
            if self.count > 200:
                self.powerup.gotPowerUp = False
                self.powerup.rect.x = (random.randint(1,800 - self.powerup.rect.width)) ; self.powerup.rect.y = (random.randint(1,600 - self.powerup.rect.height))
                self.count = 0

            #exit game
            if kb[pygame.K_ESCAPE]:
                gamestate = 1
                escpressed = True
                break
            #reset game after ghost death
            if self.ghostV.hp <= 0:
                self.clock.tick(fps)
                self.count2 += 1
                if self.count2 > 0:
                    gamestate = 1
                    escpressed = True
                    break
            if self.ghost.hp <= 0:
                self.clock.tick(fps)
                self.count2 += 1
                if self.count2 > 60:
                    gamestate = 1
                    escpressed = True
                    break
            
            if self.ghostV.alive:
                if self.hasJoy:
                    #flip the image of ghostV
                    self.axis[0] = round(self.joy.get_axis(0) * 10) #x axis
                    self.axis[1] = round(self.joy.get_axis(1) * 10) #y axis
                    if self.axis[0] > 0 and self.ghostV.flip == True:
                        self.ghostV.flip = False
                    if self.axis[0] < 0 and self.ghostV.flip == False:
                        self.ghostV.flip = True

                    #move ghostV with joypad
                    self.ghostV.rect.move_ip(self.axis[0], self.axis[1])
                    if self.joy.get_button(2):
                        if self.hasShot2:
                            self.shots2.append(Shoot(self.ghostV.rect.x + self.ghostV.rect.width /2, self.ghostV.rect.y + (self.ghostV.rect.height / 2), self.ghostV.flip))
                            self.hasShot2 = False
                            self.sfx2.play()
                    else:
                        self.hasShot2 = True
                    if self.joy.get_button(3):
                        if len(self.mines2) < 3 and self.hasMined2:
                            self.mines2.append(Mine(self.ghostV.rect.x - 30, self.ghostV.rect.y))
                            self.hasMined2 = False
                    else:
                        self.hasMined2 = True  
                else:
                    self.inputPlayer2(kb)

                self.ghostV.keepInBounds()

            if self.ghost.alive:
                self.inputPlayer(kb)

            #update shots
            for s in self.shots:
                s.move(20,0)
                if s.rect.x  + s.rect.width < 0 or s.rect.x > screen.get_width():
                    self.shots.remove(s)
                if self.ghostV.alive:
                    if s.rect.colliderect(self.ghostV.rect):
                        self.ghostV.hp -= 10
                        self.shots.remove(s)
                        continue
               
                        
            
            for s in self.shots2:
                s.move(20,0)
                if s.rect.x  + s.rect.width < 0 or s.rect.x > screen.get_width():
                    self.shots2.remove(s)
                if self.ghost.alive:
                    if s.rect.colliderect(self.ghost.rect):
                        self.ghost.hp -= 10
                        self.shots2.remove(s)
                        continue
              
                        

            for m in self.mines:
                if m.rect.colliderect(self.ghostV.rect):
                    self.mines.remove(m)
                    self.ghostV.hp -= 30
                if m.rect.colliderect(self.ghost.rect):
                    self.mines.remove(m)
                    self.ghost.hp -= 30

            for m in self.mines2:
                if m.rect.colliderect(self.ghostV.rect):
                    self.mines2.remove(m)
                    self.ghostV.hp -= 30
                if m.rect.colliderect(self.ghost.rect):
                    self.mines2.remove(m)
                    self.ghost.hp -= 30
            if self.ghost.alive == True:
                if self.ghost.hp <= 0:
                    self.ghost.alive = False
                    self.boom.play()
            if self.ghostV.alive == True:
                if self.ghostV.hp <= 0:
                    self.ghostV.alive = False
                    self.boom.play()
            
            self.draw()
    
    def inputPlayer(self, keyb):
        if self.ghost.rect.y > 0:
            if keyb[pygame.K_UP]:
                self.ghost.move(0,-10)
        if self.ghost.rect.y + self.ghost.rect.height < screen.get_height():
            if keyb[pygame.K_DOWN]:
                self.ghost.move(0,10)
        if self.ghost.rect.x > 0:
            if keyb[pygame.K_LEFT]:
                self.ghost.flip = True
                self.ghost.move(-10,0)
        if self.ghost.rect.x + self.ghost.rect.width < screen.get_width():
            if keyb[pygame.K_RIGHT]:
                self.ghost.flip = False
                self.ghost.move(10,0)
        if keyb[pygame.K_RCTRL] and self.hasShot:
            self.shots.append(Shoot(self.ghost.rect.x + self.ghost.rect.width /2, self.ghost.rect.y + (self.ghost.rect.height / 2), self.ghost.flip))
            self.hasShot = False
            self.sfx2.play()
        if not keyb[pygame.K_RCTRL]:
            self.hasShot = True
        if keyb[pygame.K_RSHIFT]:
            if len(self.mines) < 3 and self.hasMined:
                self.mines.append(Mine(self.ghost.rect.x - 30, self.ghost.rect.y))
                self.hasMined = False
        else:
            self.hasMined = True

    def inputPlayer2(self, keyb):            
        if self.ghostV.rect.y > 0:
            if keyb[pygame.K_w]:
                self.ghostV.move(0,-10)
        if self.ghostV.rect.y + self.ghostV.rect.height < screen.get_height():
            if keyb[pygame.K_s]:
                self.ghostV.move(0,10)
        if self.ghostV.rect.x > 0:
            if keyb[pygame.K_a]:
                self.ghostV.flip = True
                self.ghostV.move(-10,0)
        if self.ghostV.rect.x + self.ghostV.rect.width < screen.get_width():
            if keyb[pygame.K_d]:
                self.ghostV.flip = False
                self.ghostV.move(10,0)
        if keyb[pygame.K_f] and self.hasShot2:
            self.shots2.append(Shoot(self.ghostV.rect.x + self.ghostV.rect.width /2, self.ghostV.rect.y + (self.ghostV.rect.height / 2), self.ghostV.flip))
            self.hasShot2 = False
            self.sfx2.play()
        if not keyb[pygame.K_f]:
            self.hasShot2 = True
        if keyb[pygame.K_g]:
            if len(self.mines2) < 3 and self.hasMined2:
                self.mines2.append(Mine(self.ghostV.rect.x - 30, self.ghostV.rect.y))
                self.hasMined2 = False
        else:
            self.hasMined2 = True            
    
    def draw(self):
        screen.fill((255,255,255))
        self.bg.draw()
      
        pygame.draw.rect(screen, (0,0,255), (10,10, self.ghost.hp * 1.5, 20))
        pygame.draw.rect(screen, (0,255,0), (screen.get_width(),10, -self.ghostV.hp * 1.5, 20))
        
        if self.ghost.alive:
            if self.ghost.strip.i < len(self.ghost.strip.images):
                self.ghost.image = self.ghost.strip.next()
            else:
                self.ghost.strip.i = 0
                if self.ghost.flip:
                    self.ghost.image = pygame.transform.flip(self.ghost.image, True, False)
            if self.ghost.flip:
                self.ghost.image = pygame.transform.flip(self.ghost.image, True, False)
            
            self.ghost.draw()

        if self.ghostV.alive:
            if self.ghostV.strip.i < len(self.ghostV.strip.images):
                self.ghostV.image = self.ghostV.strip.next()
            else:
                self.ghostV.strip.i = 0
                if self.ghostV.flip:
                    self.ghostV.image = pygame.transform.flip(self.ghostV.image, True, False)
            if self.ghostV.flip:
                self.ghostV.image = pygame.transform.flip(self.ghostV.image, True, False)
            
            self.ghostV.draw()
        self.powerup.draw()

        for s in self.shots:
            i = self.shoot1
            if s.flip:
                i = pygame.transform.flip(self.shoot1, True, False)
            screen.blit(i, s.rect)

        for s in self.shots2:
            i = self.shoot2
            if s.flip:
                i = pygame.transform.flip(self.shoot2, True, False)
            screen.blit(i, s.rect)

        for m in self.mines:
            m.draw()

        for m in self.mines2:
            m.draw()
        
        if self.powerup.gotPowerUp == False:
            if self.ghostV.alive:
                if self.ghostV.rect.colliderect(self.powerup.rect):
                    self.powerup.gotPowerUp = True
                    self.ghostV.hp += 50
                    if self.ghostV.hp >200: self.ghostV.hp = 200
            if self.ghost.alive:
                if self.ghost.rect.colliderect(self.powerup.rect) :
                    self.powerup.gotPowerUp = True
                    self.ghost.hp += 50
                    if self.ghost.hp >200: self.ghost.hp = 200
        
        pygame.display.flip()
    


while True:
    if gamestate == 1:
        menu = Menu("images/BGHOME.png", ["Start", option1],["Quit",option2])
        menu.update(60)
        #pygame.display.flip()
    elif gamestate == 2:
        game = Game()
        game.update(60)
        #pygame.display.flip()
    else:
        pygame.quit()
        sys.exit()
