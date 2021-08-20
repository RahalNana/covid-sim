import math

import pygame
import sys
from pygame.locals import *
import random

# COLORS
YELLOW = (255, 255, 0)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
RED = (255, 0, 0)
GREY = (150, 150, 150)

# SIZES
X_LIM = 1400
Y_LIM = 700
WINDOW_SIZE = (X_LIM, Y_LIM)

# CITIES
nCity = 15
minCitySize = 100
maxCitySize = 200
minPopSize = 30
maxPopSize = 50

# MOTION
moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
vLim = 1
dLim = 20

# PROBABILITIES
pTravel = 0.001
pInf = 0.02

# MODEL CONSTANTS
nInf = 5
S = 0
I = 1
R = 2


class Person:
    def __init__(self, x, y, resCity):
        self.x = x
        self.y = y
        self.xVel = 0
        self.yVel = 0
        self.resCity = resCity
        self.migrating = False
        self.destCity = resCity
        self.color = BLUE
        self.status = S


class City:
    def __init__(self):
        self.center = (random.randint(0, X_LIM), random.randint(0, Y_LIM))
        self.size = random.randint(minCitySize, maxCitySize)
        self.left = int(self.center[0] - self.size / 2)
        self.right = int(self.center[0] + self.size / 2)
        self.top = int(self.center[1] - self.size / 2)
        self.bottom = int(self.center[1] + self.size / 2)
        self.rect = pygame.Rect(self.left, self.top, self.size, self.size)


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Markov Model Based Random Motion")
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    screen.fill((0, 0, 0))

    cityList = [City() for x in range(nCity)]
    pop = []

    for city in cityList:
        cityPep = [Person(random.randint(city.left, city.right),
                          random.randint(city.top, city.bottom),
                          city) for i in range(random.randint(minPopSize, maxPopSize))]
        pop = pop + cityPep
    n = len(pop)

    infPeople = random.sample(pop, nInf)
    for person in infPeople:
        person.status = I
        person.color = RED

    while True:
        for city in cityList:
            pygame.draw.rect(screen, YELLOW, city.rect, width=1)

        for i in range(n):
            person = pop[i]
            if random.random() < pTravel:
                person.migrating = True
                person.destCity = cityList[random.choices(range(nCity))[0]]
                print(random.choices(range(nCity))[0])
                person.xVel = (person.destCity.center[0] - person.x)
                person.yVel = (person.destCity.center[1] - person.y)
                vMag = math.sqrt(person.xVel ** 2 + person.yVel ** 2)
                person.xVel *= vLim * 1.2 / vMag
                person.yVel *= vLim * 1.2 / vMag

            if person.migrating:
                person.x += person.xVel
                person.y += person.yVel
                if (person.destCity.left < person.x < person.destCity.right) \
                        and (person.destCity.top < person.y < person.destCity.bottom):
                    person.migrating = False
                    person.resCity = person.destCity

            else:
                xAcc, yAcc = random.choices(moves)[0]
                if -vLim < person.xVel + xAcc * 0.1 < vLim:
                    person.xVel = person.xVel + xAcc * 0.1
                if -vLim < person.yVel + yAcc * 0.1 < vLim:
                    person.yVel = person.yVel + yAcc * 0.1

                if person.resCity.left < person.x + person.xVel < person.resCity.right:
                    person.x += person.xVel
                else:
                    person.xVel = 0
                if person.resCity.top < person.y + person.yVel < person.resCity.bottom:
                    person.y += person.yVel
                else:
                    person.yVel = 0

            for j in range(i + 1, n):
                if pop[i].status == I or pop[j].status == I:
                    if (pop[i].x - pop[j].x) ** 2 + (pop[i].y - pop[j].y) ** 2 <= dLim and random.random() < pInf:
                        if pop[i].status == S:
                            pop[i].status = I
                            pop[i].color = RED
                            nInf += 1
                        elif pop[j].status == S:
                            pop[j].status = I
                            pop[j].color = RED
                            nInf += 1

            pygame.draw.circle(screen, person.color, [person.x, person.y], 5)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        # clock.tick(60)
        screen.fill((0, 0, 0))
