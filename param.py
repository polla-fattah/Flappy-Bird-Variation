import os
import pygame
import pickle

'''
This class is responsible of initializing, saving, resetting and loading all
important constants and parameters as well as used images in the game.
'''
class Param:
    FPS = 60 # Frame/Second
    ANIMATION_SPEED = 0.18  # pixels per millisecond
    WIN_WIDTH = 568     # windows width
    WIN_HEIGHT = 512	# windows hight

    Flappy_WIDTH = 64	# The bird's width 
    Flappy_HEIGHT = 64 # The bird's hight 
    Flappy_SINK_SPEED = 0.18 # at which speed the bird will fall if not flapped up
    Flappy_CLIMB_SPEED = 0.3 # the climb speed of the bird
    Flappy_CLIMB_DURATION = 333.3 # how much each climb command will levitate the bird
    ADD_INTERVAL = 2500	# the horizontal distance between two columns
    DATA_FILE = 'data.pkl' # 
    SPACE = 3 #vertical distance between columns

	'''
	Calls reset to initiate all object variables, the reset is creted so that 
	we can change to the defaults atany time by calling reset function of the object.
	'''
    def __init__(self):
        self.reset()

	'''
	
	'''
    def save(self):
        dataFile = open(Param.DATA_FILE, 'wb')
        pickle.dump(self, dataFile, pickle.HIGHEST_PROTOCOL)
        dataFile.close()

    @staticmethod
    def load():
        file = open(Param.DATA_FILE, 'rb')
        return pickle.load(file)


    def reset(self):
        self.fps = Param.FPS
        self.animation_speed = Param.ANIMATION_SPEED
        self.win_width = Param.WIN_WIDTH
        self.win_height = Param.WIN_HEIGHT

        self.flappywidth = Param.Flappy_WIDTH
        self.flappyheight = Param.Flappy_HEIGHT
        self.flappysink_speed = Param.Flappy_SINK_SPEED
        self.flappyclimb_speed = Param.Flappy_CLIMB_SPEED
        self.flappyclimb_duration = Param.Flappy_CLIMB_DURATION
        self.columninterval = Param.ADD_INTERVAL

        self.best_score = 0
        self.images = None
        self.sound = True
        self.mode = 'easy'
        self.life = 5
        self.space = 3


    def frames_to_msec(self, frames): # Convert Number frames to milliseconds
        return 1000.0 * frames / self.fps


    def msec_to_frames(self, milliseconds):# Convert milliseconds to frames
        return self.fps * milliseconds / 1000.0

    def load_images(self):
        # Load all images required by the game and return a dict of them.

        def load_image(img_file_name):
            # Return the loaded pygame image with the specified file name.
            file_name = os.path.join('.', 'images', img_file_name)
            img = pygame.image.load(file_name)
            img.convert()
            return img

        self.images = {'background': load_image('background.png'),
                        'column-end': load_image('column_end.png'),
                        'column-body': load_image('column_body.png'),
                        'bird-wingup': load_image('bird_wing_up.png'),
                        'bird-wingdown': load_image('bird_wing_down.png'),
                        'startBackground': load_image('startBackground.png')}
        return self.images

try:
    const = Param.load()
    const.save()
except IOError:
    const = Param()

