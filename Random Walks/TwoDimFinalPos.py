import random
import matplotlib.pyplot as plt

#number of trials
nTrials = 200

#number of steps
nSteps = 10000

moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
w = [1, 1, 1, 1]

finalX = []
finalY = []

for trial in range(nTrials):
    x = 0
    y = 0

    for i in range(nSteps):
        xStep, yStep = random.choices(moves, weights=w)[0]
        x = x+xStep
        y = y+yStep

    finalX.append(x)
    finalY.append(y)

plt.scatter(finalX,finalY)

w = [1.1, 1, 1, 1]

finalX = []
finalY = []

for trial in range(nTrials):
    x = 0
    y = 0

    for i in range(nSteps):
        xStep, yStep = random.choices(moves, weights=w)[0]
        x = x+xStep
        y = y+yStep

    finalX.append(x)
    finalY.append(y)

plt.scatter(finalX,finalY,color='red')

plt.show()