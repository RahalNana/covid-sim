import math
import numpy as np
import pygame
import sys
from pygame.locals import *
import random

# COLORS
YELLOW = (255, 255, 0)
ORANGE = (255, 185, 0)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)

# SIZES
X_LIM = 1500
Y_LIM = 750
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
vTrans = 5
dLim = 20

# PROBABILITIES
pTravel = 0.0005
pInf = 0.2
pSus = 0.001

# infected time upper and lower limit
iTimeUpper = 500
iTimeLower = 200

# exposed time upper and lower limit
eTimeUpper = 200
eTimeLower = 100

# MODEL CONSTANTS
nInf = 5
S = 0
I = 1
R = 2
E = 3

pInfPow = 0
pInfVal = 0
while pInf < 1:
    pInf *= 10
    pInfPow += 1
while pInf >= 1:
    pInf -= 1
    pInfVal += 1

pTravPow = 0
pTravVal = 0
while pTravel < 1:
    pTravel *= 10
    pTravPow += 1
while pTravel >= 1:
    pTravel -= 1
    pTravVal += 1


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
        self.time = 0


class City:
    def __init__(self):
        self.center = (random.randint(minCitySize / 2, X_LIM - minCitySize / 2),
                       random.randint(minCitySize / 2, Y_LIM - minCitySize / 2))
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

    xPos = np.array([person.x for person in pop])
    yPos = np.array([person.y for person in pop])
    xPos = xPos.reshape((1, n))
    yPos = yPos.reshape((1, n))

    status = np.zeros(n, dtype=int)
    rVal = np.zeros(n, dtype=int)
    immune = np.zeros(n, dtype=int)

    infPeople = random.sample(range(n), nInf)
    for i in infPeople:
        person = pop[i]
        person.status = E
        status[i] = I
        person.color = ORANGE
        person.time = random.randint(eTimeLower, eTimeUpper)

    dist = 0

    while True:
        for city in cityList:
            pygame.draw.rect(screen, YELLOW, city.rect, width=1)

        # interactions vectorized
        dist = np.square(xPos - xPos.T) + np.square(yPos - yPos.T)
        inf = np.multiply(np.multiply((np.random.rand(n, n) < pInf), dist < dLim),
                          status)  # checks if infected person is within dLim and accout for probabilitstic infectioin
        inf = np.multiply(status.reshape(n, 1) < 1, (
                inf - np.identity(n, dtype=int)) > 0)  # removes self infection and re-infection of already infected
        inf = np.multiply(immune.reshape(n, 1) < 1, inf)  # removes immune cases
        status = 1 * ((status + np.sum(inf, axis=1)) > 0)  # update infection status
        rVal = rVal + np.sum(inf, axis=0)  # updates rVal (R0 measure)
        nInf = np.sum(status)

        # PRINT R0
        # print(np.average(rVal[rVal > 0]))

        for i in range(n):
            person = pop[i]
            if random.random() < pTravel:
                person.migrating = True
                # immune[i] = 1     # makes people immune while travelling
                person.destCity = cityList[random.choices(range(nCity))[0]]
                person.xVel = (person.destCity.center[0] - person.x)
                person.yVel = (person.destCity.center[1] - person.y)
                vMag = math.sqrt(person.xVel ** 2 + person.yVel ** 2)
                person.xVel *= vTrans / vMag
                person.yVel *= vTrans / vMag

            if person.migrating:
                person.x += person.xVel
                person.y += person.yVel
                if (person.destCity.left < person.x < person.destCity.right) \
                        and (person.destCity.top < person.y < person.destCity.bottom):
                    person.migrating = False
                    # immune[i] = 0
                    person.xVel = person.xVel * vLim / vTrans
                    person.yVel = person.yVel * vLim / vTrans
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

            xPos[0, i] = person.x
            yPos[0, i] = person.y

            if status[i] == I:
                if person.status == S:
                    person.status = E
                    person.time = random.randint(eTimeLower, eTimeUpper)
                elif person.time == 0:
                    if person.status == E:
                        person.status = I
                        person.time = random.randint(iTimeLower, iTimeUpper)
                    elif person.status == I:
                        status[i] = S
                        person.status = R
                        immune[i] = 1
                else:
                    person.time -= 1

            if immune[i] == 1 and random.random() < pSus:
                immune[i] = 0
                person.status = S

            person.color = BLUE if person.status == S else GREY if person.status == R else ORANGE if person.status == E else RED
            pygame.draw.circle(screen, person.color, [person.x, person.y], 5)

        pInfText = pygame.font.Font('freesansbold.ttf', 32).render("pInf = " + str(round(pInf, 5)), True, WHITE)
        screen.blit(pInfText, (10, 10))

        pTravText = pygame.font.Font('freesansbold.ttf', 32).render("pTravel = " + str(round(pTravel, 5)), True, WHITE)
        screen.blit(pTravText, (10, 50))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if pInfVal == 9:
                        pInfPow -= 1
                        pInfVal = 1
                    else:
                        pInfVal += 1
                if event.key == pygame.K_DOWN:
                    if pInfVal == 1:
                        pInfPow += 1
                        pInfVal = 9
                    else:
                        pInfVal -= 1
                if event.key == pygame.K_RIGHT:
                    if pTravVal == 9:
                        pTravPow -= 1
                        pTravVal = 1
                    else:
                        pTravVal += 1
                if event.key == pygame.K_LEFT:
                    if pTravVal == 1:
                        pTravPow += 1
                        pTravVal = 9
                    else:
                        pTravVal -= 1

        pInf = pInfVal * (0.1 ** pInfPow)
        pTravel = pTravVal * (0.1 ** pTravPow)

        pygame.display.update()
        clock.tick(60)
        screen.fill((0, 0, 0))
