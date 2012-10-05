import os, sys

import pygame
from pygame.locals import *
from pygame.sprite import Sprite

from assets.lib import util
from assets.lib.euclid import *

from settings import *

class Leuk(Sprite):

    def __init__(self, screen, startx, starty):
        Sprite.__init__(self)

        self.image, self.rect = util.load_image('white_cell.png', -1)
        self.arm_image, self.arm_rect = util.load_image('arm.png', -1)
        self.screen = screen
        self.pos = Vector2(startx, starty)
        self.targets = {}
        self.target_speeds = []
        self.active_move_keys = []
        self.speed = 0
        self.arm_orientation = Vector2(1, 0)

    def update(self, time_passed):
        #read new input and add changes to vector
        move_keys = [K_w, K_s, K_a, K_d]
        pressed_keys = pygame.key.get_pressed()
        current_move_keys = [i for i in move_keys if pressed_keys[i]]
        new_active_move_keys = [i for i in current_move_keys if i not in self.active_move_keys]
        util.debug_print(current_move_keys)
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
                    new_target.y = new_target.y + SCREEN_HEIGHT + 10
                if K_s in new_active_move_keys:
                    new_target.y = new_target.y - SCREEN_HEIGHT + 10
                if K_a in new_active_move_keys:
                    new_target.x = new_target.x + SCREEN_WIDTH + 10
                if K_d in new_active_move_keys:
                    new_target.x = new_target.x - SCREEN_WIDTH + 10
                self.targets[new_active_move_keys[0]] = (new_target, 3)
        self.active_move_keys = current_move_keys
        util.debug_print(self.targets)
        secs_passed = time_passed / 100.

        util.debug_print("position: %s" % self.pos)

        #make position changes based on current direction vector and speed
        for i in self.targets.keys():
            target = self.targets[i]
            util.debug_print(target)
            speed = target[1]
            distance = speed * secs_passed
            t = target[0]
            displacement = Vector2(    
                self.pos.x - t.x,
                self.pos.y - t.y)
            util.debug_print("displacement: %s" % displacement)
            displacement = displacement.normalize()
            util.debug_print("normalized displacement: %s" % displacement)
            self.pos += displacement * distance

            #decelerate per tick
            if speed > 0.:
                self.targets[i] = (t, speed - 2)
            if speed < 0:
                self.targets[i] =  (t, 0)
            if speed == 0:
                del self.targets[i]

        mouse_pos = pygame.mouse.get_pos()
        self.arm_orientation = Vector2(mouse_pos[0], mouse_pos[1]).normalized()
        util.debug_print(self.arm_orientation)
        #self.arm_image = pygame.transform.rotate(self.arm_image, -self.arm_orientation.get_angle())


    def blit_my_bits(self):
        image_w, image_h = self.image.get_size()
        draw_pos = self.image.get_rect().move(
            self.pos.x - image_w / 2, 
            self.pos.y - image_h / 2)
        self.screen.blit(self.image, draw_pos)

        arm_image_w, arm_image_h = self.image.get_size()
        draw_pos = self.image.get_rect().move(
            self.pos.x - image_w / 2, 
            self.pos.y - image_h / 2)
        self.screen.blit(self.image, draw_pos)

        if DEBUG:
            #blit the debug target vector lines
            for i in self.targets:
                t = self.targets[i][0]
                pygame.draw.line(self.screen, (255, 255, 255), (t.x, t.y), (self.pos.x, self.pos.y))