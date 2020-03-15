#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' BirksBeamer Breakout '''
import math
import pygame

# TODO: sounds
# TODO: power ups!

FRAME_RATE = 100
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
PLAY_WIDTH = 960
PLAY_HEIGHT = 600
TOPLEFT_X = (SCREEN_WIDTH  - PLAY_WIDTH) // 2
TOPLEFT_Y = (SCREEN_HEIGHT - PLAY_HEIGHT) // 2
BACKGROUND_COLOR = (200, 200, 200)
FONT_COLOR = (84, 13, 110)
BORDER_COLOR = (255, 210, 63)
BALL_COLOR = (238, 66, 102)
BALL_RADIUS = 10
BALL_START_X = BALL_RADIUS
BALL_START_Y = PLAY_HEIGHT / 2
BALL_START_VELOCITY_X = 2
BALL_START_VELOCITY_Y = 2
PADDLE_COLOR = (14, 173, 105)
PLAYAREA_COLOR = (40, 40, 40)
PADDLE_HEIGHT = 12
PADDLE_WIDTH = 100
PADDLE_BUFFER = 2
PADDLE_MOVE_SPEED = 4
MAX_ANGLE_CHANGE = 2 * math.atan(1)
MAX_DEPART_ANGLE = math.acos(.5)

BRICK_ROWS = 5
BRICK_COLS = 15
BRICK_HEIGHT = 20
BRICK_SPACING = 2
BRICK_WIDTH = (PLAY_WIDTH - (BRICK_COLS + 1) * BRICK_SPACING) / BRICK_COLS
ATTIC_HEIGHT = 60
BRICK_COLORS = ((188, 182, 255),
                (184, 225, 255),
                (169, 255, 247),
                (148, 251, 171),
                (130, 171, 161))

# Power Ups
POWER_UP_FREQUENCY = 40
POWER_UP_TYPES = ["board_length"]  # "ball_split", "paddle_guns", "ball_swell", "sticky_paddle"
POWER_UP_LENGTH = 15

# Scoring
BRICK_VALUES = [15, 10, 5, 3, 1]
SCORE_POWER_UP = 50
SCORE_LEVEL = 100

class Point:
    ''' a simple class to keep track of coordinates'''
    def __init__(self, x, y):
        self.x = x
        self.y = y

class BreakoutPaddle:
    '''' BreakoutPaddle class '''
    def __init__(self):
        self.location = Point(PLAY_WIDTH / 2, PLAY_HEIGHT - PADDLE_HEIGHT - PADDLE_BUFFER)
        self.width = PADDLE_WIDTH

    def set_location(self, x):
        ''' moves the paddle to the provided location '''
        self.location.x = x
        if self.location.x > PLAY_WIDTH - self.width / 2:
            self.location.x = PLAY_WIDTH - self.width / 2
        if self.location.x < self.width / 2:
            self.location.x = self.width / 2

    def move(self, relative_x):
        ''' move the paddle by a relative amount from current location '''
        self.set_location(self.location.x + relative_x)

class BreakoutBrick:
    '''' BreakoutBrick class '''
    def __init__(self, col, row, power_up=False):
        self.grid_location = Point(row, col)
        x = BRICK_WIDTH / 2 + BRICK_SPACING + col * (BRICK_WIDTH + BRICK_SPACING)
        y = ATTIC_HEIGHT + BRICK_HEIGHT / 2 + row * (BRICK_HEIGHT + BRICK_SPACING)
        self.location = Point(x, y)
        self.hidden = False
        self.color = BRICK_COLORS[row]
        self.value = BRICK_VALUES[row]
        self.power_up = power_up

    def screen_loc(self):
        ''' screen_loc is a simple helper to get the brick's drawn location '''
        return pygame.Rect(TOPLEFT_X + self.location.x - BRICK_WIDTH/2,
                           TOPLEFT_Y + self.location.y - BRICK_HEIGHT/2,
                           BRICK_WIDTH, BRICK_HEIGHT)

class BreakoutBall:
    '''' BreakoutBall class '''
    def __init__(self):
        self.location = Point(BALL_START_X, BALL_START_Y)
        self.velocity = Point(BALL_START_VELOCITY_X, BALL_START_VELOCITY_Y)

    def set_location(self, x, y, vel_x, vel_y):
        ''' moves the ball to the provided location '''
        self.location.x = x
        self.location.y = y
        self.velocity.x = vel_x
        self.velocity.y = vel_y

    def hit(self, brick):
        ''' check for brick hit '''
        if brick.hidden:
            return False

        if abs(self.location.x - brick.location.x) <= BRICK_WIDTH/2:
            if abs(self.location.y - brick.location.y) <= BRICK_HEIGHT/2 + BALL_RADIUS:
                # vertical hit
                self.velocity.y = -self.velocity.y
                return True

        if abs(self.location.y - brick.location.y) <= BRICK_HEIGHT/2:
            if abs(self.location.x - brick.location.x) <= BRICK_WIDTH/2 + BALL_RADIUS:
                # horizontal hit
                self.velocity.x = -self.velocity.x
                return True

        return False

    def move(self, paddle, bricks):
        ''' moves the ball, bounce off the constraints of our field, and check
            for brick and paddle hits '''
        points = 0
        # move
        self.location.x += self.velocity.x
        self.location.y += self.velocity.y
        # check for walls, left and right
        if self.location.x < BALL_RADIUS or self.location.x > PLAY_WIDTH - BALL_RADIUS:
            self.velocity.x = -self.velocity.x
        # check for walls, top:
        if self.location.y < BALL_RADIUS:
            self.velocity.y = -self.velocity.y
        # check for lost off edge of screen
        if self.location.y >= PLAY_HEIGHT + BALL_RADIUS:
            self.velocity.y = 0
            self.velocity.x = 0
            # return that all is not well
            return False, points

        # paddle hitting - is the leading edge of the ball within the hit area of the paddle
        vertical_distance = self.location.y + BALL_RADIUS - paddle.location.y
        if 0 <= vertical_distance <= self.velocity.y:
            distance_to_paddle_center = self.location.x - paddle.location.x
            if abs(distance_to_paddle_center) <= PADDLE_WIDTH / 2:
                # this is a paddle hit.  these next lines calculate the new
                # ball trajectory:
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

        # check for brick hits
        for brick in bricks:
            if self.hit(brick):
                brick.hidden = True
                points += brick.value

        return True, points

