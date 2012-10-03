#!/usr/bin/python

import os, sys
from random import randint, choice
from math import sin, cos, radians

import pygame
from pygame.locals import *
from pygame.sprite import Sprite

from assets.lib.euclid import *


# Game parameters
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BG_COLOR = 150, 150, 80


def load_image(name, colorkey=None, pngTransparency=None):
    fullname = os.path.join('assets/images/', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
        
    if colorkey is not None:
        image = image.convert()
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    elif pngTransparency is not None:
        image = image.convert_alpha()
        
    return image, image.get_rect()


class Whitey(Sprite):

    def __init__(self, screen, startx, starty):
        Sprite.__init__(self)

        self.image, self.rect = load_image('bluecreep.png', -1)
        self.target_image, self.target_rect = load_image('graycreep.png', -1)
        self.screen = screen
        self.pos = Vector2(startx, starty)
        self.targets = {}
        self.target_speeds = []
        self.active_move_keys = []
        self.speed = 0

    def update(self, time_passed):
        #read new input and add changes to vector
        move_keys = [K_w, K_s, K_a, K_d]
        pressed_keys = pygame.key.get_pressed()
        current_move_keys = [i for i in move_keys if pressed_keys[i]]
        new_active_move_keys = [i for i in current_move_keys if i not in self.active_move_keys]
        print current_move_keys
        self.active_move_keys
        if current_move_keys:
            for i in self.targets.keys():
                if i in current_move_keys:
                    self.targets[i] = self.targets[i][0], self.targets[i][1] + 3
                    #cap max speed
                    if self.targets[i][1] > 20:
                        self.targets[i] = (self.targets[i][0], 20)
            if new_active_move_keys:
                new_target = Vector2(self.pos.x, self.pos.y)
                if K_w in new_active_move_keys:
                    new_target.y = new_target.y + SCREEN_HEIGHT * 2
                if K_s in new_active_move_keys:
                    new_target.y = new_target.y - SCREEN_HEIGHT * 2
                if K_a in new_active_move_keys:
                    new_target.x = new_target.x + SCREEN_WIDTH * 2
                if K_d in new_active_move_keys:
                    new_target.x = new_target.x - SCREEN_WIDTH * 2
                self.targets[new_active_move_keys[0]] = (new_target, 3)
        self.active_move_keys = current_move_keys
        print self.targets
        secs_passed = time_passed / 100.

        print "position: %s" % self.pos

        #make position changes based on current direction vector and speed
        for i in self.targets.keys():
            target = self.targets[i]
            print target
            speed = target[1]
            distance = speed * secs_passed
            # print "distance: %s" % distance
            t = target[0]
            displacement = Vector2(    
                self.pos.x - t.x,
                self.pos.y - t.y)
            print "displacement: %s" % displacement
            displacement = displacement.normalize()
            print "normalized displacement: %s" % displacement
            self.pos += displacement * distance

            #decelerate per tick
            if speed > 0.:
                self.targets[i] = (t, speed - 2)
            if speed < 0:
                self.targets[i] =  (t, 0)
            if speed == 0:
                del self.targets[i]


    def blitme(self):
        self.image_w, self.image_h = self.image.get_size()
        draw_pos = self.image.get_rect().move(
            self.pos.x - self.image_w / 2, 
            self.pos.y - self.image_h / 2)
        self.screen.blit(self.image, draw_pos)

        #blit the debug target images
        for i in self.targets:
            t = self.targets[i][0]
            target_image_w, target_image_h = self.target_image.get_size()
            target_draw_pos = self.target_image.get_rect().move(
                t.x - target_image_w / 2, 
                t.y - target_image_h / 2)
            self.screen.blit(self.target_image, target_draw_pos)
            pygame.draw.line(self.screen, (255, 0, 0), (t.x, t.y), (self.pos.x, self.pos.y))


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()
    startx = SCREEN_WIDTH / 2
    starty = SCREEN_HEIGHT / 2
    whitey = Whitey(screen, startx, starty)

    while True:
        time_passed = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if(event.key == K_ESCAPE):
                    sys.exit()
        
        # Redraw the background
        screen.fill(BG_COLOR)
        
        whitey.update(time_passed)
        whitey.blitme()

        pygame.display.flip()



run_game()
