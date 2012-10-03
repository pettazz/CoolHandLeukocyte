import sys, os, pygame
from pygame.locals import *


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