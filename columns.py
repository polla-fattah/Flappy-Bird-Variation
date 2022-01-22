from random import randint

import pygame
from pygame.locals import *
from flappy import Flappy

from param import const


class Columns(pygame.sprite.Sprite):
    """Represents an obstacle.

    A Columns has a top and a bottom column, and only between them can
    the bird pass -- if it collides with either part, the game is over.

    Attributes:
    x: The Columns's X position.  This is a float, to make movement
        smoother.  Note that there is no y attribute, as it will only
        ever be 0.
    image: A pygame.Surface which can be blitted to the display surface
        to display the Columns.
    mask: A bitmask which excludes all pixels in self.image with a
        transparency greater than 127.  This can be used for collision
        detection.
    top_pieces: The number of pieces, including the end piece, in the
        top column.
    bottom_pieces: The number of pieces, including the end piece, in
        the bottom column.

    Constants:
    WIDTH: The width, in pixels, of a column piece. Because a column is
        only one piece wide, this is also the width of a Columns's
        image.
    PIECE_HEIGHT: The height, in pixels, of a column piece.
    ADD_INTERVAL: The interval, in milliseconds, in between adding new
        columns.
    """

    WIDTH = 80
    PIECE_HEIGHT = 32

    def __init__(self, column_end_img, column_body_img):
        """Initialises a new random Columns.

        The new Columns will automatically be assigned an x attribute of
        float(const.win_width - 1).

        Arguments:
        column_end_img: The image to use to represent a column's end piece.
        column_body_img: The image to use to represent one horizontal slice
            of a column's body.
        """
        self.x = float(const.win_width - 1)
        self.score_counted = False

        self.image = pygame.Surface((Columns.WIDTH, const.win_height), SRCALPHA)
        self.image.convert()   # speeds up blitting
        self.image.fill((0, 0, 0, 0))
        total_column_body_pieces = int(
            (const.win_height -                  # fill window from top to bottom
             const.space * Flappy.HEIGHT -             # make room for bird to fit through
             const.space * Columns.PIECE_HEIGHT) /  # 2 end pieces + 1 body piece
            Columns.PIECE_HEIGHT          # to get number of column pieces
        )
        self.bottom_pieces = randint(1, total_column_body_pieces)
        self.top_pieces = total_column_body_pieces - self.bottom_pieces

        # bottom column
        for i in range(1, self.bottom_pieces + 1):
            piece_pos = (0, const.win_height - i*Columns.PIECE_HEIGHT)
            self.image.blit(column_body_img, piece_pos)
        bottom_column_end_y = const.win_height - self.bottom_height_px
        bottom_end_piece_pos = (0, bottom_column_end_y - Columns.PIECE_HEIGHT)
        self.image.blit(column_end_img, bottom_end_piece_pos)

        # top column
        for i in range(self.top_pieces):
            self.image.blit(column_body_img, (0, i * Columns.PIECE_HEIGHT))
        top_column_end_y = self.top_height_px
        self.image.blit(column_end_img, (0, top_column_end_y))

        # compensate for added end pieces
        self.top_pieces += 1
        self.bottom_pieces += 1

        # for collision detection
        self.mask = pygame.mask.from_surface(self.image)

    @property
    def top_height_px(self):
        """Get the top column's height, in pixels."""
        return self.top_pieces * Columns.PIECE_HEIGHT

    @property
    def bottom_height_px(self):
        """Get the bottom column's height, in pixels."""
        return self.bottom_pieces * Columns.PIECE_HEIGHT

    @property
    def visible(self):
        """Get whether this Columns on screen, visible to the player."""
        return -Columns.WIDTH < self.x < const.win_width

    @property
    def rect(self):
        """Get the Rect which contains this Columns."""
        return Rect(self.x, 0, Columns.WIDTH, Columns.PIECE_HEIGHT)

    def update(self, delta_frames=1):
        """Update the Columns's position.

        Arguments:
        delta_frames: The number of frames elapsed since this method was
            last called.
        """
        self.x -= const.animation_speed * const.frames_to_msec(delta_frames)



