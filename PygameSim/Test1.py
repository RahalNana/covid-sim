import pygame, sys

from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()  # sets up clock
pygame.display.set_caption("Test Window")
WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

ball = pygame.image.load('BlueBall.png')
ballLoc = [100, 100]

yMomentum = 0

xVel = 2
yVel = 2
g = 0.2

movLeft = False
movRight = False
movUp = False
movDown = False

while True:
    screen.fill((0, 0, 0))
    screen.blit(ball, ballLoc)

    if movDown:
        yMomentum += yVel
    if movUp:
        yMomentum -= yVel
    if movRight:
        ballLoc[0] += xVel
    if movLeft:
        ballLoc[0] -= xVel

    if ballLoc[1] + ball.get_height() > WINDOW_SIZE[1]:
        yMomentum = -0.8*yMomentum
    else:
        yMomentum += g
    ballLoc[1] += yMomentum

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                movRight = True
            if event.key == K_LEFT:
                movLeft = True
            if event.key == K_UP:
                movUp = True
            if event.key == K_DOWN:
                movDown = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                movRight = False
            if event.key == K_LEFT:
                movLeft = False
            if event.key == K_UP:
                movUp = False
            if event.key == K_DOWN:
                movDown = False

    pygame.display.update()
    clock.tick(60)  # keeps window running at 60fps
