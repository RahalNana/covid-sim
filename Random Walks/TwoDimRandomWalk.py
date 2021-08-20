import random
import matplotlib.pyplot as plt

#number of trials
nTrials = 5

#number of steps
nSteps = 10000

moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
w = [1.1, 1, 1, 1]

for trial in range(nTrials):
    #starting pos
    x = [0]
    y = [0]

    for i in range(nSteps):
        xStep, yStep = random.choices(moves, weights=w)[0]
        x.append(x[i]+xStep)
        y.append(y[i]+yStep)

    plt.plot(x,y, c=[random.random(),random.random(),random.random()])

plt.show()