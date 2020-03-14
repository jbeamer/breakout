#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' BirksBeamer Breakout '''
import math
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAY_WIDTH = 780
PLAY_HEIGHT = 400
TOPLEFT_X = (SCREEN_WIDTH  - PLAY_WIDTH) // 2
TOPLEFT_Y = (SCREEN_HEIGHT - PLAY_HEIGHT) // 2
BACKGROUND_COLOR = (200, 200, 200)
FONT_COLOR = (84, 13, 110)
BORDER_COLOR = (255, 210, 63)
BALL_COLOR = (238, 66, 102)
BALL_RADIUS = 10
PADDLE_COLOR = (14, 173, 105)
PLAYAREA_COLOR = (40, 40, 40)
PADDLE_HEIGHT = 8
PADDLE_WIDTH = 100
PADDLE_MOVE_SPEED = 4
MAX_ANGLE_CHANGE = 2 * math.atan(1)
MAX_DEPART_ANGLE = math.acos(.5)

BRICK_ROWS = 5
BRICK_COLS = 25
BRICK_HEIGHT = 20
BRICK_SPACING = 2
BRICK_WIDTH = (PLAY_WIDTH - (BRICK_COLS + 1) * BRICK_SPACING) / BRICK_COLS
ATTIC_HEIGHT = 60
BRICK_COLORS = ((188, 182, 255),
                (184, 225, 255),
                (169, 255, 247),
                (148, 251, 171),
                (130, 171, 161))

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

class BreakoutBrick:
    '''' BreakoutBrick class '''
    def __init__(self, col, row):
        self.grid_location = Point(row, col)
        x = TOPLEFT_X + BRICK_WIDTH / 2 + BRICK_SPACING + col * (BRICK_WIDTH + BRICK_SPACING)
        y = TOPLEFT_Y + ATTIC_HEIGHT + BRICK_HEIGHT / 2 + row * (BRICK_HEIGHT + BRICK_SPACING)
        self.screen_location = Point(x, y)
        self.hidden = False

    def hit_test(self, ball):
        ''' brick hit test '''
        if self.hidden:
            return False

        if abs(ball.location.x - self.screen_location.x) <= BRICK_WIDTH / 2 + BALL_RADIUS:
            if abs(ball.location.y - self.screen_location.y) <= BRICK_HEIGHT / 2 + BALL_RADIUS:
                self.hidden = True
                # change the ball direction - TODO: this is too simplistic
                ball.velocity.y = -ball.velocity.y
                return True
        return False

class BreakoutGame:
    '''' BreakoutGame class '''
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Dad's Awesome Breakout")
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.ball = BreakoutBall()
        self.paddle = BreakoutPaddle()
        self.lives = 3
        self.bricks = {}
        for i in range(BRICK_COLS):
            for j in range(BRICK_ROWS):
                self.bricks[(i, j)] = BreakoutBrick(i, j)

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

        # move the ball and check for paddle hit
        if self.ball.move(self.paddle.location.x):
            # go through all of the bricks check for hits
            for i in range(BRICK_COLS):
                for j in range(BRICK_ROWS):
                    self.bricks[(i, j)].hit_test(self.ball)
            self.draw_window()
        else:
            # ball reports that it is lost, change the ball
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
        label = font.render("Dad's Awesome Breakout", 1, FONT_COLOR)
        self.surface.blit(label, (TOPLEFT_X + PLAY_WIDTH/2 - label.get_width()/2, 30))

        # draw the playing area:
        pygame.draw.rect(self.surface, PLAYAREA_COLOR,
                         (TOPLEFT_X - 2, TOPLEFT_Y - 2, PLAY_WIDTH + 4, PLAY_HEIGHT + 4),
                         0)
        pygame.draw.rect(self.surface, BORDER_COLOR,
                         (TOPLEFT_X - 2, TOPLEFT_Y - 2, PLAY_WIDTH + 4, PLAY_HEIGHT + 4),
                         2)

        # draw the bricks
        for i in range(BRICK_COLS):
            for j in range(BRICK_ROWS):
                brick = self.bricks[(i, j)]
                if not brick.hidden:
                    pygame.draw.rect(self.surface, BRICK_COLORS[j],
                                     (brick.screen_location.x - BRICK_WIDTH/2,
                                      brick.screen_location.y - BRICK_HEIGHT/2,
                                      BRICK_WIDTH,
                                      BRICK_HEIGHT),
                                     0)

        # draw the ball
        if draw_ball:
            pygame.draw.circle(self.surface,
                               BALL_COLOR,
                               (self.ball.location.x, self.ball.location.y),
                               BALL_RADIUS)

        # draw the paddle
        pygame.draw.rect(self.surface,
                         PADDLE_COLOR,
                         (self.paddle.location.x - PADDLE_WIDTH / 2,
                          self.paddle.location.y,
                          PADDLE_WIDTH,
                          PADDLE_HEIGHT),
                         0)

        # draw the extra balls
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
