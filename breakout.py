#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' BirksBeamer Breakout '''
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAY_WIDTH = 600
PLAY_HEIGHT = 400
TOPLEFT_X = (SCREEN_WIDTH  - PLAY_WIDTH) // 2
TOPLEFT_Y = (SCREEN_HEIGHT - PLAY_HEIGHT) // 2

class BreakoutGame:
    '''' BreakoutGame class '''
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Breakout")
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def game_loop(self):
        ''' this function is called repeatedly to handle the functioning of the game experience '''
        done = False
        # handle any pending events.  All the piece moving and time advancing happens here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        self.draw_window()
        return done

    def play(self):
        ''' the main function of the BreakoutGame object, sets up a clock to
            call our loop function repeatedly at 60 Hz '''
        # start game
        done = False
        clock = pygame.time.Clock()

        # execute the main game loop at 60 Hz
        while not done:
            done = self.game_loop()
            clock.tick_busy_loop(60)

        # all done, do any clean up here:
        pygame.quit()

    def draw_window(self):
        """ draw_window function """
        # start with a solid background
        self.surface.fill((0, 0, 0))

        # write something at the top
        font = pygame.font.Font(None, 48)
        label = font.render('Breakout', 1, (255, 255, 255))
        self.surface.blit(label, (TOPLEFT_X + PLAY_WIDTH/2 - label.get_width()/2, 30))

        # draw the border around the playing area:
        pygame.draw.rect(self.surface,
                         (255, 255, 255),
                         (TOPLEFT_X - 2, TOPLEFT_Y - 2, PLAY_WIDTH + 4, PLAY_HEIGHT + 4),
                         2)

        # update the screen with what we've drawn.
        pygame.display.flip()

def main():
    ''' main function '''
    game = BreakoutGame()
    game.play()

if __name__ == '__main__':
    main()
