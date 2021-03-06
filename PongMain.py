# Pong Game using Python and the PyGame package
# Blake Niebrugge, CS330, Fall 2021

# Code for basic single-host Pong game has been adapted and optimized from 101Computing,net
# https://www.101computing.net/pong-tutorial-using-pygame-getting-started/


# import and initalize pygame library
import sys

import pygame
# import paddle sprites
from network import Network
from paddle import Paddle
# import ball

from ball import Ball
import tkinter as tk
from tkinter import messagebox
import time

pygame.init()
pygame.font.init()
# set local colors: Black for background, white for text, blue and red for teams
Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Blue = (0, 0, 255)

# create paddles using paddle class and add them to a list of sprites
paddleLeft = Paddle(Red, 10, 100)
paddleLeft.rect.x = 20
paddleLeft.rect.y = 200

paddleRight = Paddle(Blue, 10, 100)
paddleRight.rect.x = 870
paddleRight.rect.y = 200

ball = Ball(White, 10, 10)
ball.rect.x = 445
ball.rect.y = 195

allSprites = pygame.sprite.Group()
allSprites.add(paddleLeft)
allSprites.add(paddleRight)
allSprites.add(ball)

# set game window
size = (900, 500)
pygame.display.set_caption("Multiplayer Pong")


# to the functionality, we will have a while loop that will listen to user inputs, adding logic to the game (score,
# boundaries, etc.), and refreshing the program global "running" funtion that will control the while loop, simple bool
class game():
    size = (900, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Multiplayer Pong")

    def __init__(self, paddleLeft, paddleRight, ball):
        self.rect = None
        self.net = Network()
        self.paddleLeft = paddleLeft
        self.paddleRight = paddleRight
        self.ball = ball
        self.velocity = 2
        self.width = 900
        self.height = 500

    def mUp(self, pixels):
        self.rect.y -= pixels
        # dont go off screen
        if self.rect.y < 0:
            self.rect.y = 0

    # move down function, alike above function
    def mDown(self, pixels):
        self.rect.y += pixels
        if self.rect.y > 400:
            self.rect.y = 400

    def run(self):

        running = True

        # need a clock for refreshing the screen (included in pygame package)
        clock = pygame.time.Clock()

        # scores for each side
        scoreLeft = 0
        scoreRight = 0

        # start loop
        while running:
            screen = pygame.display.set_mode(size)
            # --listen for inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if quit button is pressed, leave
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        running = False

                # keyboard inputs
                key = pygame.key.get_pressed()
                if key[pygame.K_w]:
                    paddleLeft.mUp(5)
                if key[pygame.K_s]:
                    paddleLeft.mDown(5)
                if key[pygame.K_UP]:
                    paddleRight.mUp(5)
                if key[pygame.K_DOWN]:
                    paddleRight.mDown(5)

                # --logic
                allSprites.update()

                # --drawing here (paddles, screen, scores, boundaries, etc
                screen.fill(Black)
                pygame.draw.line(screen, White, [448, 0], [448, 500], 4)

                allSprites.draw(screen)

                # check for left/right wall bounce - The sequence of events looks like this:
                # Check if ball hiit wall behind paddle
                # add to score, if score = 7, break from loop and end game
                # reset ball, wait for a second
                # send ball in direction of the play who scored last

                if ball.rect.x >= 890:
                    scoreLeft += 1
                    # messgae box using tkinter, delete the root window as soon as it shows up, then display alert
                    if scoreLeft == 7:
                        time.sleep(2)
                        break
                    ball.rect.x = 445
                    ball.rect.y = 195
                    time.sleep(2)
                    ball.velocity[0] = -ball.velocity[0]
                if ball.rect.x <= 0:
                    scoreRight += 1
                    if scoreRight == 7:
                        time.sleep(2)
                        break
                    ball.rect.x = 445
                    ball.rect.y = 195
                    time.sleep(2)
                    ball.velocity[0] = -ball.velocity[0]

                # reverse y-bound on collision with top or bottom
                if ball.rect.y >= 490:
                    ball.velocity[1] = -ball.velocity[1]
                if ball.rect.y <= 0:
                    ball.velocity[1] = -ball.velocity[1]

                # check for paddle hit
                if pygame.sprite.collide_mask(ball, paddleLeft) or pygame.sprite.collide_mask(ball, paddleRight):
                    ball.bounce()

                # display scores
                '''
                font = pygame.font.SysFont(, 50)
                text = font.render(str(scoreLeft), 1, Red)
                screen.blit(text, (420, 10))
                text = font.render(str(scoreRight), 1, Blue)
                screen.blit(text, (460, 10))
                '''
                # --update screen with drawings
                pygame.display.flip()
                # --60 fps limit
                clock.tick(60)

                self.paddleLeft, self.paddleLeft, self.ball = self.parse_data(self.send_data())

            # stop program once main loop is exited
            pygame.quit()

    def send_data(self):
        data = str(self.net.id) + ":" + str(self.paddleLeft) + "," + str(self.paddleRight) + "," + str(self.ball)
        reply = self.net.send(data)
        return reply
        pass

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1], int(d[2]))
        except:
            return 0, 0, 0
        pass
