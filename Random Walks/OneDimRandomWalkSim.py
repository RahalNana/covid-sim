import random
import matplotlib.pyplot as plt


#number of trials
nTrials = 1000

#number of steps
nSteps = 100

moves = [-1, 1]
out = [0.0]*(2*nSteps+1)
x = list(range(-nSteps, nSteps+1))

for i in range(nTrials):
    pos = 0
    for j in range(nSteps):
        pos += random.choice(moves)
    out[pos+nSteps] += 1

res = [k/nTrials for k in out]

plt.bar(x, res)
plt.show()