#!/usr/bin/python

import os, sys

import pygame
from pygame.locals import *

from Leuk import Leuk

from settings import *

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()
    startx = SCREEN_WIDTH / 2
    starty = SCREEN_HEIGHT / 2
    our_hero = Leuk(screen, startx, starty)

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
        
        our_hero.update(time_passed)
        our_hero.blit_my_bits()

        pygame.display.flip()


run_game()
