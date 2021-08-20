import pygame
import sys
import random
from pygame.locals import *
import matplotlib.pyplot as plt
import numpy as np

BLUE = (50, 50, 255)
RED = (255, 0, 0)
BLACK = (150, 150, 150)
GREEN = (50, 255, 50)
WINDOW_SIZE = (700, 700)
UNINFECTED = 0
INFECTED = 1
IMMUNE = 2
DEAD = 3


class Person:
    def __init__(self, pInf=0.02, life=True, immunitystatus=False, status=False, iTimeUpper=600, iTimeLower=200, vLim=1,
                 dLim=20, xVel=0, yVel=0, x=0, y=0, duration=0, pDead=1, pImmune=0):
        # infection probability
        self.pInf = 0.02
        self.life = life
        self.immunitystatus = immunitystatus
        self.status = UNINFECTED
        # status time upper and lower limit
        self.iTimeUpper = iTimeUpper
        self.iTimeLower = iTimeLower
        self.vLim = vLim
        self.dLim = dLim ** 2
        self.moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
        self.nTrans = 0  # no of people status by given person
        self.xVel = xVel
        self.yVel = yVel
        self.x = x
        self.y = y
        self.color = BLUE
        self.nTrans = 0
        self.duration = duration
        self.outcomes = [UNINFECTED, IMMUNE, DEAD]
        self.pDead = pDead
        self.pImmune = pImmune
        self.pOut = [1 - pImmune - pDead, pImmune, pDead]


class Population:
    def __init__(self, n=200, nofInfected=1, nDead=0):
        self.n = n  # Number of people
        self.nInf = nofInfected  # Number of status people
        self.people = []
        for i in range(self.n):
            self.people.append(Person())
        self.nDead = nDead
        self.positions()
        self.genInf()

    def genInf(self):
        # generate status people
        for i in random.sample(range(self.n), self.nInf):
            self.people[i].color = RED
            self.people[i].status = INFECTED
            self.people[i].duration = random.randint(self.people[i].iTimeLower, self.people[i].iTimeUpper)

    def positions(self):
        for i in range(self.n):
            self.people[i].x = random.randrange(WINDOW_SIZE[0])
            self.people[i].y = random.randrange(WINDOW_SIZE[0])


def colorOf(stat):
    if stat == UNINFECTED:
        return BLUE
    if stat == INFECTED:
        return RED
    if stat == IMMUNE:
        return GREEN
    if stat == DEAD:
        return BLACK


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Random Walk")
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

    # Form a population
    population = Population(n=200, nofInfected=1, )
    # start simulation
    nInf = 1  # Total number of status
    t = 0
    while True:
        t += 1
        screen.fill((0, 0, 0))

        for i in range(population.n):
            person = population.people[i]
            xAcc, yAcc = random.choices(person.moves)[0]
            if -person.vLim < person.xVel + xAcc * 0.1 < person.vLim:
                person.xVel = person.xVel + xAcc * 0.1
            if -person.vLim < person.yVel + yAcc * 0.1 < person.vLim:
                person.yVel = person.yVel + yAcc * 0.1

            if 0 < person.x + person.xVel < WINDOW_SIZE[0]:
                person.x += person.xVel
            else:
                person.xVel = 0
            if 0 < person.y + person.yVel < WINDOW_SIZE[1]:
                person.y += person.yVel
            else:
                person.yVel = 0
            print(nInf)
            for j in range(i + 1, population.n):
                contact = population.people[j]
                if person.status == INFECTED or contact.status == INFECTED:
                    if (person.x - contact.x) ** 2 + (person.y - contact.y) ** 2 <= min(person.dLim,
                                                                                        contact.dLim) and random.random() < min(
                            person.pInf, contact.pInf):
                        if contact.status == UNINFECTED:
                            contact.status = INFECTED
                            contact.color = RED
                            contact.duration = random.randint(contact.iTimeLower, contact.iTimeUpper)
                            contact.nTrans += 1
                            nInf += 1
                        elif person.status == UNINFECTED:
                            person.status = INFECTED
                            person.color = RED
                            person.duration = random.randint(person.iTimeLower, person.iTimeUpper)
                            person.nTrans += 1
                            nInf += 1
                population.people[j] = contact  # update

            if person.duration == 0 and person.status == INFECTED:
                person.status = random.choices(person.outcomes, person.pOut)[0]
                person.color = colorOf(person.status)
                population.nInf -= 1
                if person.status == DEAD:
                    population.nDead += 1
            else:
                person.duration -= 1
            pygame.draw.circle(screen, person.color, [person.x, person.y], 5)
            population.people[i] = person  # update

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)
