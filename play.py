from collections import deque

import pygame
from pygame.locals import *

from param import const
from flappy import Flappy
from columns import Columns

class Play:
    def __init__(self, display_surface):
        self.columns = deque()

        self.frame_clock = 0  # this counter is only incremented if the game isn't paused
        self.score = 0
        self.done = False
        self.paused = self.game_over = True

        self.display_surface = display_surface
        self.score_font = pygame.font.SysFont(None, 32, bold=True)  # default font
        self.score_surface = self.score_font.render(str(self.score), True, (255, 255, 255))

        self.images = const.load_images()

        # the bird stays in the same x position, so bird.x is a constant
        # center bird on screen
        self.bird = Flappy(50, int(const.win_height/2 - Flappy.HEIGHT/2), 2,
                    (self.images['bird-wingup'], self.images['bird-wingdown']))
        self.wing_sound = pygame.mixer.Sound("sounds/wing.ogg")
        self.hit_sound = pygame.mixer.Sound('sounds/hit.ogg')
        self.die_sound = pygame.mixer.Sound('sounds/die.ogg')
        self.life = const.life


    def draw(self):
        global const
        if self.paused:
            return  # don't draw anything

        # check for collisions
        column_collision = any(pygame.sprite.collide_mask(p, self.bird) for p in self.columns) # uses pygame method to find any collesion
        if column_collision or 0 >= self.bird.y or self.bird.y >= const.win_height - Flappy.HEIGHT:
            self.columns.clear()
            self.bird.x, self.bird.y = 50, int(const.win_height/2 - Flappy.HEIGHT/2)
            self.life -= 1
            if self.life == 0:
                const.save()
                if const.sound: self.die_sound.play()
                self.game_over = True
                self.paused = True
            else:
                if const.sound: self.hit_sound.play()


        for x in (0, const.win_width ):
            self.display_surface.blit(self.images['background'], (x, 0))

        while self.columns and not self.columns[0].visible:
            self.columns.popleft()

        for p in self.columns:
            p.update()
            self.display_surface.blit(p.image, p.rect)

        self.bird.update()
        self.display_surface.blit(self.bird.image, self.bird.rect)

        # update and display score
        for p in self.columns:
            if p.x + Columns.WIDTH < self.bird.x and not p.score_counted:
                self.score += 1
                if self.score >= const.best_score:
                    const.best_score = self.score
                p.score_counted = True

        self.score_surface = self.score_font.render('Life: ' + str(self.life) + '     Score: '
                                                    + str(self.score) + '    Best: ' + str(const.best_score)
                                                    , True, (255, 255, 255))
        score_x = const.win_width/2 - self.score_surface.get_width()/2
        self.display_surface.blit(self.score_surface, (score_x, Columns.PIECE_HEIGHT))

        self.frame_clock += 1

    def generat_next_col(self):
        if not (self.paused or self.frame_clock % const.msec_to_frames(const.columninterval)):
            pp = Columns(self.images['column-end'], self.images['column-body'])
            self.columns.append(pp)

    def playtime_events(self, e):
        if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
            self.done = True
        elif e.type == KEYUP and e.key in (K_PAUSE, K_p):
            self.paused = not self.paused
        elif e.type == MOUSEBUTTONUP or (e.type == KEYUP and
                e.key in (K_UP, K_RETURN, K_SPACE)):
            if not self.paused and const.sound:
                self.wing_sound.play()
            self.bird.msec_to_climb = Flappy.CLIMB_DURATION
