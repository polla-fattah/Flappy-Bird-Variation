import math
import pygame
from pygame.locals import *

from param import const


class Flappy(pygame.sprite.Sprite):
    WIDTH = const.flappywidth # The width, in pixels, of the bird's image.
    HEIGHT = const.flappyheight # The height, in pixels, of the bird's image.
    SINK_SPEED = const.flappysink_speed # With which speed, in pixels per millisecond, the bird descends in one second while not climbing
    CLIMB_SPEED = const.flappyclimb_speed # bird ascends in one second while climbing, on average.
    CLIMB_DURATION = const.flappyclimb_duration # The number of milliseconds it takes the bird to execute a complete climb.

    def __init__(self, x, y, msec_to_climb, images):
        super(Flappy, self).__init__()
        self.x, self.y = x, y
        self.msec_to_climb = msec_to_climb
        self._img_wingup, self._img_wingdown = images
        self._mask_wingup = pygame.mask.from_surface(self._img_wingup) # image of the bird with its wing pointing upward
        self._mask_wingdown = pygame.mask.from_surface(self._img_wingdown) #image of the bird with its wing pointing downward

    def update(self, delta_frames=1):# Update the bird's position.
        """
        One complete climb lasts CLIMB_DURATION milliseconds, during which
        the bird ascends with an average speed of CLIMB_SPEED px/ms.
        This Flappy's msec_to_climb attribute will automatically be
        decreased accordingly if it was > 0 when this method was called.

        Arguments:
        delta_frames: The number of frames elapsed since this method was
            last called.
        """
        if self.msec_to_climb > 0:
            self.y -= (Flappy.CLIMB_SPEED * const.frames_to_msec(delta_frames))
            self.msec_to_climb -= const.frames_to_msec(delta_frames)
        else:
            self.y += Flappy.SINK_SPEED * const.frames_to_msec(delta_frames)

    @property
    def image(self): # responsible of returninig
        if pygame.time.get_ticks() % 700 >= 350:
            return self._img_wingup
        return self._img_wingdown

    @property
    def rect(self): #This function is important to detect colletion with columns and upper lower frame
        return Rect(self.x, self.y, Flappy.WIDTH, Flappy.HEIGHT)