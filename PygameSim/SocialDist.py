import pygame, sys, random, math
import numpy as np
from pygame.locals import *

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
pDead = 0.2
pImmune = 0

moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]

x = []
y = []
xVel = [0] * n
yVel = [0] * n
color = [BLUE] * n
duration = [0] * n
status = [0] * n  # 0 - uninfected, 1- infected, 2 - immune, 3 - dead

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
    stat = stat[0]
    if stat == UNINFECTED:
        return BLUE
    if stat == INFECTED:
        return RED
    if stat == IMMUNE:
        return GREEN
    if stat == DEAD:
        return BLACK


delX = 0
delY = 0
dist = 0

x = np.array(x)
y = np.array(y)

while True:
    screen.fill((0, 0, 0))

    for i in range(n):
        xAcc = 0.0
        yAcc = 0.0
        delX = x - x[i]
        delY = y - y[i]
        # print(delX)
        # print(delY)
        dist = np.sqrt(np.square(delX) + np.square(delY))
        accX = np.divide(delX, np.power(dist, 3))
        accY = np.divide(delY, np.power(dist, 3))
        # print(accX)
        # print(accY)
        xAcc = np.nansum(accX[dist < 100])
        yAcc = np.nansum(accY[dist < 100])

        for j in range(i + 1, n):
            if status[i] == INFECTED or status[j] == INFECTED:
                if (x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2 <= dLim and random.random() < pInf:
                    if status[j] == 0:
                        status[j] = INFECTED
                        color[j] = RED
                        duration[j] = random.randint(iTimeLower, iTimeUpper)
                    elif status[i] == 0:
                        status[i] = INFECTED
                        color[i] = RED
                        duration[i] = random.randint(iTimeLower, iTimeUpper)

        xVel[i] = xVel[i] - 100 * xAcc
        yVel[i] = yVel[i] - 100 * yAcc

        if 0 < x[i] + xVel[i] < WINDOW_SIZE[0]:
            x[i] = x[i] + xVel[i]
        else:
            xVel[i] = 0
        if 0 < y[i] + yVel[i] < WINDOW_SIZE[1]:
            y[i] = y[i] + yVel[i]
        else:
            yVel[i] = 0

        if duration[i] == 0 and status[i] == INFECTED:
            status[i] = random.choices(outcomes, pOut)
            color[i] = colorOf(status[i])
        else:
            duration[i] -= 1
        pygame.draw.circle(screen, color[i], [x[i], y[i]], 5)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)
