import pyglet

import cocos
from cocos import euclid
from cocos.actions import *

from settings import *

class HelloWorld(cocos.layer.ColorLayer):
    def __init__(self):
        super(HelloWorld, self).__init__(178, 0, 0, 255)

        self.whitey = Whitey(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2)

        self.add(self.whitey, z=1)

class Whitey(cocos.sprite.Sprite):

    is_event_handler = True

    def __init__(self, startx, starty):
        super(Whitey, self).__init__('assets/images/white_cell.png')

        self.position = startx, starty

    def on_key_press (self, key, modifiers):
        print key


if __name__ == '__main__':
    cocos.director.director.init(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    cocos.director.director.run(cocos.scene.Scene(HelloWorld()))