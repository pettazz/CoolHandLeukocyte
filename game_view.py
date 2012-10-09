from cocos.layer import Layer, ColorLayer
from cocos.scene import Scene
from cocos.director import director
from cocos.actions import *

from game_controller import GameController
from game_model import GameModel
from settings import *
from status import *
import levels


class GameView( Layer ):

    def __init__(self, model):
        super(GameView,self).__init__()

        # width, height = director.get_window_size()

        # aspect = width / float(height)
        # self.grid_size = ( int(20 *aspect),20)
        # self.duration = 8

        # self.position = ( width/2 - COLUMNS * SQUARE_SIZE / 2, 0 )
        # self.transform_anchor = ( COLUMNS*SQUARE_SIZE /2, ROWS * SQUARE_SIZE/2)

        # background layer to delimit the pieces visually
        # cl = ColorLayer( 112,66,20,50, width = COLUMNS * SQUARE_SIZE, height=ROWS * SQUARE_SIZE )
        # self.add( cl, z=-1)

        self.model = model

        self.model.push_handlers(self.on_game_over, \
                                    self.on_level_complete, \
                                    self.on_new_level, \
                                    self.on_win \
                                    )

        #self.hud.show_message( 'GET READY', self.model.start )

    def on_enter(self):
        super(GameView,self).on_enter()

        # soundex.set_music('tetris.mp3')
        # soundex.play_music()

    def on_exit(self):
        super(GameView,self).on_exit()
        # soundex.stop_music()

    def on_line_complete( self, lines ):
        # soundex.play('line.mp3')
        return True

    def on_move_block(self ):
        # soundex.play('move.mp3')
        return True

    def on_drop_block(self ):
        # soundex.play('drop.mp3')
        return True

    def on_level_complete( self ):
        soundex.play('level_complete.mp3')
        # self.hud.show_message('Level complete', self.model.set_next_level)
        return True

    def on_new_level( self ):
        # soundex.play('go.mp3')
        self.stop()
        self.do( StopGrid() )
        self.rotation = 0
        self.scale = 1
        return True

    def on_game_over( self ):
        # self.parent.add( gameover.GameOver(win=False), z=10 )
        return True

    def on_win( self ):
        # self.parent.add( gameover.GameOver(win=True), z=10 )
        return True

    def draw(self):
        if self.model.our_hero:
            self.model.our_hero.draw()


def get_newgame():
    '''returns the game scene'''
    scene = Scene()

    # model
    model = GameModel()

    # controller
    controller = GameController(model)

    # view
    view = GameView(model)

    # set controller in model
    model.set_controller(controller)

    # add controller
    scene.add(controller, z=1, name="controller")

    # add view
    #scene.add(BackgroundLayer(), z=0, name="background")
    scene.add(view, z=2, name="view")

    return scene
