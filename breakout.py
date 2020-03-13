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
BACKGROUND_COLOR = (0, 0, 0)
FONT_COLOR = (255, 255, 255)
BORDER_COLOR = (255, 255, 255)
BALL_COLOR = (255, 255, 255)
BALL_RADIUS = 10

class Point:
    ''' a simple class to keep track of coordinates'''
    def __init__(self, x, y):
        self.x = x
        self.y = y

class BreakoutBall:
    '''' BreakoutBall class '''
    def __init__(self):
        self.location = Point(TOPLEFT_X + PLAY_WIDTH / 2, TOPLEFT_Y + PLAY_HEIGHT / 2)
        self.velocity = Point(1, 1)
        
    def move(self):
        ''' moves the ball and bounces off of the constraints of our field '''
        self.location.x += self.velocity.x
        if self.location.x < TOPLEFT_X:
            self.location.x = TOPLEFT_X
            self.velocity.x = -self.velocity.x
        if self.location.x > TOPLEFT_X + PLAY_WIDTH:
            self.location.x = TOPLEFT_X + PLAY_WIDTH
            self.velocity.x = -self.velocity.x

        self.location.y += self.velocity.y
        if self.location.y < TOPLEFT_Y:
            self.location.y = TOPLEFT_Y
            self.velocity.y = -self.velocity.y
        if self.location.y > TOPLEFT_Y + PLAY_HEIGHT:
            self.location.y = TOPLEFT_Y + PLAY_HEIGHT
            self.velocity.y = -self.velocity.y

class BreakoutGame:
    '''' BreakoutGame class '''
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Breakout")
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.ball = BreakoutBall()

    def game_loop(self):
        ''' this function is called repeatedly to handle the functioning of the game experience '''
        running = True
        # handle any pending events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        self.ball.move()
        self.draw_window()
        return running

    def play(self):
        ''' the main function of the BreakoutGame object, sets up a clock to
            call our loop function repeatedly at 60 Hz '''
        # start game
        running = True
        clock = pygame.time.Clock()

        # execute the main game loop at 60 Hz
        while running:
            running = self.game_loop()
            clock.tick_busy_loop(60)

        # all done, do any clean up here:
        pygame.quit()

    def draw_window(self):
        """ draw_window function """
        # start with a solid background
        self.surface.fill(BACKGROUND_COLOR)

        # write something at the top
        font = pygame.font.Font(None, 48)
        label = font.render('Breakout', 1, FONT_COLOR)
        self.surface.blit(label, (TOPLEFT_X + PLAY_WIDTH/2 - label.get_width()/2, 30))

        # draw the border around the playing area:
        pygame.draw.rect(self.surface,
                         BORDER_COLOR,
                         (TOPLEFT_X - 2, TOPLEFT_Y - 2, PLAY_WIDTH + 4, PLAY_HEIGHT + 4),
                         2)

        # draw the ball around the playing area:
        pygame.draw.circle(self.surface,
                           BALL_COLOR,
                           (self.ball.location.x, self.ball.location.y),
                           BALL_RADIUS)

        # update the screen with what we've drawn.
        pygame.display.flip()

def main():
    ''' main function '''
    game = BreakoutGame()
    game.play()

if __name__ == '__main__':
    main()
