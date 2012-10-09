import weakref

import pyglet

import cocos
from cocos import euclid
from cocos.actions import *

from settings import *
from status import *

class GameModel(pyglet.event.EventDispatcher):
    def __init__(self):
        super(GameModel,self).__init__()

        self.our_hero = Leuk(int(settings.screen_height / 4), int(settings.screen_height / 2))

        status.reset()
        # # phony level
        # status.level = levels.levels[0]

    def start(self):
        self.set_next_level()

    def set_next_level(self):
        self.controller().resume_controller()

        if status.level_id is None:
            status.level_id = 0
        else:
            status.level_id += 1

        l = levels.levels[status.level_id]

        status.level = l()

        self.dispatch_event("on_new_level")

    def set_controller(self, controller):
        self.controller = weakref.ref(controller)

GameModel.register_event_type('on_level_complete')
GameModel.register_event_type('on_new_level')
GameModel.register_event_type('on_game_over')
GameModel.register_event_type('on_win')


class Leuk( object ):
    def __init__(self, startx, starty):
        super(Leuk, self).__init__()
        self.position = (startx, starty)
        self.image = pyglet.resource.image('assets/images/white_cell.png')

    def draw(self):
        self.image.blit(self.position[0] - int(self.image.width / 2), self.position[1] - int(self.image.height / 2))
