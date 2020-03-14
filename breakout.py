#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' BirksBeamer Breakout '''
import math
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAY_WIDTH = 600
PLAY_HEIGHT = 400
TOPLEFT_X = (SCREEN_WIDTH  - PLAY_WIDTH) // 2
TOPLEFT_Y = (SCREEN_HEIGHT - PLAY_HEIGHT) // 2
BACKGROUND_COLOR = (84, 13, 110)
FONT_COLOR = (14, 173, 105)
BORDER_COLOR = (255, 210, 63)
BALL_COLOR = (238, 66, 102)
BALL_RADIUS = 10
PADDLE_COLOR = (59, 206, 172)
PADDLE_HEIGHT = 8
PADDLE_WIDTH = 100
PADDLE_MOVE_SPEED = 2
MAX_ANGLE_CHANGE = 2 * math.atan(1)
MAX_DEPART_ANGLE = math.acos(.5)

class Point:
    ''' a simple class to keep track of coordinates'''
    def __init__(self, x, y):
        self.x = x
        self.y = y

class BreakoutBall:
    '''' BreakoutBall class '''
    def __init__(self):
        self.location = Point(TOPLEFT_X + PLAY_WIDTH / 2, TOPLEFT_Y + PLAY_HEIGHT / 2)
        self.velocity = Point(2, -2)

    def set_location(self, x, y, vel_x, vel_y):
        ''' moves the ball to the provided location '''
        self.location.x = TOPLEFT_X + x
        self.location.y = TOPLEFT_X + y
        self.velocity.x = vel_x
        self.velocity.y = vel_y

    def move(self, paddle_location):
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
        if self.location.y >= TOPLEFT_Y + PLAY_HEIGHT:
            self.location.y = TOPLEFT_Y + PLAY_HEIGHT
            self.velocity.y = 0
            self.velocity.x = 0
            # this is a problem -- off the end of the screen
            return False

        if self.location.y > TOPLEFT_Y + PLAY_HEIGHT - PADDLE_HEIGHT:
            distance_to_paddle_center = self.location.x - paddle_location
            if abs(distance_to_paddle_center) <= PADDLE_WIDTH / 2:
                self.location.y = TOPLEFT_Y + PLAY_HEIGHT - PADDLE_HEIGHT
                # paddle hit
                speed = math.sqrt(self.velocity.x*self.velocity.x + self.velocity.y*self.velocity.y)
                angle_of_incidence = math.asin(self.velocity.x/speed)
                angle_change = MAX_ANGLE_CHANGE * distance_to_paddle_center / (PADDLE_WIDTH / 2)
                angle_of_reflection = angle_of_incidence
                angle_of_reflection += angle_change
                if angle_of_reflection > MAX_DEPART_ANGLE:
                    angle_of_reflection = MAX_DEPART_ANGLE
                if angle_of_reflection < -MAX_DEPART_ANGLE:
                    angle_of_reflection = -MAX_DEPART_ANGLE

                self.velocity.x = +speed * math.sin(angle_of_reflection)
                self.velocity.y = -speed * math.cos(angle_of_reflection)

        return True

class BreakoutPaddle:
    '''' BreakoutPaddle class '''
    def __init__(self):
        self.location = Point(TOPLEFT_X + PLAY_WIDTH / 2, TOPLEFT_Y + PLAY_HEIGHT - PADDLE_HEIGHT)

    def set_location(self, x):
        ''' moves the paddle to the provided location '''
        self.location.x = x
        if self.location.x > TOPLEFT_X + PLAY_WIDTH - PADDLE_WIDTH / 2:
            self.location.x = TOPLEFT_X + PLAY_WIDTH - PADDLE_WIDTH / 2
        if self.location.x < TOPLEFT_X + PADDLE_WIDTH / 2:
            self.location.x = TOPLEFT_X + PADDLE_WIDTH / 2

    def move(self, relative_x):
        ''' move the paddle by a relative amount from current location '''
        self.set_location(self.location.x + relative_x)

class BreakoutGame:
    '''' BreakoutGame class '''
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Breakout")
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.ball = BreakoutBall()
        self.paddle = BreakoutPaddle()
        self.lives = 3

    def game_loop(self):
        ''' this function is called repeatedly to handle the functioning of the game experience '''
        running = True
        # handle any pending events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.paddle.move(-PADDLE_MOVE_SPEED)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.paddle.move(+PADDLE_MOVE_SPEED)

        if self.ball.move(self.paddle.location.x):
            self.draw_window()
        else:
            # ball is lost
            self.lives -= 1
            if self.lives == 0:
                running = False
            self.ball.set_location(50, 50, 2, -2)

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

    def draw_window(self, draw_ball=True):
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
        if draw_ball:
            pygame.draw.circle(self.surface,
                               BALL_COLOR,
                               (self.ball.location.x, self.ball.location.y),
                               BALL_RADIUS)

        # draw the paddle around the playing area:
        pygame.draw.rect(self.surface,
                         PADDLE_COLOR,
                         (self.paddle.location.x - PADDLE_WIDTH / 2,
                          self.paddle.location.y,
                          PADDLE_WIDTH,
                          PADDLE_HEIGHT),
                         0)

        for ball_index in range(self.lives - 1):
            pygame.draw.circle(self.surface,
                               BALL_COLOR,
                               (TOPLEFT_X + BALL_RADIUS + 3*BALL_RADIUS*ball_index,
                                TOPLEFT_Y + PLAY_HEIGHT + 2*BALL_RADIUS),
                               BALL_RADIUS)

         # update the screen with what we've drawn.
        pygame.display.flip()

def main():
    ''' main function '''
    game = BreakoutGame()
    game.play()

if __name__ == '__main__':
    main()
