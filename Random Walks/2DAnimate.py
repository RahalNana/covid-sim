import random
import matplotlib.pyplot as plt
import math


# number of steps
nSteps = 10000

# number of agents
nAgents = 50

lim = int(math.sqrt(nSteps))
moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
w = [1, 1, 1, 1]

# colors
c = []

# starting pos
x = []
y = []
for i in range(nAgents):
    x.append(random.randrange(lim) - lim // 2)
    y.append(random.randrange(lim) - lim // 2)
    c.append([random.random(), random.random(), random.random()])

for i in range(nSteps):
    plt.clf()
    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)
    for j in range(nAgents):
        xStep, yStep = random.choices(moves, weights=w)[0]
        x[j] = x[j] + xStep
        y[j] = y[j] + yStep
        plt.scatter(x[j], y[j], color=c[j])
    plt.pause(0.001)
plt.show()
