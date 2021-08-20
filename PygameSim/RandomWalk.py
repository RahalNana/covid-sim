import pygame, sys, random
from pygame.locals import *
import matplotlib.pyplot as plt
import numpy as np

pygame.init()

clock = pygame.time.Clock()
WINDOW_SIZE = (700, 700)

BLUE = (50, 50, 255)
RED = (255, 0, 0)
BLACK = (150, 150, 150)
GREEN = (50, 255, 50)
# BLACK = (0, 0, 0)

pygame.display.set_caption("Random Walk")
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

# number of people
n = 200
nInf = 1  # number of infected
vLim = 1
dLim = 20

# infected time upper and lower limit
iTimeUpper = 600
iTimeLower = 200

# infection probability
pInf = 0.02
pDead = 1
pImmune = 0

moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]

x = []
y = []
xVel = [0] * n
yVel = [0] * n
color = [BLUE] * n
duration = [0] * n
nTrans = [0] * n  # no of people infected by given person
status = [0] * n  # 0 - uninfected, 1- infected, 2 - immune, 3 - dead
nDead = 0
t = 0
Ts = 60
epiCurveDat = []

UNINFECTED = 0
INFECTED = 1
IMMUNE = 2
DEAD = 3

outcomes = [UNINFECTED, IMMUNE, DEAD]
pOut = [1 - pImmune - pDead, pImmune, pDead]
dLim = dLim ** 2

for i in range(n):
    x.append(random.randrange(WINDOW_SIZE[0]))
    y.append(random.randrange(WINDOW_SIZE[0]))

# generate infected people
for i in random.sample(range(n), nInf):
    color[i] = RED
    status[i] = INFECTED
    duration[i] = random.randint(iTimeLower, iTimeUpper)


def colorOf(stat):
    if stat == UNINFECTED:
        return BLUE
    if stat == INFECTED:
        return RED
    if stat == IMMUNE:
        return GREEN
    if stat == DEAD:
        return BLACK


while True:
    t += 1
    screen.fill((0, 0, 0))

    for i in range(n):
        xAcc, yAcc = random.choices(moves)[0]
        if -vLim < xVel[i] + xAcc * 0.1 < vLim:
            xVel[i] = xVel[i] + xAcc * 0.1
        if -vLim < yVel[i] + yAcc * 0.1 < vLim:
            yVel[i] = yVel[i] + yAcc * 0.1

        if 0 < x[i] + xVel[i] < WINDOW_SIZE[0]:
            x[i] = x[i] + xVel[i]
        else:
            xVel[i] = 0
        if 0 < y[i] + yVel[i] < WINDOW_SIZE[1]:
            y[i] = y[i] + yVel[i]
        else:
            yVel[i] = 0
        for j in range(i + 1, n):
            if status[i] == INFECTED or status[j] == INFECTED:
                if (x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2 <= dLim and random.random() < pInf:
                    if status[j] == 0:
                        status[j] = INFECTED
                        color[j] = RED
                        duration[j] = random.randint(iTimeLower, iTimeUpper)
                        nTrans[i] += 1
                        nInf += 1
                    elif status[i] == 0:
                        status[i] = INFECTED
                        color[i] = RED
                        duration[i] = random.randint(iTimeLower, iTimeUpper)
                        nTrans[j] += 1
                        nInf += 1
        if duration[i] == 0 and status[i] == INFECTED:
            status[i] = random.choices(outcomes, pOut)[0]
            color[i] = colorOf(status[i])
            nInf -= 1
            if status[i] == DEAD:
                nDead += 1
        else:
            duration[i] -= 1
        pygame.draw.circle(screen, color[i], [x[i], y[i]], 5)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)

