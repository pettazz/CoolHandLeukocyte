import copy, random

import pyglet
from pyglet.window import key

from cocos.layer import Layer
from cocos.scene import Scene
from cocos import euclid

from status import *

class GameController( Layer ):
    is_event_handler = True #: enable pyglet's events

    def __init__(self, model):
        super(GameController, self).__init__()

        self.used_key = False
        self.paused = True

        self.model = model
        self.elapsed = 0

    def on_key_press(self, keys, modifiers):
        if self.paused:
            return False

        if key in (key.W, key.A, key.S, key.D):
            if k == key.A:
                self.model.whitey.keypress_left()
            elif k == key.D:
                self.model.whitey.keypress_right()
            elif k == key.S:
                self.model.whitey.keypress_down()
            elif k == key.W:
                self.model.whitey.keypress_up()
            
            return True
        return False

    def pause_controller(self):
        '''removes the schedule timer and doesn't handler the keys'''
        self.paused = True
        self.unschedule(self.step)

    def resume_controller(self):
        '''schedules  the timer and handles the keys'''
        self.paused = False
        self.schedule(self.step)

    def step(self, dt):
        '''updates the engine'''
        self.elapsed += dt
        if self.elapsed > status.level.speed:
            self.elapsed = 0
            self.model.block_down( sound=False)