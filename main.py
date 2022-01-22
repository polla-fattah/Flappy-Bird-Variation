import math
from random import randint
from collections import deque
import pygame
from pygame.locals import *
import sgc
from sgc.locals import *

from param import const
from param import Param
from flappy import Flappy
from columns import Columns
from play import Play


play = None

class StartButton(sgc.Button):
    def __init__(self, s):
        super(StartButton, self).__init__(label="Start", pos=(120, 100))
        self.s = s

    def on_click(self):
        global play
        play = Play(self.s)
        play.game_over = False
        play.paused = False
        play.life = const.life

class StopButton(sgc.Button):
    def on_click(self):
        play.done = True

class ResetButton(sgc.Button):
    def on_click(self):
        global const
        const.reset()
        const.save()
        const.load_images()

class SoundSwitch(sgc.Switch):
    def on_click(self):
        global const
        const.sound = not const.sound
        const.save()


class EasyRadio(sgc.Radio):
    def __init__(self, selected):
        if selected:
            super(EasyRadio, self).__init__(group="group1", label="Easy", active=True)
        else:
            super(EasyRadio, self).__init__(group="group1", label="Easy")

    def on_select(self):
        global const
        const.life = 5
        const.columninterval = 2500
        const.mode = 'easy'
        const.save()

class NormalRadio(sgc.Radio):
    def __init__(self, selected):
        if selected:
            super(NormalRadio, self).__init__(group="group1", label="Normal", active=True)
        else:
            super(NormalRadio, self).__init__(group="group1", label="Normal")

    def on_select(self):
        global const
        const.life = 3
        const.space = 2.7
        const.columninterval = 2000
        const.mode = 'normal'
        const.save()


class HardRadio(sgc.Radio):
    def __init__(self, selected):
        if selected:
            super(HardRadio, self).__init__(group="group1", label="Hard", active=True)
        else:
            super(HardRadio, self).__init__(group="group1", label="Hard")

    def on_select(self):
        global const
        const.life = 1
        const.space = 2.5
        const.columninterval = 1500
        const.mode = 'hard'
        const.save()

def main():
    global play, lbl_best, lbl_current
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Flappy the Saphier  Eater')
    clock = pygame.time.Clock()
    display_surface = sgc.surface.Screen((const.win_width, const.win_height))
    play = Play(display_surface)

    StartButton(display_surface).add(1)
    StopButton(label="Quit", pos=(320, 100)).add(2)
    ResetButton(label="Reset", pos=(210, 430)).add(3)


    difficulty_label = sgc.Label(text='Difficulty : ', pos=(40,400))
    difficulty_label.add()
    option_label = sgc.Label(text='Options : ', pos=(270,380))
    option_label.add()


    radio1 = EasyRadio(const.mode == 'easy')
    radio2 = NormalRadio(const.mode == 'normal')
    radio3 = HardRadio(const.mode == 'hard')



    radio_box = sgc.VBox(widgets=(radio1, radio2, radio3), pos=(40,430))
    radio_box.add(order=4)

    SoundSwitch(label="Sound ", pos=(430,440), state = const.sound, label_side='left').add(order=3)

    sgc.Label(text='Scores...', pos=(315,250)).add()
    sgc.Label(text='___________', pos=(300,260)).add()

    lbl_best = sgc.Label(text='Best: ' + str(const.best_score), pos=(320,280))
    lbl_best.add()
    lbl_current = sgc.Label(text='Current: ' + str(play.score), pos=(320,300))
    lbl_current.add()

    while not play.done:
        time = clock.tick(const.fps)
        play.generat_next_col()
        for e in pygame.event.get():
            sgc.event(e)
            play.playtime_events(e)

        if not play.game_over:
            play.draw()
        else:
            lbl_best.text = 'Best: ' + str(const.best_score)
            lbl_current.text = 'Current: ' + str(play.score)
            display_surface.blit(const.images['startBackground'], (0, 0))
            sgc.update(time)

        pygame.display.flip()

    print('Game over! Score: %i' % play.score)
    pygame.quit()


if __name__ == '__main__':
    # If this module had been imported, __name__ would be 'flappybird'.
    # It was executed (e.g. by double-clicking the file), so call main.
    main()