class BreakoutGame:
    '''' BreakoutGame class '''
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Dad's Awesome Breakout")
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                               pygame.FULLSCREEN | pygame.SCALED)
        self.ball = BreakoutBall()
        self.paddle = BreakoutPaddle()
        self.lives = 3
        self.score = 0
        self.bricks = [BreakoutBrick(i, j) for i in range(BRICK_COLS) for j in range(BRICK_ROWS)]

    def bricks_left(self):
        ''' bricks left: just a quick helper to count the remaining bricks'''
        total = BRICK_COLS * BRICK_ROWS
        return len([self.bricks[i] for i in range(total) if not self.bricks[i].hidden])

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
        success, points = self.ball.move(self.paddle, self.bricks)
        if not success:
            # ball reports that it is lost, change the ball
            self.lives -= 1
            if self.lives == 0:
                running = False
            # this ball is done... create a new one:
            self.ball = BreakoutBall()
        self.score += points

        self.draw_window(self.bricks_left() == 0)

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
            clock.tick_busy_loop(FRAME_RATE)

        # all done, do any clean up here:
        pygame.quit()

    def draw_window(self, winner=False):
        """ draw_window function """

        # start with a solid background
        self.surface.fill(BACKGROUND_COLOR)

        # write something at the top
        font = pygame.font.SysFont("trebuchetmsboldttf", 60)
        label = font.render("Dad's Awesome Breakout", True, FONT_COLOR, BACKGROUND_COLOR)
        self.surface.blit(label, (TOPLEFT_X + PLAY_WIDTH/2 - label.get_width()/2, 30))

        # draw the playing area:
        pygame.draw.rect(self.surface, PLAYAREA_COLOR,
                         (TOPLEFT_X - 2, TOPLEFT_Y - 2, PLAY_WIDTH + 4, PLAY_HEIGHT + 4),
                         0)

        # draw the ball
        pygame.draw.circle(self.surface, BALL_COLOR,
                           (TOPLEFT_X + self.ball.location.x, TOPLEFT_Y + self.ball.location.y),
                           BALL_RADIUS)

        # draw the background strip and border around the play area, which obscure
        # the ball as it leaves the screen:
        pygame.draw.rect(self.surface, BACKGROUND_COLOR,
                         (TOPLEFT_X, TOPLEFT_Y + PLAY_HEIGHT + 1, PLAY_WIDTH, BALL_RADIUS * 2),
                         0)
        pygame.draw.rect(self.surface, BORDER_COLOR,
                         (TOPLEFT_X - 2, TOPLEFT_Y - 2, PLAY_WIDTH + 4, PLAY_HEIGHT + 4),
                         2)

        # draw the bricks
        for brick in self.bricks:
            if not brick.hidden:
                pygame.draw.rect(self.surface, brick.color, brick.screen_loc(), 0)

        # draw the paddle
        pygame.draw.rect(self.surface, PADDLE_COLOR,
                         (TOPLEFT_X + self.paddle.location.x - PADDLE_WIDTH / 2,
                          TOPLEFT_Y + self.paddle.location.y,
                          PADDLE_WIDTH, PADDLE_HEIGHT), 0)

        # draw the extra balls
        for ball_index in range(self.lives - 1):
            pygame.draw.circle(self.surface, BALL_COLOR,
                               (TOPLEFT_X + BALL_RADIUS + 3*BALL_RADIUS*ball_index,
                                TOPLEFT_Y + PLAY_HEIGHT + 2*BALL_RADIUS),
                               BALL_RADIUS, 0)

        # draw the scoreboard
        pygame.draw.rect(self.surface, PLAYAREA_COLOR, (TOPLEFT_X, TOPLEFT_Y - 50, 100, 40), 0)
        pygame.draw.rect(self.surface, BORDER_COLOR, (TOPLEFT_X, TOPLEFT_Y - 50, 100, 40), 2)
        font = pygame.font.SysFont("couriernewboldttf", 28)
        label = font.render("{:04d}".format(self.score), True, (255, 255, 255), PLAYAREA_COLOR)
        self.surface.blit(label,
                          (TOPLEFT_X + 50 - label.get_width()/2,
                           TOPLEFT_Y - 28 - label.get_height()/2))

        if winner:
            font = pygame.font.SysFont("trebuchetmsboldttf", 60)
            label = font.render("You Win!!!", True, BACKGROUND_COLOR, PLAYAREA_COLOR)
            self.surface.blit(label,
                              (SCREEN_WIDTH/2 - label.get_width()/2,
                               SCREEN_HEIGHT/2 - label.get_height()/2))

        # update the screen with what we've drawn.
        pygame.display.flip()

def main():
    ''' main function '''
    game = BreakoutGame()
    game.play()

if __name__ == '__main__':
    main()
